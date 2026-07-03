"""Trace-profile helpers for attention-allocation diagnostic figures."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


DISPLAY_LABELS = {
    "none": "No intervention",
    "random_b350": "Random b350",
    "random_b450": "Random b450",
    "random_b600": "Random b600",
    "lv_voi_scale3": "LV-VoI scale3",
    "min_disagree_vlv0p25": "Min-disagree LV-VoI",
    "score_floor_vlv3_after4000_floor0p05": "Score-floor LV-VoI",
}

TRACE_STRATEGY_ORDER = (
    "random_b350",
    "lv_voi_scale3",
    "score_floor_vlv3_after4000_floor0p05",
)


@dataclass(frozen=True)
class AttentionTraceSource:
    strategy: str
    relative_dir: str
    pattern: str
    source_label: str


DEFAULT_TRACE_SOURCES = (
    AttentionTraceSource(
        strategy="random_b350",
        relative_dir="results/r023_real_trace_seed0_2",
        pattern="trace_Lift_random_b350_seed*.csv",
        source_label="R023 random_b350 traces",
    ),
    AttentionTraceSource(
        strategy="lv_voi_scale3",
        relative_dir="results/r023_real_trace_seed0_2",
        pattern="trace_Lift_voi_b600_seed*.csv",
        source_label="R023 LV-VoI scale3 traces",
    ),
    AttentionTraceSource(
        strategy="score_floor_vlv3_after4000_floor0p05",
        relative_dir="results/r024_score_floor_seed0_2",
        pattern="trace_Lift_voi_b600_seed*.csv",
        source_label="R024 score-floor LV-VoI traces",
    ),
)


def read_csv_rows(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_profile_csv(path, rows):
    if not rows:
        raise ValueError("cannot write an empty attention trace profile")
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def as_float(value):
    text = str(value).strip()
    if text == "" or text.lower() == "nan":
        return math.nan
    try:
        return float(text)
    except ValueError:
        return math.nan


def finite_numeric_values(rows, column):
    values = [as_float(row.get(column, "")) for row in rows]
    return np.asarray([value for value in values if np.isfinite(value)], dtype=float)


def finite_numeric_differences(rows, left_column, right_column):
    values = []
    for row in rows:
        left = as_float(row.get(left_column, ""))
        right = as_float(row.get(right_column, ""))
        if np.isfinite(left) and np.isfinite(right):
            values.append(left - right)
    return np.asarray(values, dtype=float)


def rows_for_strategy(rows, strategy):
    return [row for row in rows if row.get("diagnostic_strategy") == strategy]


def collect_attention_trace_rows(project_root, trace_sources=DEFAULT_TRACE_SOURCES):
    root = Path(project_root)
    traces = []
    for source in trace_sources:
        source_dir = root / source.relative_dir
        files = sorted(source_dir.glob(source.pattern))
        if not files:
            raise FileNotFoundError(
                f"no trace files for {source.strategy}: {source_dir / source.pattern}"
            )
        for path in files:
            for row in read_csv_rows(path):
                trace_row = dict(row)
                trace_row["diagnostic_strategy"] = source.strategy
                trace_row["source_label"] = source.source_label
                traces.append(trace_row)
    return traces


def quantile_text(values):
    if len(values) == 0:
        return ""
    q1, median, q3 = np.percentile(values, [25, 50, 75])
    return f"{median:.4f} [{q1:.4f}, {q3:.4f}]"


def _fraction_text(mask_values):
    if len(mask_values) == 0:
        return ""
    return f"{float(np.mean(mask_values)):.6f}"


def build_attention_trace_profile(
    traces,
    strategy_order=TRACE_STRATEGY_ORDER,
    display_labels=DISPLAY_LABELS,
):
    profile_rows = []
    for strategy in strategy_order:
        group = rows_for_strategy(traces, strategy)
        steps = finite_numeric_values(group, "env_step")
        budgets = finite_numeric_values(group, "budget_used_frac")
        norm = finite_numeric_values(group, "gripper_to_cube_norm")
        xy = finite_numeric_values(group, "gripper_to_cube_xy")
        eef_z = finite_numeric_values(group, "eef_z")
        cube_z = finite_numeric_values(group, "cube_z")
        score = finite_numeric_values(group, "score")
        p_fail = finite_numeric_values(group, "p_fail")
        eef_gap = finite_numeric_differences(group, "eef_z", "cube_z")

        profile_rows.append({
            "strategy": strategy,
            "display_label": display_labels.get(strategy, strategy),
            "n_trace_starts": len(group),
            "mean_start_step": f"{np.mean(steps):.3f}" if len(steps) else "",
            "median_start_step": f"{np.median(steps):.3f}" if len(steps) else "",
            "early_0_2k_frac": _fraction_text(steps < 2000),
            "mid_2_6k_frac": _fraction_text((steps >= 2000) & (steps < 6000)),
            "late_6_10k_frac": _fraction_text(steps >= 6000),
            "budget_used_frac_median_iqr": quantile_text(budgets),
            "g2c_norm_median_iqr": quantile_text(norm),
            "g2c_xy_median_iqr": quantile_text(xy),
            "eef_z_median_iqr": quantile_text(eef_z),
            "cube_z_median_iqr": quantile_text(cube_z),
            "eef_minus_cube_z_median_iqr": quantile_text(eef_gap),
            "score_median_iqr": quantile_text(score),
            "score_ge_9p9_frac": _fraction_text(score >= 9.9),
            "p_fail_median_iqr": quantile_text(p_fail),
            "p_fail_ge_0p99_frac": _fraction_text(p_fail >= 0.99),
        })
    return profile_rows
