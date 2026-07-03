"""Phase-2 driver: full strategy comparison for FORESIGHT-HIL on robosuite Lift.

Runs the 4 intervention strategies (none / always / random / voi) across several
seeds, with the fixed env (no terminate-on-success) and budget pacing on the
budgeted strategies. `always` is deliberately budget-unaware and should be read
as an oracle-data stress test, not as an autonomous-policy upper bound. Results go to
`results/full/` and the run is *resumable*: any matching config whose per-run CSV
already exists is skipped, so the batch can be interrupted and restarted. The
driver includes key hyperparameters in the run label; otherwise different BC or
training configurations would silently collide on the same filename.

Order is seed-major (all 4 strategies for seed 0, then seed 1, ...) so a complete
comparison exists as early as possible.

Usage:
    python scripts/run_comparison.py                     # seeds 0,1,2
    python scripts/run_comparison.py --seeds 0           # just seed 0
    python scripts/run_comparison.py --total_steps 50000 # shorter
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

TRAIN = os.path.join(os.path.dirname(__file__), "train_robosuite_hil.py")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foresight_hil.experiments.strategy_specs import (
    DEFAULT_COMPARISON_STRATEGIES,
    build_driver_run_label,
    build_training_cli_args,
    comparison_run_identity,
)


def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--task", type=str, default="Lift")
    p.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    p.add_argument("--strategies", type=str, nargs="+",
                   default=list(DEFAULT_COMPARISON_STRATEGIES))
    p.add_argument("--budget", type=int, default=4000)
    p.add_argument("--total_steps", type=int, default=150000)
    p.add_argument("--n_demos", type=int, default=20)
    p.add_argument("--learning_starts", type=int, default=1000)
    p.add_argument("--batch_size", type=int, default=256)
    p.add_argument("--gradient_steps", type=int, default=1)
    p.add_argument("--intervention_demo_mode", type=str, default="all",
                   choices=["all", "starts", "none"])
    p.add_argument("--bc_pretrain_steps", type=int, default=0)
    p.add_argument("--bc_pretrain_batch_size", type=int, default=256)
    p.add_argument("--bc_actor_reg_coef", type=float, default=0.0)
    p.add_argument("--bc_actor_reg_every", type=int, default=1)
    p.add_argument("--bc_actor_reg_schedule", type=str, default="constant",
                   choices=["constant", "linear_late"])
    p.add_argument("--bc_actor_reg_late_coef", type=float, default=None)
    p.add_argument("--bc_actor_reg_late_start_frac", type=float, default=0.5)
    p.add_argument("--takeover_len", type=int, default=10)
    p.add_argument("--voi_tau", type=float, default=0.1)
    p.add_argument("--voi_cquery", type=float, default=0.05)
    p.add_argument("--voi_reference_policy", type=str, default="none",
                   choices=["none", "demo_nn"])
    p.add_argument("--voi_reference_max_points", type=int, default=2048)
    p.add_argument("--voi_learning_value_scale", type=float, default=0.0)
    p.add_argument("--voi_learning_value_clip", type=float, default=1.0)
    p.add_argument("--voi_learning_value_min_disagreement", type=float, default=0.0)
    p.add_argument("--voi_score_floor_after_step", type=int, default=0)
    p.add_argument("--voi_score_floor_after_value", type=float, default=0.0)
    p.add_argument("--voi_phase_guard", type=str, default="none",
                   choices=["none", "stack_pick_place"])
    p.add_argument("--eval_at_start", action="store_true")
    p.add_argument("--restore_best_model_at_end", action="store_true")
    p.add_argument("--trace_interventions", action="store_true")
    p.add_argument("--trace_candidates", action="store_true")
    p.add_argument("--force", action="store_true",
                   help="rerun even if the matching per-run CSV already exists")
    p.add_argument("--eval_every", type=int, default=10000)
    p.add_argument("--eval_episodes", type=int, default=20)
    p.add_argument("--out_dir", type=str, default="results/full")
    return p


def main():
    args = build_parser().parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    t0 = time.time()
    jobs = [(seed, strat) for seed in args.seeds for strat in args.strategies]
    print(f"[driver] {len(jobs)} runs queued -> {args.out_dir}")

    for i, (seed, strat) in enumerate(jobs, 1):
        run_label, run_tag = comparison_run_identity(args, seed, strat)
        run_csv = os.path.join(args.out_dir, f"run_{run_tag}.csv")
        if os.path.exists(run_csv) and not args.force:
            print(f"[driver] ({i}/{len(jobs)}) SKIP existing {run_tag}")
            continue

        cmd = [
            sys.executable, "-u", TRAIN,
            *build_training_cli_args(args, seed, strat, run_label),
        ]

        print(f"\n[driver] ({i}/{len(jobs)}) START {run_tag} "
              f"(elapsed {time.time()-t0:.0f}s)\n        {' '.join(cmd)}", flush=True)
        rc = subprocess.run(cmd).returncode
        status = "OK" if rc == 0 else f"FAILED(rc={rc})"
        print(f"[driver] ({i}/{len(jobs)}) {status} {run_tag}", flush=True)

    print(f"\n[driver] done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
