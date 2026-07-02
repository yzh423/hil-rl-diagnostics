"""Repeated-evaluation summaries used by paper-facing checkpoint claims."""

from __future__ import annotations

import numpy as np

from foresight_hil.metrics import wilson_interval


def summarize_repeats(rows):
    """Aggregate repeated checkpoint-evaluation rows."""
    if not rows:
        raise ValueError("at least one repeat row is required")

    success_rates = np.asarray([float(r["success_rate"]) for r in rows], dtype=float)
    returns = np.asarray([float(r["return_mean"]) for r in rows], dtype=float)
    total_successes = int(sum(int(r["successes"]) for r in rows))
    total_episodes = int(sum(int(r["episodes"]) for r in rows))
    ci_low, ci_high = wilson_interval(total_successes, total_episodes)
    return {
        "n_repeats": len(rows),
        "success_mean": float(success_rates.mean()),
        "success_std": float(success_rates.std()),
        "return_mean": float(returns.mean()),
        "return_std": float(returns.std()),
        "total_successes": total_successes,
        "total_episodes": total_episodes,
        "success_ci_low": ci_low,
        "success_ci_high": ci_high,
    }


def repeat_summary_row(checkpoint, task, summary):
    """Format a repeated-evaluation summary for the summary CSV."""
    return {
        "checkpoint": checkpoint,
        "task": task,
        "n_repeats": summary["n_repeats"],
        "success_mean": f"{summary['success_mean']:.4f}",
        "success_std": f"{summary['success_std']:.4f}",
        "return_mean": f"{summary['return_mean']:.4f}",
        "return_std": f"{summary['return_std']:.4f}",
        "total_successes": summary["total_successes"],
        "total_episodes": summary["total_episodes"],
        "success_ci_low": f"{summary['success_ci_low']:.4f}",
        "success_ci_high": f"{summary['success_ci_high']:.4f}",
    }
