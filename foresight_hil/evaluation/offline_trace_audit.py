"""Offline trigger-gate audits from recorded intervention-start traces."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from statistics import median


PHASES = (
    ("early_0_2k", 0.0, 2000.0),
    ("quiet_2_4k", 2000.0, 4000.0),
    ("post_floor_4_6k", 4000.0, 6000.0),
    ("late_6_10k", 6000.0, math.inf),
)


@dataclass(frozen=True)
class OfflineGateSpec:
    gate_id: str
    label: str
    description: str
    caveat: str
    predicate: object


def write_csv_rows(path, rows):
    if not rows:
        raise ValueError("cannot write an empty offline trace audit table")
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
        parsed = float(text)
    except ValueError:
        return math.nan
    return parsed if math.isfinite(parsed) else math.nan


def finite_values(rows, column):
    values = [as_float(row.get(column, "")) for row in rows]
    return [value for value in values if math.isfinite(value)]


def format_float(value, digits=6):
    if value == "" or value is None:
        return ""
    if not math.isfinite(float(value)):
        return ""
    return f"{float(value):.{digits}f}"


def format_fraction(numerator, denominator):
    if denominator == 0:
        return ""
    return format_float(numerator / denominator)


def median_text(rows, column):
    values = finite_values(rows, column)
    if not values:
        return ""
    return format_float(median(values))


def count_post4k_low_score(rows, threshold=0.05):
    count = 0
    for row in rows:
        step = as_float(row.get("env_step", ""))
        score = as_float(row.get("score", ""))
        if math.isfinite(step) and math.isfinite(score) and step >= 4000.0 and score < threshold:
            count += 1
    return count


def rows_for_strategy(rows, strategy):
    return [row for row in rows if row.get("diagnostic_strategy") == strategy]


def phase_for_step(step):
    for name, lower, upper in PHASES:
        if lower <= step < upper:
            return name
    return ""


def default_gate_specs():
    return (
        OfflineGateSpec(
            gate_id="posthoc_score_after4k_ge0p05",
            label="Post-hoc score floor >=0.05 after 4k",
            description="Keep original R023 LV-VoI starts before 4k, then require score >= 0.05.",
            caveat="Post-hoc filtering of accepted starts; not an online replay.",
            predicate=lambda row: as_float(row.get("env_step", "")) < 4000.0
            or as_float(row.get("score", "")) >= 0.05,
        ),
        OfflineGateSpec(
            gate_id="posthoc_score_after4k_ge0p10",
            label="Post-hoc score floor >=0.10 after 4k",
            description="Keep original R023 LV-VoI starts before 4k, then require score >= 0.10.",
            caveat="Stricter score gate; diagnostic only.",
            predicate=lambda row: as_float(row.get("env_step", "")) < 4000.0
            or as_float(row.get("score", "")) >= 0.10,
        ),
        OfflineGateSpec(
            gate_id="posthoc_drop_score_ge9p9",
            label="Drop saturated score >=9.9",
            description="Remove starts whose LV-VoI score is clipped near 10.",
            caveat="Tests score saturation as a failure signal, not a validated trigger.",
            predicate=lambda row: as_float(row.get("score", "")) < 9.9,
        ),
        OfflineGateSpec(
            gate_id="posthoc_late_after4k_only",
            label="Keep only starts after 4k",
            description="Remove the early intervention starts and keep the post-4k phase.",
            caveat="Phase-only filter; ignores success impact.",
            predicate=lambda row: as_float(row.get("env_step", "")) >= 4000.0,
        ),
        OfflineGateSpec(
            gate_id="posthoc_budget_frac_le0p60",
            label="Budget fraction <=0.60",
            description="Keep starts up to 60% of the LV-VoI recorded budget fraction.",
            caveat="A hard cap can match count but does not select better interventions.",
            predicate=lambda row: as_float(row.get("budget_used_frac", "")) <= 0.60,
        ),
    )


def summarize_selected_rows(
    gate_id,
    label,
    audit_kind,
    source_rows,
    selected_rows,
    original_lv_count,
    random_target_count,
    description,
    caveat,
):
    retained = len(selected_rows)
    removed = len(source_rows) - retained
    denominator = original_lv_count - random_target_count
    gap_closed = ""
    if audit_kind != "reference_trace" and denominator != 0:
        gap_closed = format_float((original_lv_count - retained) / denominator)
    steps = finite_values(selected_rows, "env_step")
    score_values = finite_values(selected_rows, "score")
    score_saturated = ""
    if score_values:
        score_saturated = format_fraction(
            sum(1 for value in score_values if value >= 9.9),
            len(score_values),
        )
    return {
        "gate_id": gate_id,
        "label": label,
        "audit_kind": audit_kind,
        "description": description,
        "source_start_count": str(len(source_rows)),
        "retained_starts": str(retained),
        "removed_starts": str(removed),
        "retention_frac": format_fraction(retained, len(source_rows)),
        "random_target_starts": str(random_target_count),
        "excess_starts_vs_random": str(retained - random_target_count),
        "gap_closed_vs_original_lv_voi": gap_closed,
        "median_start_step": median_text(selected_rows, "env_step"),
        "early_0_2k_frac": format_fraction(sum(step < 2000.0 for step in steps), len(steps)),
        "mid_2_6k_frac": format_fraction(
            sum(2000.0 <= step < 6000.0 for step in steps), len(steps)
        ),
        "late_6_10k_frac": format_fraction(sum(step >= 6000.0 for step in steps), len(steps)),
        "median_budget_used_frac": median_text(selected_rows, "budget_used_frac"),
        "median_g2c_norm": median_text(selected_rows, "gripper_to_cube_norm"),
        "median_g2c_xy": median_text(selected_rows, "gripper_to_cube_xy"),
        "median_score": median_text(selected_rows, "score"),
        "score_ge9p9_frac": score_saturated,
        "post4k_low_score_starts": str(count_post4k_low_score(selected_rows)),
        "caveat": caveat,
    }


def build_offline_gate_audit(
    random_rows,
    lv_rows,
    score_floor_rows,
    gate_specs=None,
):
    if gate_specs is None:
        gate_specs = default_gate_specs()
    random_target = len(random_rows)
    original_lv_count = len(lv_rows)
    rows = [
        summarize_selected_rows(
            "r023_random_reference",
            "R023 random b350 reference",
            "reference_trace",
            random_rows,
            random_rows,
            original_lv_count,
            random_target,
            "Observed random b350 intervention-start trace count.",
            "Reference count only; random has no LV-VoI score fields.",
        ),
        summarize_selected_rows(
            "r023_lv_voi_original",
            "R023 original LV-VoI trace",
            "observed_trace_baseline",
            lv_rows,
            lv_rows,
            original_lv_count,
            random_target,
            "Observed original LV-VoI scale3 intervention-start trace count.",
            "Baseline accepted-start trace; not a counterfactual.",
        ),
        summarize_selected_rows(
            "r024_score_floor_observed",
            "R024 observed score-floor run",
            "observed_online_followup",
            score_floor_rows,
            score_floor_rows,
            original_lv_count,
            random_target,
            "Observed score-floor repair run with the same trace schema.",
            "Actual repaired run; success remains dominated by random in R024.",
        ),
    ]
    for spec in gate_specs:
        selected = [row for row in lv_rows if spec.predicate(row)]
        rows.append(
            summarize_selected_rows(
                spec.gate_id,
                spec.label,
                "posthoc_filter_on_r023_lv_voi_starts",
                lv_rows,
                selected,
                original_lv_count,
                random_target,
                spec.description,
                spec.caveat,
            )
        )
    earliest = sorted(lv_rows, key=lambda row: as_float(row.get("env_step", "")))[:random_target]
    rows.append(
        summarize_selected_rows(
            "posthoc_earliest_random_count_cap",
            f"Earliest {random_target} LV-VoI starts",
            "posthoc_count_cap_on_r023_lv_voi_starts",
            lv_rows,
            earliest,
            original_lv_count,
            random_target,
            "Keep the earliest original LV-VoI starts until the random b350 start count is matched.",
            "Count cap only; not evidence that the retained starts are useful.",
        )
    )
    return rows


def build_phase_trace_summary(trace_rows, strategy_order):
    rows = []
    for strategy in strategy_order:
        group = rows_for_strategy(trace_rows, strategy)
        total = len(group)
        for phase, lower, upper in PHASES:
            selected = []
            for row in group:
                step = as_float(row.get("env_step", ""))
                if math.isfinite(step) and lower <= step < upper:
                    selected.append(row)
            rows.append({
                "strategy": strategy,
                "phase": phase,
                "start_count": str(len(selected)),
                "start_fraction": format_fraction(len(selected), total),
                "median_budget_used_frac": median_text(selected, "budget_used_frac"),
                "median_g2c_norm": median_text(selected, "gripper_to_cube_norm"),
                "median_g2c_xy": median_text(selected, "gripper_to_cube_xy"),
                "median_score": median_text(selected, "score"),
                "median_p_fail": median_text(selected, "p_fail"),
                "post4k_low_score_starts": str(count_post4k_low_score(selected)),
            })
    return rows
