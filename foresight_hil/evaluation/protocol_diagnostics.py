"""Derived protocol diagnostics for the human-attention evaluation paper."""

from __future__ import annotations

import csv
from pathlib import Path


DISPLAY_LABELS = {
    "random_b350": "Random b350",
    "lv_voi_scale3": "LV-VoI scale3",
    "score_floor_vlv3_after4000_floor0p05": "Score-floor LV-VoI",
    "min_disagree_vlv0p25": "Min-disagree LV-VoI",
}


def read_csv_rows(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv_rows(path, rows):
    if not rows:
        raise ValueError("cannot write an empty derived diagnostic table")
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _find(rows, strategy):
    for row in rows:
        if row.get("strategy") == strategy:
            return row
    raise ValueError(f"missing strategy row: {strategy}")


def _float(row, key, default=0.0):
    value = row.get(key, "")
    if value == "":
        return default
    return float(value)


def _pp(value):
    return f"{value:+.1f} pp"


def _latex_escape(value):
    text = str(value)
    return (
        text.replace("\\", r"\textbackslash{}")
        .replace("_", r"\_")
        .replace("%", r"\%")
        .replace("&", r"\&")
    )


def _cost_success_context(r021_rows):
    random = _find(r021_rows, "random_b350")
    lv_voi = _find(r021_rows, "lv_voi_scale3")
    random_success = _float(random, "repeated_success") * 100.0
    lv_success = _float(lv_voi, "repeated_success") * 100.0
    random_cost = _float(random, "mean_best_human_steps")
    lv_cost = _float(lv_voi, "mean_best_human_steps")
    return {
        "success_margin_pp": random_success - lv_success,
        "cost_saving_steps": lv_cost - random_cost,
        "random_success": random_success,
        "lv_success": lv_success,
        "random_cost": random_cost,
        "lv_cost": lv_cost,
    }


def _repair_context(r024_rows):
    random = _find(r024_rows, "random_b350")
    score_floor = _find(r024_rows, "score_floor_vlv3_after4000_floor0p05")
    random_success = _float(random, "repeated_success") * 100.0
    floor_success = _float(score_floor, "repeated_success") * 100.0
    random_cost = _float(random, "mean_best_human_steps")
    floor_cost = _float(score_floor, "mean_best_human_steps")
    return {
        "success_gap_pp": floor_success - random_success,
        "extra_cost_steps": floor_cost - random_cost,
        "random_success": random_success,
        "floor_success": floor_success,
        "random_cost": random_cost,
        "floor_cost": floor_cost,
    }


def _trace_context(r023_trace_rows, r024_trace_rows):
    random = _find(r023_trace_rows, "random_b350")
    lv_voi = _find(r023_trace_rows, "lv_voi_scale3")
    score_floor = _find(r024_trace_rows, "score_floor_vlv3_after4000_floor0p05")
    random_starts = _float(random, "trace_starts")
    lv_starts = _float(lv_voi, "trace_starts")
    floor_starts = _float(score_floor, "trace_starts")
    return {
        "random_starts": random_starts,
        "lv_starts": lv_starts,
        "floor_starts": floor_starts,
        "start_inflation": lv_starts / random_starts,
        "floor_start_inflation": floor_starts / random_starts,
        "floor_start_reduction": (lv_starts - floor_starts) / lv_starts,
        "floor_gap_closure": (lv_starts - floor_starts) / (lv_starts - random_starts),
        "random_norm": _float(random, "mean_g2c_norm"),
        "lv_norm": _float(lv_voi, "mean_g2c_norm"),
        "random_xy": _float(random, "mean_g2c_xy"),
        "lv_xy": _float(lv_voi, "mean_g2c_xy"),
        "floor_median_score": _float(score_floor, "median_score"),
        "floor_low_score_starts": _float(score_floor, "after_floor_low_score_starts"),
    }


def build_protocol_gate_matrix(r021_rows, r024_rows, r023_trace_rows, r024_trace_rows):
    cost = _cost_success_context(r021_rows)
    repair = _repair_context(r024_rows)
    trace = _trace_context(r023_trace_rows, r024_trace_rows)
    return [
        {
            "gate_id": "G1",
            "gate": "Cost-matched random frontier",
            "question": "Does the trigger beat a random budget near its realized human cost?",
            "case_result": (
                f"random_b350 is {_pp(cost['success_margin_pp'])} higher and uses "
                f"{cost['cost_saving_steps']:.1f} fewer human steps than LV-VoI scale3"
            ),
            "verdict": "reject_trigger_superiority",
        },
        {
            "gate_id": "G2",
            "gate": "Repeated checkpoint evaluation",
            "question": "Is the ranking based on repeated rollouts rather than one checkpoint?",
            "case_result": "R021 reports 500 repeated Lift episodes per main strategy with Wilson intervals",
            "verdict": "ranking_auditable",
        },
        {
            "gate_id": "G3",
            "gate": "Trace-level attention diagnosis",
            "question": "How is the intervention budget spent when the trigger fails?",
            "case_result": (
                f"LV-VoI starts {int(trace['lv_starts'])}/{int(trace['random_starts'])} = "
                f"{trace['start_inflation']:.2f}x as often while starting closer to the cube"
            ),
            "verdict": "diagnose_budget_spending",
        },
        {
            "gate_id": "G4",
            "gate": "Same-seed repair stop gate",
            "question": "Should a lightweight repair be expanded?",
            "case_result": (
                f"score-floor remains {_pp(repair['success_gap_pp'])} below random b350 and "
                f"uses {repair['extra_cost_steps']:.1f} extra human steps"
            ),
            "verdict": "stop_repair_expansion",
        },
    ]


def build_failure_taxonomy_rows(r021_rows, r024_rows, r023_trace_rows, r024_trace_rows):
    cost = _cost_success_context(r021_rows)
    repair = _repair_context(r024_rows)
    trace = _trace_context(r023_trace_rows, r024_trace_rows)
    return [
        {
            "failure_mode": "cost_matched_reversal",
            "diagnostic_observation": (
                f"random_b350 dominates LV-VoI by {_pp(cost['success_margin_pp'])} "
                f"and {cost['cost_saving_steps']:.1f} fewer human steps"
            ),
            "evidence": "R021",
            "protocol_response": "Reject trigger-superiority claims before redesign.",
        },
        {
            "failure_mode": "over_triggering_despite_plausible_geometry",
            "diagnostic_observation": (
                f"LV-VoI starts {trace['start_inflation']:.2f}x as often as random while "
                f"mean 3D gripper-cube distance is lower ({trace['lv_norm']:.3f} vs {trace['random_norm']:.3f})"
            ),
            "evidence": "R023",
            "protocol_response": "Do not explain the failure as a simple far-from-object threshold issue.",
        },
        {
            "failure_mode": "weak_score_floor_selectivity",
            "diagnostic_observation": (
                f"Score-floor removes low-score post-floor starts but closes only "
                f"{trace['floor_gap_closure']:.1%} of the start-count gap to random"
            ),
            "evidence": "R024",
            "protocol_response": "Stop lightweight repair expansion under same-seed random dominance.",
        },
        {
            "failure_mode": "repair_success_cost_dominance",
            "diagnostic_observation": (
                f"Score-floor remains {_pp(repair['success_gap_pp'])} below same-seed random and "
                f"costs {repair['extra_cost_steps']:.1f} more human steps"
            ),
            "evidence": "R024",
            "protocol_response": "Require a substantially different mechanism before new experiments.",
        },
    ]


def build_derived_metric_rows(r021_rows, r024_rows, r023_trace_rows, r024_trace_rows):
    cost = _cost_success_context(r021_rows)
    repair = _repair_context(r024_rows)
    trace = _trace_context(r023_trace_rows, r024_trace_rows)
    return [
        {
            "metric": "random_b350_success_margin_vs_lv_voi_pp",
            "value": f"{cost['success_margin_pp']:.3f}",
            "formula": "100 * (random_b350_success - lv_voi_scale3_success)",
            "source": "R021",
            "interpretation": "Positive means random_b350 has higher repeated success.",
        },
        {
            "metric": "random_b350_human_step_saving_vs_lv_voi",
            "value": f"{cost['cost_saving_steps']:.3f}",
            "formula": "lv_voi_scale3_cost - random_b350_cost",
            "source": "R021",
            "interpretation": "Positive means random_b350 uses fewer human steps.",
        },
        {
            "metric": "lv_voi_start_inflation_vs_random",
            "value": f"{trace['start_inflation']:.3f}",
            "formula": "lv_voi_trace_starts / random_b350_trace_starts",
            "source": "R023",
            "interpretation": "Values above 1 indicate more intervention starts than random.",
        },
        {
            "metric": "score_floor_start_reduction_vs_lv_voi",
            "value": f"{trace['floor_start_reduction']:.3f}",
            "formula": "(lv_voi_trace_starts - score_floor_trace_starts) / lv_voi_trace_starts",
            "source": "R024",
            "interpretation": "Fraction of original LV-VoI starts removed by the score floor.",
        },
        {
            "metric": "score_floor_gap_closure_vs_random",
            "value": f"{trace['floor_gap_closure']:.3f}",
            "formula": "(lv_voi_trace_starts - score_floor_trace_starts) / (lv_voi_trace_starts - random_trace_starts)",
            "source": "R024",
            "interpretation": "Fraction of the LV-VoI-to-random start-count gap closed by the repair.",
        },
        {
            "metric": "score_floor_success_gap_vs_random_pp",
            "value": f"{repair['success_gap_pp']:.3f}",
            "formula": "100 * (score_floor_success - same_seed_random_b350_success)",
            "source": "R024",
            "interpretation": "Negative means the repaired trigger remains below same-seed random.",
        },
    ]


def render_latex_table(rows, caption, label, columns, widths=None):
    if widths is None:
        widths = [0.18] * len(columns)
    if len(widths) != len(columns):
        raise ValueError("width count must match table columns")
    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        rf"\caption{{{_latex_escape(caption)}}}",
        rf"\label{{{label}}}",
        r"\begin{tabular}{"
        + "".join(f"p{{{width:.2f}\\textwidth}}" for width in widths)
        + "}",
        r"\toprule",
        " & ".join(_latex_escape(heading) for _, heading in columns) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            " & ".join(_latex_escape(row.get(key, "")) for key, _ in columns) + r" \\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""])
    return "\n".join(lines)
