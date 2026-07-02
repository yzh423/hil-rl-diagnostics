"""Re-evaluate a saved SAC checkpoint with repeated evaluation batches.

This is for paper-facing checkpoint claims: a single 20-episode evaluation can
overstate a transient best checkpoint. The script reloads a saved policy, runs
several independent evaluation batches, and writes both per-repeat and aggregate
CSV files.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foresight_hil.envs.robosuite_env import make_env
from foresight_hil.evaluation.protocol import repeat_summary_row, summarize_repeats
from scripts.train_robosuite_hil import evaluate


def write_csv(path, rows, fieldnames):
    out_dir = os.path.dirname(path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--task", default="Lift")
    p.add_argument("--episodes", type=int, default=20)
    p.add_argument("--repeats", type=int, default=3)
    p.add_argument("--seed", type=int, default=777)
    p.add_argument("--horizon", type=int, default=200)
    p.add_argument("--device", default="auto")
    p.add_argument("--out_csv", required=True)
    p.add_argument("--summary_csv", default="")
    args = p.parse_args()

    from stable_baselines3 import SAC

    model = SAC.load(args.checkpoint, device=args.device)
    rows = []
    for repeat in range(args.repeats):
        env, backend = make_env(
            args.task, seed=args.seed + repeat, horizon=args.horizon)
        try:
            sr, ret, succ_n, eval_n, ci_low, ci_high = evaluate(
                env, model, args.episodes)
        finally:
            env.close()
        row = {
            "checkpoint": args.checkpoint,
            "task": args.task,
            "backend": backend,
            "repeat": repeat,
            "seed": args.seed + repeat,
            "success_rate": f"{sr:.4f}",
            "return_mean": f"{ret:.4f}",
            "successes": succ_n,
            "episodes": eval_n,
            "success_ci_low": f"{ci_low:.4f}",
            "success_ci_high": f"{ci_high:.4f}",
        }
        rows.append(row)
        print(f"[repeat {repeat}] success={sr*100:.1f}% "
              f"({succ_n}/{eval_n}, CI {ci_low*100:.1f}-{ci_high*100:.1f}%) "
              f"return={ret:.2f}")

    fieldnames = [
        "checkpoint", "task", "backend", "repeat", "seed", "success_rate",
        "return_mean", "successes", "episodes", "success_ci_low",
        "success_ci_high",
    ]
    write_csv(args.out_csv, rows, fieldnames)
    print(f"[csv] saved {args.out_csv}")

    summary = summarize_repeats(rows)
    summary_row = repeat_summary_row(args.checkpoint, args.task, summary)
    summary_csv = args.summary_csv or os.path.splitext(args.out_csv)[0] + "_summary.csv"
    write_csv(summary_csv, [summary_row], list(summary_row.keys()))
    print(f"[summary] success={summary['success_mean']*100:.1f}% "
          f"+/- {summary['success_std']*100:.1f}% over {summary['n_repeats']} repeats "
          f"({summary['total_successes']}/{summary['total_episodes']}, "
          f"CI {summary['success_ci_low']*100:.1f}-{summary['success_ci_high']*100:.1f}%)")
    print(f"[csv] saved {summary_csv}")


if __name__ == "__main__":
    main()
