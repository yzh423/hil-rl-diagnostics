"""FORESIGHT-HIL on a REAL simulated robot (robosuite/MuJoCo) -- HIL-SERL-*style*.

HONESTY / SCOPE NOTE
--------------------
This is an HIL-SERL-*style* SIM baseline with a SCRIPTED-ORACLE "human", NOT an
exact reproduction of the HIL-SERL real-robot system or its numbers. The off-
policy actor is SAC (stable-baselines3) trained RLPD-style with a 50/50
demo+online replay mix; a scripted privileged-state oracle can intervene, and
intervention transitions are added to BOTH the demo and the RL buffers (as in
HIL-SERL). FORESIGHT-HIL contributes WHO/WHEN intervention happens: a model-based
Value-of-Information trigger (`VoIGate` + `EnsembleDynamics`) under a query
budget. We compare intervention strategies: none / always / random@budget /
voi@budget.

`always` is intentionally retained as a stress test for "all data are oracle
actions"; it is not treated as an upper bound on autonomous-policy evaluation,
because the evaluated policy must act without the oracle at test time.

Example (short smoke run):
    python scripts/train_robosuite_hil.py --task Lift --strategy voi \
        --budget 300 --total_steps 1500 --n_demos 5 --learning_starts 200 \
        --eval_every 750 --eval_episodes 3 --seed 0

Full run (documented, not executed here):
    python scripts/train_robosuite_hil.py --task Lift --strategy voi \
        --budget 4000 --total_steps 150000 --n_demos 20 --learning_starts 1000 \
        --eval_every 5000 --eval_episodes 20 --seed 0
"""

from __future__ import annotations

import os

# Windows fix: torch and mujoco each ship an OpenMP runtime (libiomp5md.dll vs
# libomp140.x86_64.dll); loading both aborts with "OMP: Error #15". Allowing the
# duplicate is the documented workaround and is safe for our single-process use.
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import argparse
import sys
import csv
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foresight_hil.envs.robosuite_env import make_env
from foresight_hil.oracle.robosuite_oracle import ScriptedLiftOracle
from foresight_hil.gating.reference_policy import (
    DemoNearestActionPolicy,
    demo_arrays_from_mixed_buffer,
)
from foresight_hil.gating.voi_gate import VoIGate
from foresight_hil.hil.mixed_replay_buffer import MixedReplayBuffer
from foresight_hil.hil.intervention import InterventionController
from foresight_hil.metrics import wilson_interval
from foresight_hil.experiments.bookkeeping import (
    best_eval_cost_metadata,
    build_run_tag,
    choose_reported_final_eval,
    effective_bc_actor_reg_coef,
    maybe_save_best_checkpoint,
    should_add_intervention_demo,
    write_summary_row,
)
from foresight_hil.experiments.trace import (
    CANDIDATE_TRACE_FIELDS,
    INTERVENTION_TRACE_FIELDS,
    candidate_trace_row,
    intervention_trace_row,
)


def stack_phase_guard_allows(priv, mode="none"):
    """Task-phase guard for Stack intervention starts.

    The guard keeps the learned actor responsible for easy long-range approach
    states and allows human starts near the contact-sensitive pick/place windows.
    It is a simulated phase classifier over object geometry; the default mode
    is `none`, which preserves the original ungated behavior.
    """
    mode = str(mode)
    if mode == "none":
        return True
    if mode != "stack_pick_place":
        raise ValueError(f"unknown phase guard mode: {mode}")
    if str(priv.get("task", "")).lower() != "stack":
        return True
    if "cubeA_pos" not in priv or "cubeB_pos" not in priv:
        return True

    eef = np.asarray(priv.get("eef_pos", np.zeros(3)), dtype=np.float64)
    cube_a = np.asarray(priv["cubeA_pos"], dtype=np.float64)
    cube_b = np.asarray(priv["cubeB_pos"], dtype=np.float64)
    d_xy_a = float(np.linalg.norm(eef[:2] - cube_a[:2]))
    d_xy_b = float(np.linalg.norm(eef[:2] - cube_b[:2]))
    dz_above_a = abs(float(eef[2] - (cube_a[2] + 0.07)))
    cube_a_lifted = bool(cube_a[2] > cube_b[2] + 0.055)

    pick_window = (not cube_a_lifted) and d_xy_a < 0.08 and dz_above_a < 0.12
    place_window = cube_a_lifted and d_xy_b < 0.15
    return bool(pick_window or place_window)


class PhaseFilteredGate:
    """Thin wrapper that masks gate candidates without changing scores/logging."""

    def __init__(self, gate, allow_fn):
        self._gate = gate
        self._allow_fn = allow_fn

    def __getattr__(self, name):
        return getattr(self._gate, name)

    def candidates(self, states, policy):
        cand, score, p_fail = self._gate.candidates(states, policy)
        if not bool(self._allow_fn()):
            cand = np.zeros_like(np.asarray(cand), dtype=bool)
        return cand, score, p_fail


def build_dynamics(state_dim, act_dim, kind, seed, n_members,
                   value_aware=False, value_aware_coef=0.5):
    """Torch MLP ensemble for high-dim robosuite state; numpy linear fallback.

    `value_aware`/`value_aware_coef` are OPTIONAL (M1) and only affect the torch
    ensemble; the numpy linear fallback ignores them (pure MLE), preserving the
    original default behavior.
    """
    if kind == "linear":
        from foresight_hil.models.ensemble_dynamics import EnsembleDynamics
        return EnsembleDynamics(state_dim, act_dim, n_members=n_members, seed=seed)
    try:
        from foresight_hil.models.torch_ensemble import TorchEnsembleDynamics
        return TorchEnsembleDynamics(
            state_dim, act_dim, n_members=n_members, seed=seed,
            value_aware=value_aware, value_aware_coef=value_aware_coef)
    except Exception as e:
        print(f"[dyn] torch ensemble unavailable ({e}); using linear numpy ensemble.")
        from foresight_hil.models.ensemble_dynamics import EnsembleDynamics
        return EnsembleDynamics(state_dim, act_dim, n_members=n_members, seed=seed)


def make_critic_value_fn(model):
    """M1 helper: build V(s)=min_i Q_i(s, pi(s)) from a trained SB3 SAC model.

    The policy action is detached (treated as fixed) so gradients flow only
    through the critic w.r.t. the predicted next state. Returns None if the
    SAC internals are not available, in which case M1 silently falls back to MLE.
    """
    try:
        import torch
    except Exception:
        return None

    def value_fn(states):
        st = states.to(model.device).float()
        with torch.no_grad():
            actions = model.actor(st)
            if isinstance(actions, (tuple, list)):
                actions = actions[0]
        qs = model.critic(st, actions)
        if isinstance(qs, (tuple, list)):
            q = torch.min(torch.stack(list(qs), dim=0), dim=0).values
        else:
            q = qs
        return q.reshape(-1)

    return value_fn


def make_np_value_fn(model):
    """N1 helper: numpy V(s)=min_i Q_i(s, pi(s)) for the value-based VoI gate.

    Takes a numpy (b, sdim) batch and returns a numpy (b,) value estimate using
    the SAC actor+critic. Returns None if torch / SAC internals are unavailable
    (the gate then falls back to the geometry-heuristic risk mode).
    """
    try:
        import torch
    except Exception:
        return None

    def np_value_fn(states_np):
        st = torch.as_tensor(np.atleast_2d(states_np).astype(np.float32),
                             device=model.device)
        with torch.no_grad():
            try:
                a = model.actor(st, deterministic=True)
            except TypeError:
                a = model.actor(st)
            if isinstance(a, (tuple, list)):
                a = a[0]
            qs = model.critic(st, a)
            if isinstance(qs, (tuple, list)):
                q = torch.min(torch.stack(list(qs), dim=0), dim=0).values
            else:
                q = qs
        return q.reshape(-1).cpu().numpy()

    return np_value_fn


def _dyn_probe(dyn, n=256):
    """Sample a normalized (s,a) input batch from the torch ensemble buffer.

    Used as ReDo probe input; returns None for the linear ensemble or before fit.
    """
    if getattr(dyn, "_x_mu", None) is None or not getattr(dyn, "_S", None):
        return None
    S = np.concatenate(dyn._S, 0)
    A = np.concatenate(dyn._A, 0)
    X = np.concatenate([S, A], axis=1)
    m = X.shape[0]
    idx = np.random.randint(0, m, size=min(n, m))
    return ((X[idx] - dyn._x_mu) / dyn._x_sd).astype(np.float32)


# ---- T1 targets: the SAC critic / actor (where the observed collapse lives) ----
def _sac_critic_modules(model):
    """(qnet, optimizer) pairs for each SAC Q-network (input = cat[obs, act])."""
    qnets = getattr(model.critic, "q_networks", None)
    opt = getattr(model.critic, "optimizer", None)
    if qnets is None:
        return []
    return [(qn, opt) for qn in qnets]


def _sac_actor_modules(model):
    """(latent_pi, optimizer) for the SAC actor trunk (input = obs)."""
    lat = getattr(model.actor, "latent_pi", None)
    opt = getattr(model.actor, "optimizer", None)
    return [(lat, opt)] if lat is not None else []


def _buffer_probe(mixed, kind, n=256):
    """ReDo probe sampled from the replay buffer.

    kind="critic" -> cat[obs, act] (matches a Q-network's input);
    kind="obs"    -> obs only (matches the actor trunk's input).
    """
    if mixed.size() < 2:
        return None
    batch = mixed.sample(min(n, mixed.size()))
    obs = batch.observations.detach().cpu().numpy().astype(np.float32)
    if kind == "critic":
        act = batch.actions.detach().cpu().numpy().astype(np.float32)
        return np.concatenate([obs, act], axis=1)
    return obs


def collect_demos(env, oracle, buffer, dyn, n_demos, verbose=True):
    """Run the scripted oracle to seed the demo buffer + warm the dynamics model."""
    succ = 0
    total_steps = 0
    for ep in range(n_demos):
        obs, _ = env.reset()
        oracle.reset()
        done = False
        steps = 0
        ever_success = False
        while not done and steps < env.horizon:
            a = oracle.act(env.privileged_state())
            nobs, r, term, trunc, info = env.step(a)
            buffer.add_demo(obs, nobs, a, r, float(term))
            dyn.add(obs, a, nobs)
            obs = nobs
            ever_success = ever_success or bool(info.get("is_success", False))
            done = term or trunc
            steps += 1
        succ += int(ever_success)
        total_steps += steps
    if verbose:
        print(f"[demos] {n_demos} oracle episodes | success {succ}/{n_demos} "
              f"| {total_steps} transitions | demo_buffer={buffer.demo_size()}")
    return succ, total_steps


def bc_actor_update(model, mixed, batch_size, coef=1.0):
    """One supervised actor update on the demo buffer; returns unscaled MSE."""
    demo_n = mixed.demo_size()
    if demo_n <= 0:
        return None

    import torch.nn.functional as F

    bs = max(1, min(int(batch_size), demo_n))
    batch = mixed.demo.sample(bs)
    pred = model.actor(batch.observations, deterministic=True)
    mse = F.mse_loss(pred, batch.actions)
    loss = float(coef) * mse
    model.actor.optimizer.zero_grad()
    loss.backward()
    model.actor.optimizer.step()
    return float(mse.detach().cpu().item())


def pretrain_actor_bc(model, mixed, steps, batch_size):
    """Behavior-clone the SAC actor on successful oracle/demo transitions.

    RLPD-style replay makes demonstrations available to the critic, but it does
    not by itself ensure the *evaluated deterministic actor* can execute the
    successful demonstrations early in training. This optional warm-start is a
    lightweight imitation step on the demo buffer before online RL begins.
    """
    steps = int(steps)
    if steps <= 0:
        return None
    demo_n = mixed.demo_size()
    if demo_n <= 0:
        print("[bc] requested but demo buffer is empty; skipping.")
        return None

    last_loss = 0.0
    for _ in range(steps):
        last_loss = bc_actor_update(model, mixed, batch_size, coef=1.0)

    bs = max(1, min(int(batch_size), demo_n))
    print(f"[bc] actor warm-start steps={steps} batch={bs} final_mse={last_loss:.6f}")
    return last_loss


def evaluate(env, model, n_episodes):
    succ, rets = 0, []
    for _ in range(n_episodes):
        obs, _ = env.reset()
        done = False
        ep_ret = 0.0
        steps = 0
        ever_success = False
        while not done and steps < env.horizon:
            a, _ = model.predict(obs, deterministic=True)
            obs, r, term, trunc, info = env.step(a)
            ep_ret += r
            ever_success = ever_success or bool(info.get("is_success", False))
            done = term or trunc
            steps += 1
        succ += int(ever_success)
        rets.append(ep_ret)
    n = max(1, int(n_episodes))
    rate = succ / n
    ci_low, ci_high = wilson_interval(succ, n)
    return rate, float(np.mean(rets)), succ, n, ci_low, ci_high


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--task", type=str, default="Lift")
    p.add_argument("--strategy", type=str, default="voi",
                   choices=["none", "always", "random", "voi"])
    p.add_argument("--budget", type=int, default=4000,
                   help="total human-control steps allowed across the run")
    p.add_argument("--total_steps", type=int, default=150000)
    p.add_argument("--n_demos", type=int, default=20)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--horizon", type=int, default=200)
    # human imperfection knobs
    p.add_argument("--human_noise", type=float, default=0.0)
    p.add_argument("--human_delay", type=int, default=0)
    p.add_argument("--human_skill", type=float, default=1.0)
    p.add_argument("--human_dropout", type=float, default=0.0)
    p.add_argument("--takeover_len", type=int, default=10)
    # budget pacing (spreads interventions across the run; ceiling, not a quota)
    p.add_argument("--pace", type=str, default="none", choices=["none", "linear"],
                   help="linear: cap cumulative human spend to budget*(t/total_steps)")
    p.add_argument("--pace_warmup", type=float, default=0.05,
                   help="fraction of budget available at t=0 under --pace linear")
    # SAC / RLPD
    p.add_argument("--learning_starts", type=int, default=1000)
    p.add_argument("--batch_size", type=int, default=256)
    p.add_argument("--gradient_steps", type=int, default=1)
    p.add_argument("--demo_frac", type=float, default=0.5)
    p.add_argument("--buffer_size", type=int, default=300000)
    p.add_argument("--intervention_demo_mode", type=str, default="all",
                   choices=["all", "starts", "none"],
                   help=("which intervention transitions enter the demo replay "
                         "used by BC regularization: all takeover steps "
                         "(default), only engagement starts, or none"))
    p.add_argument("--bc_pretrain_steps", type=int, default=0,
                   help="optional actor behavior-cloning warm-start on oracle/demo transitions")
    p.add_argument("--bc_pretrain_batch_size", type=int, default=256,
                   help="batch size for --bc_pretrain_steps; capped by demo buffer size")
    p.add_argument("--bc_actor_reg_coef", type=float, default=0.0,
                   help="optional online actor BC regularization coefficient during SAC updates")
    p.add_argument("--bc_actor_reg_every", type=int, default=1,
                   help="apply actor BC regularization every N env steps when enabled")
    p.add_argument("--bc_actor_reg_schedule", type=str, default="constant",
                   choices=["constant", "linear_late"],
                   help="anti-collapse actor BC schedule; linear_late ramps toward "
                        "--bc_actor_reg_late_coef after --bc_actor_reg_late_start_frac")
    p.add_argument("--bc_actor_reg_late_coef", type=float, default=None,
                   help="target actor BC regularization coefficient for linear_late")
    p.add_argument("--bc_actor_reg_late_start_frac", type=float, default=0.5,
                   help="fraction of training after which linear_late starts ramping")
    # dynamics / VoI
    p.add_argument("--dyn_kind", type=str, default="torch", choices=["torch", "linear"])
    p.add_argument("--dyn_members", type=int, default=5)
    p.add_argument("--dyn_epochs", type=int, default=40)
    p.add_argument("--dyn_refit_every", type=int, default=4000)
    p.add_argument("--voi_horizon", type=int, default=5)
    p.add_argument("--voi_tau", type=float, default=0.10)
    p.add_argument("--voi_cquery", type=float, default=0.05)
    p.add_argument("--risk_thresh", type=float, default=0.10,
                   help="Lift risk proxy: predicted gripper->cube dist (m) above which a state is 'risky'")
    # N1: decision-theoretic (EVSI) value-based trigger vs the geometry heuristic
    p.add_argument("--voi_mode", type=str, default="value", choices=["value", "risk"],
                   help="value: decision-theoretic EVSI VoI from the critic+world model (N1, default); "
                        "risk: hand-crafted gripper->cube distance heuristic (ablation baseline)")
    p.add_argument("--voi_unc_scale", type=float, default=5.0,
                   help="psi() up-weighting scale for value-uncertainty (value mode; CV-scaled)")
    p.add_argument("--voi_value_scale_floor", type=float, default=1.0,
                   help="value-mode VoI denominator floor; prevents near-zero early critics "
                        "from exploding relative decline scores")
    p.add_argument("--voi_score_clip", type=float, default=10.0,
                   help="absolute clip for value-mode VoI scores; <=0 disables clipping")
    p.add_argument("--voi_reference_policy", type=str, default="none",
                   choices=["none", "demo_nn"],
                   help=("reference action source for learning-value gating; "
                         "'demo_nn' uses nearest demonstration action"))
    p.add_argument("--voi_reference_max_points", type=int, default=2048,
                   help="maximum demo points used by the nearest-neighbor reference policy")
    p.add_argument("--voi_learning_value_scale", type=float, default=0.0,
                   help="multiplier strength for policy-reference action disagreement")
    p.add_argument("--voi_learning_value_clip", type=float, default=1.0,
                   help="clip normalized policy-reference action disagreement; <=0 disables")
    p.add_argument("--voi_learning_value_min_disagreement", type=float, default=0.0,
                   help=("minimum normalized policy-reference action disagreement "
                         "required for learning-value VoI to start an intervention; "
                         "0 disables the filter"))
    p.add_argument("--voi_score_floor_after_step", type=int, default=0,
                   help=("R024 diagnostic gate: after this training step, a VoI "
                         "candidate must have score >= --voi_score_floor_after_value "
                         "to start a takeover. Only active when the value is >0."))
    p.add_argument("--voi_score_floor_after_value", type=float, default=0.0,
                   help=("R024 diagnostic gate score floor for mid/late VoI starts; "
                         "0 disables and preserves the original trigger."))
    p.add_argument("--voi_phase_guard", type=str, default="none",
                   choices=["none", "stack_pick_place"],
                   help=("optional task-phase mask on VoI intervention starts; "
                         "stack_pick_place only allows starts near Stack pick/place windows"))
    # --- M1: decision-aware / value-equivalent dynamics (OPTIONAL, default OFF) ---
    p.add_argument("--dyn_value_aware", action="store_true",
                   help="M1: add an IterVAML-style value-equivalent term to the "
                        "dynamics loss (V from the SAC critic). Default OFF.")
    p.add_argument("--dyn_value_aware_coef", type=float, default=0.5,
                   help="M1: beta in [0,1] mixing value-equivalent vs MLE term.")
    # --- T1: plasticity preservation (OPTIONAL, default OFF) ---
    p.add_argument("--plasticity", action="store_true",
                   help="T1: periodically reset dormant/stale units of the dynamics "
                        "ensemble to counter primacy bias. Default OFF.")
    p.add_argument("--plasticity_method", type=str, default="redo",
                   choices=["redo", "perturb"])
    p.add_argument("--plasticity_target", type=str, default="critic",
                   choices=["critic", "actor", "both", "dynamics"],
                   help="T1: which network to keep plastic. 'critic' (default) targets the "
                        "SAC Q-networks where the observed success-collapse originates; "
                        "'dynamics' resets the world-model ensemble (original behavior).")
    p.add_argument("--plasticity_every", type=int, default=0,
                   help="T1: step period between resets (0 disables even if --plasticity).")
    p.add_argument("--plasticity_tau", type=float, default=0.0,
                   help="T1: ReDo dormancy threshold (normalized activation).")
    p.add_argument("--plasticity_frac", type=float, default=0.1,
                   help="T1: shrink-and-perturb fraction for --plasticity_method perturb.")
    # --- M2: trigger calibration logging (OPTIONAL, default OFF) ---
    p.add_argument("--calibrate", action="store_true",
                   help="M2: log a reliability diagram + ECE for the failure trigger. Default OFF.")
    p.add_argument("--calib_bins", type=int, default=10)
    # eval / logging
    p.add_argument("--eval_every", type=int, default=5000)
    p.add_argument("--eval_episodes", type=int, default=20)
    p.add_argument("--eval_at_start", action="store_true",
                   help="evaluate the autonomous actor after demos/BC before online RL")
    p.add_argument("--run_label", type=str, default="",
                   help="optional suffix for per-run CSV and summary identity")
    p.add_argument("--auto_run_label", action="store_true",
                   help="append a compact hyperparameter label to the run tag")
    p.add_argument("--no_save_best_model", action="store_false",
                   dest="save_best_model", default=True,
                   help="disable writing checkpoints/best_<run_tag>.zip on eval improvement")
    p.add_argument("--restore_best_model_at_end", action="store_true",
                   help=("reload the saved best checkpoint after training and use its "
                         "fresh evaluation as final_success_rate; raw final policy "
                         "metrics are still stored separately"))
    p.add_argument("--trace_interventions", action="store_true",
                   help=("write one diagnostic CSV row per intervention start; "
                         "for offline analysis only, not used by the policy"))
    p.add_argument("--trace_path", type=str, default="",
                   help="optional path for --trace_interventions CSV")
    p.add_argument("--trace_candidates", action="store_true",
                   help=("write one diagnostic CSV row per VoI gate evaluation, "
                         "including rejected candidate states; offline analysis only"))
    p.add_argument("--candidate_trace_path", type=str, default="",
                   help="optional path for --trace_candidates CSV")
    p.add_argument("--out_dir", type=str, default="results")
    args = p.parse_args()

    np.random.seed(args.seed)
    t_start = time.time()
    if args.eval_episodes < 20:
        print(f"[warn] eval_episodes={args.eval_episodes}; low-N success rates are noisy. "
              "Use >=20 for paper claims.")

    # ---- env + oracle ----
    env, backend = make_env(args.task, seed=args.seed, horizon=args.horizon)
    eval_env, _ = make_env(args.task, seed=args.seed + 777, horizon=args.horizon)
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]
    print(f"[env] task={args.task} backend={backend} obs_dim={obs_dim} act_dim={act_dim}")

    oracle = ScriptedLiftOracle(
        action_dim=act_dim, noise_std=args.human_noise, delay=args.human_delay,
        skill=args.human_skill, p_dropout=args.human_dropout, seed=args.seed + 2,
        task=args.task,
    )

    # ---- SAC actor (stable-baselines3) ----
    from stable_baselines3 import SAC
    model = SAC(
        "MlpPolicy", env, verbose=0, seed=args.seed,
        learning_starts=args.learning_starts, batch_size=args.batch_size,
        gradient_steps=args.gradient_steps, buffer_size=args.buffer_size,
        device="auto",
    )
    # RLPD-style mixed demo/online buffer (HIL-SERL backbone)
    mixed = MixedReplayBuffer(args.buffer_size, env.observation_space,
                              env.action_space, device=model.device,
                              demo_frac=args.demo_frac)
    model.replay_buffer = mixed
    model._setup_learn(total_timesteps=args.total_steps)  # init logger / counters
    print(f"[sac] device={model.device}")

    def policy_fn(states):
        states = np.atleast_2d(states).astype(np.float32)
        acts, _ = model.predict(states, deterministic=True)
        return np.atleast_2d(acts)

    # ---- dynamics model + VoI gate ----
    dyn = build_dynamics(obs_dim, act_dim, args.dyn_kind, args.seed, args.dyn_members,
                         value_aware=args.dyn_value_aware,
                         value_aware_coef=args.dyn_value_aware_coef)
    if args.dyn_value_aware:
        # M1: attach the SAC critic as the value function for the value-aware loss.
        vfn = make_critic_value_fn(model)
        if vfn is not None and hasattr(dyn, "set_value_fn"):
            dyn.set_value_fn(vfn)
            print(f"[M1] value-aware dynamics ON (beta={args.dyn_value_aware_coef})")
        else:
            print("[M1] value-aware requested but unavailable; falling back to MLE.")
    g2c_slice = env.gripper_to_cube_slice()

    def risk_fn(states):
        if g2c_slice is None:
            return np.zeros(states.shape[0], dtype=bool)
        d = np.linalg.norm(states[:, g2c_slice], axis=1)
        return d > args.risk_thresh

    np_value_fn = make_np_value_fn(model)
    gate = VoIGate(dyn, horizon=args.voi_horizon, c_query=args.voi_cquery,
                   tau=args.voi_tau, risk_fn=risk_fn, value_fn=np_value_fn,
                   mode=args.voi_mode, unc_scale=args.voi_unc_scale,
                   value_scale_floor=args.voi_value_scale_floor,
                   score_clip=args.voi_score_clip,
                   learning_value_scale=args.voi_learning_value_scale,
                   learning_value_clip=args.voi_learning_value_clip,
                   learning_value_min_disagreement=(
                       args.voi_learning_value_min_disagreement))
    print(f"[voi] trigger mode={gate.mode} (H={args.voi_horizon} tau={args.voi_tau} "
          f"c_query={args.voi_cquery} unc_scale={args.voi_unc_scale} "
          f"value_floor={args.voi_value_scale_floor} score_clip={args.voi_score_clip} "
          f"vref={args.voi_reference_policy} lv_scale={args.voi_learning_value_scale} "
          f"lv_min_disagree={args.voi_learning_value_min_disagreement} "
          f"score_floor_after=({args.voi_score_floor_after_step}, "
          f"{args.voi_score_floor_after_value}))")
    if args.voi_phase_guard != "none":
        gate = PhaseFilteredGate(
            gate,
            lambda: stack_phase_guard_allows(env.privileged_state(), args.voi_phase_guard),
        )
        print(f"[voi] phase guard ON mode={args.voi_phase_guard}")

    controller = InterventionController(
        args.strategy, gate=gate, budget=args.budget,
        total_steps=args.total_steps, takeover_len=args.takeover_len,
        seed=args.seed + 3, pace=args.pace, pace_warmup=args.pace_warmup,
        voi_score_floor_after_step=args.voi_score_floor_after_step,
        voi_score_floor_after_value=args.voi_score_floor_after_value,
    )

    # ---- collect demos + warm the dynamics model ----
    collect_demos(env, oracle, mixed, dyn, args.n_demos)
    if args.voi_reference_policy == "demo_nn":
        ref_obs, ref_actions = demo_arrays_from_mixed_buffer(
            mixed, max_points=args.voi_reference_max_points, seed=args.seed + 17)
        gate.set_reference_policy(DemoNearestActionPolicy(ref_obs, ref_actions))
        print(f"[voi] demo-nearest reference policy ON "
              f"(points={ref_obs.shape[0]} scale={args.voi_learning_value_scale})")
    bc_loss = pretrain_actor_bc(
        model, mixed, args.bc_pretrain_steps, args.bc_pretrain_batch_size)
    if dyn.fitted is False:
        print("[dyn] fitting dynamics model on demo data ...")
        try:
            dyn.fit(epochs=args.dyn_epochs)
        except TypeError:
            dyn.fit()
    print(f"[dyn] fitted={dyn.fitted} members={dyn.k}")

    # ---- T1: optional plasticity manager ----
    # Default target is the SAC CRITIC (q_networks): the observed end-of-training
    # success-collapse is policy/critic catastrophic forgetting, not dynamics-model
    # error, so resetting dormant critic units is what should cure it. 'dynamics'
    # keeps the original (world-model) behavior; 'both'/'actor' are also available.
    plasticity_mgr = None
    plast_kinds = []  # parallel to plasticity_mgr.modules: probe kind per module
    if args.plasticity and args.plasticity_every > 0:
        try:
            from foresight_hil.training.plasticity import PlasticityManager
            mods, kinds = [], []
            tgt = args.plasticity_target
            if tgt in ("critic", "both"):
                for m, opt in _sac_critic_modules(model):
                    mods.append((m, opt)); kinds.append("critic")
            if tgt in ("actor", "both"):
                for m, opt in _sac_actor_modules(model):
                    mods.append((m, opt)); kinds.append("obs")
            if tgt == "dynamics" and hasattr(dyn, "members"):
                for m, opt in zip(dyn.members, dyn.opts):
                    mods.append((m, opt)); kinds.append("dyn")
            if mods:
                plasticity_mgr = PlasticityManager(
                    [(m, opt, None) for (m, opt) in mods],
                    reset_every=args.plasticity_every,
                    method=args.plasticity_method, tau=args.plasticity_tau,
                    fraction=args.plasticity_frac, seed=args.seed + 5)
                plast_kinds = kinds
                print(f"[T1] plasticity ON target={tgt} method={args.plasticity_method} "
                      f"every={args.plasticity_every} tau={args.plasticity_tau} "
                      f"n_modules={len(mods)}")
            else:
                print(f"[T1] plasticity target={tgt} produced no modules; disabled.")
        except Exception as e:
            print(f"[T1] plasticity unavailable ({e}); continuing without it.")

    # ---- M2: optional trigger-calibration logger ----
    calib_logger = None
    calib_buf = []  # per-episode (p_fail) values pending an outcome label
    if args.calibrate:
        from foresight_hil.gating.calibration import TriggerCalibrationLogger
        calib_logger = TriggerCalibrationLogger(n_bins=args.calib_bins)
        print(f"[M2] trigger calibration logging ON (bins={args.calib_bins})")

    # ---- results logging ----
    os.makedirs(args.out_dir, exist_ok=True)
    run_tag, effective_run_label = build_run_tag(args)
    run_csv = os.path.join(args.out_dir, f"run_{run_tag}.csv")
    trace_csv = args.trace_path or os.path.join(args.out_dir, f"trace_{run_tag}.csv")
    candidate_trace_csv = (
        args.candidate_trace_path
        or os.path.join(args.out_dir, f"candidate_trace_{run_tag}.csv")
    )
    best_checkpoint_path = os.path.join(
        args.out_dir, "checkpoints", f"best_{run_tag}.zip")
    with open(run_csv, "w", newline="") as f:
        csv.writer(f).writerow(
            ["env_step", "eval_success_rate", "eval_return",
             "eval_successes", "eval_episodes", "eval_success_ci_low",
             "eval_success_ci_high", "human_steps", "budget_used_frac",
             "engagements", "demo_size", "online_size", "voi_candidate_rate",
             "voi_score_mean", "voi_p_fail_mean", "bc_reg_loss_mean"])
    if args.trace_interventions:
        with open(trace_csv, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=INTERVENTION_TRACE_FIELDS).writeheader()
        print(f"[trace] intervention starts -> {trace_csv}")
    if args.trace_candidates:
        with open(candidate_trace_csv, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=CANDIDATE_TRACE_FIELDS).writeheader()
        print(f"[trace] candidate gate states -> {candidate_trace_csv}")

    # ---- HIL training loop ----
    obs, _ = env.reset()
    oracle.reset()
    controller.reset_episode()
    ep_ret, ep_len, ep_idx = 0.0, 0, 0
    best_success = 0.0
    best_step = None
    best_cost = {"human_steps": "", "budget_used_frac": "", "engagements": ""}
    last_eval = {"success": 0.0, "return": 0.0, "successes": 0,
                 "episodes": args.eval_episodes, "ci_low": 0.0, "ci_high": 1.0}
    gate_window = {"steps": 0, "candidates": 0, "score_sum": 0.0,
                   "pfail_sum": 0.0, "score_n": 0,
                   "bc_loss_sum": 0.0, "bc_loss_n": 0}

    if args.eval_at_start:
        sr, ret, succ_n, eval_n, ci_low, ci_high = evaluate(
            eval_env, model, args.eval_episodes)
        prev_best_step = best_step
        best_success, best_step, saved_best = maybe_save_best_checkpoint(
            model, best_checkpoint_path, 0, sr, best_success, best_step,
            enabled=args.save_best_model)
        best_cost = best_eval_cost_metadata(
            prev_best_step, best_step, 0, controller.spent,
            controller.spent / max(1, args.budget), controller.engagements,
            best_cost)
        last_eval = {"success": sr, "return": ret, "successes": succ_n,
                     "episodes": eval_n, "ci_low": ci_low, "ci_high": ci_high}
        with open(run_csv, "a", newline="") as f:
            csv.writer(f).writerow(
                [0, f"{sr:.4f}", f"{ret:.4f}", succ_n, eval_n,
                 f"{ci_low:.4f}", f"{ci_high:.4f}", controller.spent,
                 f"{controller.spent / max(1, args.budget):.4f}",
                 controller.engagements, mixed.demo_size(), mixed.online_size(),
                 "nan", "nan", "nan", "nan"])
        print(f"[step {0:>7}] eval_success={sr*100:5.1f}% "
              f"({succ_n}/{eval_n}, CI {ci_low*100:4.1f}-{ci_high*100:4.1f}%) "
              f"return={ret:7.2f} post_demo_bc")
        if saved_best:
            print(f"[best] step=0 success={sr*100:.1f}% -> {best_checkpoint_path}")

    for step in range(1, args.total_steps + 1):
        # M2: record the trigger's predicted failure probability for this state;
        # it is labeled at episode end with the actual failure outcome.
        if calib_logger is not None and dyn.fitted:
            try:
                _, p_fail_now = gate.voi(np.atleast_2d(obs), policy_fn)
                calib_buf.append(float(np.asarray(p_fail_now).ravel()[0]))
            except Exception:
                pass

        # learner action (with exploration), maybe overridden by the oracle
        learner_a, _ = model.predict(obs, deterministic=False)
        intervened = controller.step(obs, policy_fn)
        if args.strategy == "voi":
            gate_window["steps"] += 1
            if controller.last_candidate:
                gate_window["candidates"] += 1
            if np.isfinite(controller.last_score):
                gate_window["score_sum"] += controller.last_score
                gate_window["pfail_sum"] += controller.last_p_fail
                gate_window["score_n"] += 1
        priv_now = None
        if intervened:
            priv_now = env.privileged_state()
            action = oracle.act(priv_now)
        else:
            action = learner_a
        if args.trace_candidates and controller.last_gate_evaluated:
            if priv_now is None:
                priv_now = env.privileged_state()
            with open(candidate_trace_csv, "a", newline="") as f:
                csv.DictWriter(f, fieldnames=CANDIDATE_TRACE_FIELDS).writerow(
                    candidate_trace_row(
                        step, ep_idx, ep_len, args, controller, priv_now))
        if args.trace_interventions and controller.last_started:
            if priv_now is None:
                priv_now = env.privileged_state()
            with open(trace_csv, "a", newline="") as f:
                csv.DictWriter(f, fieldnames=INTERVENTION_TRACE_FIELDS).writerow(
                    intervention_trace_row(
                        step, ep_idx, ep_len, args, controller, priv_now))

        nobs, r, term, trunc, info = env.step(action)
        done = term or trunc

        # store transition: always online; intervention transitions -> demo too
        mixed.add_online(obs, nobs, action, r, float(term))
        if should_add_intervention_demo(
                intervened, controller, args.intervention_demo_mode):
            mixed.add_demo(obs, nobs, action, r, float(term))
        dyn.add(obs, action, nobs)

        obs = nobs
        ep_ret += r
        ep_len += 1

        # SAC updates (after warmup)
        if step >= args.learning_starts and mixed.size() >= args.batch_size:
            model.train(gradient_steps=args.gradient_steps, batch_size=args.batch_size)
            if (args.bc_actor_reg_coef > 0
                    and step % max(1, args.bc_actor_reg_every) == 0):
                bc_coef = effective_bc_actor_reg_coef(
                    step, args.total_steps, args.bc_actor_reg_coef,
                    schedule=args.bc_actor_reg_schedule,
                    late_coef=args.bc_actor_reg_late_coef,
                    late_start_frac=args.bc_actor_reg_late_start_frac)
                bc_reg_loss = bc_actor_update(
                    model, mixed, args.bc_pretrain_batch_size,
                    coef=bc_coef)
                if bc_reg_loss is not None:
                    gate_window["bc_loss_sum"] += bc_reg_loss
                    gate_window["bc_loss_n"] += 1

        # periodic dynamics refit (keeps the VoI rollouts honest as data grows)
        if args.strategy == "voi" and step % args.dyn_refit_every == 0:
            try:
                dyn.fit(epochs=max(10, args.dyn_epochs // 2))
            except TypeError:
                dyn.fit()

        # T1: periodic plasticity intervention (default target = SAC critic)
        if plasticity_mgr is not None:
            if args.plasticity_method == "redo" and (step % args.plasticity_every == 0):
                # refresh each module's ReDo probe from current data before reset
                probe_cache = {}
                new_mods = []
                for (m, opt, _), kind in zip(plasticity_mgr.modules, plast_kinds):
                    if kind == "dyn":
                        probe = _dyn_probe(dyn)
                    else:
                        if kind not in probe_cache:
                            probe_cache[kind] = _buffer_probe(mixed, kind)
                        probe = probe_cache[kind]
                    new_mods.append((m, opt, probe))
                plasticity_mgr.modules = new_mods
            reset_n = plasticity_mgr.maybe_reset(step)
            if reset_n:
                print(f"[T1] step {step}: recycled {reset_n} dormant units "
                      f"(target={args.plasticity_target})")

        if done:
            # M2: label this episode's buffered trigger probabilities with the
            # actual outcome (failure = episode ended without success).
            if calib_logger is not None and calib_buf:
                failed = 0.0 if bool(info.get("is_success", False)) else 1.0
                calib_logger.record(np.asarray(calib_buf), failed)
                calib_buf = []
            ep_idx += 1
            obs, _ = env.reset()
            oracle.reset()
            controller.reset_episode()
            ep_ret, ep_len = 0.0, 0

        # periodic evaluation
        if step % args.eval_every == 0 or step == args.total_steps:
            sr, ret, succ_n, eval_n, ci_low, ci_high = evaluate(
                eval_env, model, args.eval_episodes)
            prev_best_step = best_step
            best_success, best_step, saved_best = maybe_save_best_checkpoint(
                model, best_checkpoint_path, step, sr, best_success, best_step,
                enabled=args.save_best_model)
            last_eval = {"success": sr, "return": ret, "successes": succ_n,
                         "episodes": eval_n, "ci_low": ci_low, "ci_high": ci_high}
            budget_used_frac = controller.spent / max(1, args.budget)
            best_cost = best_eval_cost_metadata(
                prev_best_step, best_step, step, controller.spent,
                budget_used_frac, controller.engagements, best_cost)
            candidate_rate = (
                gate_window["candidates"] / gate_window["steps"]
                if gate_window["steps"] else float("nan")
            )
            score_mean = (
                gate_window["score_sum"] / gate_window["score_n"]
                if gate_window["score_n"] else float("nan")
            )
            pfail_mean = (
                gate_window["pfail_sum"] / gate_window["score_n"]
                if gate_window["score_n"] else float("nan")
            )
            bc_loss_mean = (
                gate_window["bc_loss_sum"] / gate_window["bc_loss_n"]
                if gate_window["bc_loss_n"] else float("nan")
            )
            with open(run_csv, "a", newline="") as f:
                csv.writer(f).writerow(
                    [step, f"{sr:.4f}", f"{ret:.4f}", succ_n, eval_n,
                     f"{ci_low:.4f}", f"{ci_high:.4f}", controller.spent,
                     f"{budget_used_frac:.4f}", controller.engagements,
                     mixed.demo_size(), mixed.online_size(),
                     f"{candidate_rate:.4f}" if np.isfinite(candidate_rate) else "nan",
                     f"{score_mean:.4f}" if np.isfinite(score_mean) else "nan",
                     f"{pfail_mean:.4f}" if np.isfinite(pfail_mean) else "nan",
                     f"{bc_loss_mean:.6f}" if np.isfinite(bc_loss_mean) else "nan"])
            elapsed = time.time() - t_start
            gate_msg = ""
            if args.strategy == "voi":
                gate_msg = (f" cand_rate={candidate_rate:5.3f} "
                            f"score={score_mean:7.3f} p_fail={pfail_mean:5.3f}")
            if np.isfinite(bc_loss_mean):
                gate_msg += f" bc_mse={bc_loss_mean:.5f}"
            print(f"[step {step:>7}] eval_success={sr*100:5.1f}% "
                  f"({succ_n}/{eval_n}, CI {ci_low*100:4.1f}-{ci_high*100:4.1f}%) "
                  f"return={ret:7.2f} human_steps={controller.spent:>6} "
                  f"budget={budget_used_frac*100:5.1f}% engage={controller.engagements:>5}"
                  f"{gate_msg} ({elapsed:5.0f}s)")
            if saved_best:
                print(f"[best] step={step} success={sr*100:.1f}% -> {best_checkpoint_path}")
            gate_window = {"steps": 0, "candidates": 0, "score_sum": 0.0,
                           "pfail_sum": 0.0, "score_n": 0,
                           "bc_loss_sum": 0.0, "bc_loss_n": 0}

    raw_final_eval = dict(last_eval)
    restored_best_eval = None
    if args.restore_best_model_at_end:
        if not args.save_best_model:
            print("[restore_best] requested but best checkpoint saving is disabled; "
                  "reporting last policy.")
        elif best_step is None or not os.path.exists(best_checkpoint_path):
            print("[restore_best] requested but no best checkpoint exists; "
                  "reporting last policy.")
        else:
            from stable_baselines3 import SAC
            print(f"[restore_best] loading {best_checkpoint_path} from step {best_step}")
            model = SAC.load(best_checkpoint_path, env=env, device=model.device)
            sr, ret, succ_n, eval_n, ci_low, ci_high = evaluate(
                eval_env, model, args.eval_episodes)
            restored_best_eval = {
                "success": sr, "return": ret, "successes": succ_n,
                "episodes": eval_n, "ci_low": ci_low, "ci_high": ci_high,
            }
            print(f"[restore_best] eval_success={sr*100:5.1f}% "
                  f"({succ_n}/{eval_n}, CI {ci_low*100:4.1f}-{ci_high*100:4.1f}%) "
                  f"return={ret:7.2f}")
    last_eval, final_policy_source = choose_reported_final_eval(
        raw_final_eval, restored_best_eval)

    # ---- append cross-strategy summary row ----
    header = ["task", "backend", "strategy", "budget", "human_noise", "human_delay",
              "human_skill", "human_dropout", "seed", "total_steps", "n_demos",
              "run_label", "restore_best_model_at_end",
              "intervention_demo_mode",
              "voi_phase_guard",
              "voi_reference_policy", "voi_reference_max_points",
              "voi_learning_value_scale", "voi_learning_value_clip",
              "voi_learning_value_min_disagreement",
              "voi_score_floor_after_step", "voi_score_floor_after_value",
              "bc_pretrain_steps", "bc_final_mse",
              "bc_actor_reg_coef", "bc_actor_reg_schedule",
              "bc_actor_reg_late_coef", "bc_actor_reg_late_start_frac",
              "final_success_rate", "final_policy_source",
              "raw_final_success_rate", "raw_final_eval_successes",
              "raw_final_success_ci_low", "raw_final_success_ci_high",
              "restored_best_success_rate", "restored_best_eval_successes",
              "restored_best_success_ci_low", "restored_best_success_ci_high",
              "best_success_rate", "best_eval_step",
              "best_human_steps", "best_budget_used_frac", "best_engagements",
              "best_checkpoint_path", "human_steps",
              "budget_used_frac", "engagements", "final_eval_successes",
              "final_eval_episodes", "final_success_ci_low",
              "final_success_ci_high", "wall_time_s"]
    summary_csv = os.path.join(args.out_dir, "robosuite_hil_summary.csv")
    if os.path.exists(summary_csv):
        with open(summary_csv, newline="") as f:
            existing_header = next(csv.reader(f), [])
        if existing_header != header:
            summary_csv = os.path.join(args.out_dir, "robosuite_hil_summary_v2.csv")
            print(f"[warn] existing summary schema differs; writing new rows to {summary_csv}")
    summary_row = [
        args.task, backend, args.strategy, args.budget, args.human_noise,
        args.human_delay, args.human_skill, args.human_dropout, args.seed,
        args.total_steps, args.n_demos, effective_run_label,
        int(bool(args.restore_best_model_at_end)),
        args.intervention_demo_mode,
        args.voi_phase_guard,
        args.voi_reference_policy, args.voi_reference_max_points,
        args.voi_learning_value_scale, args.voi_learning_value_clip,
        args.voi_learning_value_min_disagreement,
        args.voi_score_floor_after_step, args.voi_score_floor_after_value,
        args.bc_pretrain_steps,
        "" if bc_loss is None else f"{bc_loss:.6f}",
        args.bc_actor_reg_coef, args.bc_actor_reg_schedule,
        "" if args.bc_actor_reg_late_coef is None else args.bc_actor_reg_late_coef,
        args.bc_actor_reg_late_start_frac,
        f"{last_eval['success']:.4f}",
        final_policy_source,
        f"{raw_final_eval['success']:.4f}",
        raw_final_eval["successes"],
        f"{raw_final_eval['ci_low']:.4f}",
        f"{raw_final_eval['ci_high']:.4f}",
        "" if restored_best_eval is None else f"{restored_best_eval['success']:.4f}",
        "" if restored_best_eval is None else restored_best_eval["successes"],
        "" if restored_best_eval is None else f"{restored_best_eval['ci_low']:.4f}",
        "" if restored_best_eval is None else f"{restored_best_eval['ci_high']:.4f}",
        f"{best_success:.4f}",
        "" if best_step is None else best_step,
        best_cost["human_steps"], best_cost["budget_used_frac"],
        best_cost["engagements"],
        best_checkpoint_path if args.save_best_model and best_step is not None else "",
        controller.spent,
        f"{controller.spent / max(1, args.budget):.4f}",
        controller.engagements,
        last_eval["successes"], last_eval["episodes"],
        f"{last_eval['ci_low']:.4f}", f"{last_eval['ci_high']:.4f}",
        f"{time.time() - t_start:.1f}",
    ]
    write_summary_row(summary_csv, header, summary_row)

    # ---- M2: dump trigger reliability diagram + ECE ----
    if calib_logger is not None and len(calib_logger) > 0:
        calib_csv = os.path.join(args.out_dir, f"calib_{run_tag}.csv")
        calib_logger.to_csv(calib_csv)
        s = calib_logger.summary()
        print(f"[M2] trigger calibration: n={s['n']} ECE={s['ece']:.4f} "
              f"MCE={s['mce']:.4f} Brier={s['brier']:.4f} -> {calib_csv}")

    print(f"\n[done] strategy={args.strategy} backend={backend} "
          f"final_success={last_eval['success']*100:.1f}% "
          f"source={final_policy_source} "
          f"({last_eval['successes']}/{last_eval['episodes']}, "
          f"CI {last_eval['ci_low']*100:.1f}-{last_eval['ci_high']*100:.1f}%) "
          f"raw_final={raw_final_eval['success']*100:.1f}% "
          f"({raw_final_eval['successes']}/{raw_final_eval['episodes']}) "
          f"best={best_success*100:.1f}%"
          f"{'' if best_step is None else f'@step{best_step}'} "
          f"human_steps={controller.spent} -> {run_csv}; summary={summary_csv}")
    env.close()
    eval_env.close()


if __name__ == "__main__":
    main()
    # On Windows, MuJoCo/robosuite + OpenMP teardown can hang at interpreter exit,
    # which blocks any parent driver waiting on this process. We have already
    # flushed all results to disk, so force an immediate, clean exit that skips the
    # hanging atexit/native cleanup.
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
