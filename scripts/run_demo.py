"""FORESIGHT-HIL minimal end-to-end demo (numpy-only, no MuJoCo/Isaac needed).

Compares intervention strategies on the vectorized reach-avoid task under a
shared per-step human-query budget:

    none   : weak policy alone (no help)
    always : human acts on every alive env (budget-unaware upper bound on help)
    random : random-B candidates get help each step
    voi    : OUR foresighted VoI gate + top-B allocation

It reports, per strategy: success rate, failure rate, total human queries, and
(for gated strategies) the trigger's precision/recall against an eval-only
ground-truth lookahead ("would this trajectory have hit the hazard?").

Run:
    python scripts/run_demo.py
    python scripts/run_demo.py --num_envs 256 --episodes 6 --budget 16 \
        --human_noise 0.3 --human_delay 1
"""

from __future__ import annotations

import argparse
import sys
import os

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foresight_hil.envs.toy_reach import VectorReachEnv
from foresight_hil.models.ensemble_dynamics import EnsembleDynamics
from foresight_hil.oracle.scripted_human import ScriptedHuman
from foresight_hil.gating.voi_gate import VoIGate
from foresight_hil.agents.policy import WeakReachPolicy
from foresight_hil.allocation.budget import allocate_topk, allocate_random


def true_lookahead_failure(env, s, policy, H):
    """Eval-only: does the weak policy drive into hazard within H steps under
    the *true* noise-free dynamics? Used to score trigger precision/recall."""
    st = np.atleast_2d(s).copy()
    hit = env.in_hazard(st[:, :2])
    for _ in range(H):
        a = policy(st)
        st = env.true_dynamics(st, a)
        hit = hit | env.in_hazard(st[:, :2])
    return hit


def run_strategy(strategy, args, model=None):
    env = VectorReachEnv(num_envs=args.num_envs, max_steps=args.max_steps, seed=args.seed)
    policy = WeakReachPolicy(env.goal, noise=args.policy_noise, seed=args.seed + 1)
    human = ScriptedHuman(
        env.goal, env.hazard, env.hazard_radius,
        noise_std=args.human_noise, delay=args.human_delay,
        skill=args.human_skill, p_dropout=args.human_dropout, seed=args.seed + 2,
    )
    gate = VoIGate(model, env.hazard, env.hazard_radius,
                   horizon=args.horizon, c_query=args.c_query, tau=args.tau)

    successes = failures = queries = engagements = 0
    tp = fp = fn = 0
    rng = np.random.default_rng(args.seed + 3)

    obs = env.reset()
    alive_prev = env.alive.copy()
    timer = np.zeros(env.n, dtype=int)   # remaining human-control steps (takeover latch)
    done_all = False
    while not done_all:
        s = obs
        act = policy(s)

        ongoing = (timer > 0) & env.alive
        new_fire = np.zeros(env.n, dtype=bool)
        # only envs not already under takeover are candidates for a NEW engagement
        free = env.alive & (~ongoing)

        if strategy in ("voi", "random") and model is not None:
            cand, score, _ = gate.candidates(s, policy)
            cand = cand & free
            if strategy == "voi":
                chosen = allocate_topk(score, cand, args.budget)
            else:
                chosen = allocate_random(score, cand, args.budget, rng)
            new_fire[chosen] = True
        elif strategy == "always":
            new_fire = free.copy()

        # trigger calibration: NEW decisions vs eval-only ground-truth lookahead
        if strategy in ("voi", "random"):
            truth = true_lookahead_failure(env, s, policy, args.horizon) & free
            tp += int(np.sum(new_fire & truth))
            fp += int(np.sum(new_fire & (~truth)))
            fn += int(np.sum((~new_fire) & truth))

        timer[new_fire] = args.takeover_len
        engagements += int(new_fire.sum())
        fire = (ongoing | new_fire) & env.alive

        if fire.any():
            h_act = human.act(s)
            act = np.where(fire[:, None], h_act, act)
            queries += int(fire.sum())
        timer = np.clip(timer - 1, 0, None)

        # learn the dynamics online from real transitions
        prev_s = s.copy()
        obs, rew, done, info = env.step(act)
        if model is not None:
            alive_mask = alive_prev
            if alive_mask.any():
                model.add(prev_s[alive_mask], act[alive_mask], obs[alive_mask])

        successes += int(np.sum(info["success"]))
        failures += int(np.sum(info["failure"]))
        alive_prev = env.alive.copy()
        done_all = bool(np.all(done))

    if model is not None:
        model.fit()

    n = env.n
    out = {
        "strategy": strategy,
        "success_rate": successes / n,
        "failure_rate": failures / n,
        "queries": queries,          # total human-control steps (cost)
        "engagements": engagements,  # NEW takeovers (budget-metered)
        "queries_per_env": queries / n,
    }
    if strategy in ("voi", "random"):
        prec = tp / (tp + fp) if (tp + fp) else float("nan")
        rec = tp / (tp + fn) if (tp + fn) else float("nan")
        out["trigger_precision"] = prec
        out["trigger_recall"] = rec
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--num_envs", type=int, default=128)
    p.add_argument("--episodes", type=int, default=5, help="warmup episodes to fit the model")
    p.add_argument("--max_steps", type=int, default=60)
    p.add_argument("--budget", type=int, default=8, help="NEW human takeovers per step shared across envs")
    p.add_argument("--takeover_len", type=int, default=8, help="steps the human escorts once engaged")
    p.add_argument("--horizon", type=int, default=8)
    p.add_argument("--tau", type=float, default=0.10)
    p.add_argument("--c_query", type=float, default=0.05)
    p.add_argument("--policy_noise", type=float, default=0.25)
    p.add_argument("--human_noise", type=float, default=0.0)
    p.add_argument("--human_delay", type=int, default=0)
    p.add_argument("--human_skill", type=float, default=1.0)
    p.add_argument("--human_dropout", type=float, default=0.0)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    # warm up a shared dynamics model with a few episodes of policy data
    model = EnsembleDynamics(VectorReachEnv.state_dim, VectorReachEnv.act_dim, seed=args.seed)
    warm = VectorReachEnv(num_envs=args.num_envs, max_steps=args.max_steps, seed=args.seed + 99)
    wp = WeakReachPolicy(warm.goal, noise=0.5, seed=args.seed + 100)
    for _ in range(args.episodes):
        o = warm.reset()
        alive = warm.alive.copy()
        d = False
        while not d:
            a = wp(o)
            ps = o.copy()
            o, r, dn, _ = warm.step(a)
            if alive.any():
                model.add(ps[alive], a[alive], o[alive])
            alive = warm.alive.copy()
            d = bool(np.all(dn))
    model.fit()
    print(f"[model] fitted on warmup data; members={model.k}")

    print("\n=== FORESIGHT-HIL demo ===")
    print(f"num_envs={args.num_envs}  budget/step={args.budget}  horizon={args.horizon}  "
          f"human(noise={args.human_noise}, delay={args.human_delay}, skill={args.human_skill})\n")

    header = (f"{'strategy':>8} | {'success':>7} | {'failure':>7} | {'engage':>6} | "
              f"{'humanstep':>9} | {'prec':>5} | {'rec':>5}")
    print(header)
    print("-" * len(header))
    for strat in ["none", "always", "random", "voi"]:
        r = run_strategy(strat, args, model=model)
        prec = r.get("trigger_precision", float("nan"))
        rec = r.get("trigger_recall", float("nan"))
        print(f"{r['strategy']:>8} | {r['success_rate']*100:6.1f}% | {r['failure_rate']*100:6.1f}% | "
              f"{r['engagements']:6d} | {r['queries']:9d} | {prec:5.2f} | {rec:5.2f}")

    print("\nReading: 'voi' should match 'always'-level success at a fraction of the queries,")
    print("and beat 'random' at equal budget, with higher trigger precision/recall.")


if __name__ == "__main__":
    main()
