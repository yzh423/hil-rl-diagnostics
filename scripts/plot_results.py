"""Aggregate FORESIGHT-HIL robosuite runs and plot success-vs-human-cost.

Reads a `robosuite_hil_summary*.csv` file written by `train_robosuite_hil.py`,
aggregates across seeds per strategy, prints a comparison table, and saves a
success-vs-human-cost plot. The loader accepts both the original summary schema
and the newer schema that adds confidence intervals and budget diagnostics.

Usage:
    python scripts/plot_results.py
    python scripts/plot_results.py --summary results/robosuite_hil_summary.csv \
        --metric best_success_rate --out results/success_vs_human_cost.png
"""

from __future__ import annotations

import argparse
import csv
import os
from collections import defaultdict

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SUPPORTED_SUCCESS_METRICS = [
    "best_success_rate",
    "final_success_rate",
    "raw_final_success_rate",
]


RESULT_FIELDS = {
    "bc_final_mse", "final_success_rate", "best_success_rate",
    "final_policy_source", "raw_final_success_rate",
    "raw_final_eval_successes", "raw_final_success_ci_low",
    "raw_final_success_ci_high", "restored_best_success_rate",
    "restored_best_eval_successes", "restored_best_success_ci_low",
    "restored_best_success_ci_high", "best_eval_step",
    "best_human_steps", "best_budget_used_frac", "best_engagements",
    "best_checkpoint_path", "human_steps", "budget_used_frac", "engagements",
    "final_eval_successes", "final_eval_episodes", "final_success_ci_low",
    "final_success_ci_high", "wall_time_s",
}


def load(summary):
    rows = []
    with open(summary, newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def dedupe_rows(rows):
    if not rows:
        return rows, 0
    key_fields = [k for k in rows[0].keys() if k not in RESULT_FIELDS]
    by_key = {}
    for r in rows:
        key = tuple((k, r.get(k, "")) for k in key_fields)
        by_key[key] = r
    deduped = list(by_key.values())
    return deduped, len(rows) - len(deduped)


def human_cost_for_metric(row, metric):
    if metric == "best_success_rate":
        best_cost = row.get("best_human_steps", "")
        if best_cost not in ("", None):
            return float(best_cost)
    return float(row["human_steps"])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--summary", type=str, default="results/robosuite_hil_summary.csv")
    p.add_argument("--metric", type=str, default="best_success_rate",
                   choices=SUPPORTED_SUCCESS_METRICS)
    p.add_argument("--out", type=str, default="results/success_vs_human_cost.png")
    p.add_argument("--out_csv", type=str, default="results/strategy_comparison.csv")
    args = p.parse_args()

    if not os.path.exists(args.summary):
        raise SystemExit(f"No summary file at {args.summary}; run train_robosuite_hil.py first.")

    rows = load(args.summary)
    if not rows:
        raise SystemExit(f"No rows in {args.summary}.")
    rows, n_dupes = dedupe_rows(rows)
    if n_dupes:
        print(f"[dedupe] ignored {n_dupes} repeated summary row(s) with identical config keys.")

    by_strat = defaultdict(lambda: {"succ": [], "cost": [], "engage": []})
    task = backend = "?"
    for r in rows:
        task, backend = r["task"], r["backend"]
        s = r["strategy"]
        by_strat[s]["succ"].append(float(r[args.metric]))
        by_strat[s]["cost"].append(human_cost_for_metric(r, args.metric))
        by_strat[s]["engage"].append(float(r["engagements"]))

    order = [s for s in ["none", "always", "random", "voi"] if s in by_strat]
    print(f"\n=== FORESIGHT-HIL robosuite ({task}, backend={backend}) - {args.metric} ===")
    print(f"{'strategy':>8} | {'success':>8} | {'human_steps':>11} | {'engage':>7} | {'n':>2}")
    print("-" * 50)

    agg = {}
    for s in order:
        succ = np.array(by_strat[s]["succ"])
        cost = np.array(by_strat[s]["cost"])
        eng = np.array(by_strat[s]["engage"])
        agg[s] = (succ.mean(), succ.std(), cost.mean(), eng.mean(), len(succ))
        print(f"{s:>8} | {succ.mean()*100:6.1f}%  | {cost.mean():11.0f} | "
              f"{eng.mean():7.0f} | {len(succ):2d}")

    if "always" in by_strat:
        print("[note] robosuite 'always' is an oracle-data stress test, not an "
              "autonomous-policy upper bound.")

    with open(args.out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["strategy", "success_mean", "success_std", "human_steps_mean",
                    "engagements_mean", "n_seeds"])
        for s in order:
            m, sd, c, e, n = agg[s]
            w.writerow([s, f"{m:.4f}", f"{sd:.4f}", f"{c:.1f}", f"{e:.1f}", n])

    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    colors = {"none": "#888888", "always": "#2ca02c",
              "random": "#1f77b4", "voi": "#d62728"}
    for s in order:
        m, sd, c, _e, _n = agg[s]
        ax.errorbar(c, m * 100, yerr=sd * 100, fmt="o", ms=10,
                    color=colors.get(s, "k"), capsize=4,
                    label=f"{s} (cost={c:.0f})")
        ax.annotate(s, (c, m * 100), textcoords="offset points",
                    xytext=(8, 6), fontsize=9)
    ax.set_xlabel("Human cost  (total human-control steps)")
    ax.set_ylabel(f"Success rate (%)  [{args.metric}]")
    ax.set_title(f"FORESIGHT-HIL: success vs human cost\n{task} ({backend}), HIL-SERL-style sim")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    fig.savefig(args.out, dpi=130)
    print(f"\n[plot] saved {args.out}")
    print(f"[csv]  saved {args.out_csv}")


if __name__ == "__main__":
    main()
