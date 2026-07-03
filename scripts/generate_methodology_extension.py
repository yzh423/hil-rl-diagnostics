from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foresight_hil.evaluation.protocol_diagnostics import (
    build_derived_metric_rows,
    build_failure_taxonomy_rows,
    build_protocol_gate_matrix,
    read_csv_rows,
    render_latex_table,
    write_csv_rows,
)


R021 = ROOT / "results" / "r021_random_costmatch" / "r021_costmatch_aggregate.csv"
R024_AGG = ROOT / "results" / "r024_score_floor_seed0_2" / "r024_score_floor_aggregate.csv"
R023_TRACE = ROOT / "results" / "r023_real_trace_seed0_2" / "r023_trace_strategy_diagnostics.csv"
R024_TRACE = ROOT / "results" / "r024_score_floor_seed0_2" / "r024_trace_strategy_compare.csv"
R056 = ROOT / "results" / "r056_methodology_extension"
FIGURES = ROOT / "figures"

GATE_VERDICT_LABELS = {
    "reject_trigger_superiority": "Reject trigger-superiority claim",
    "ranking_auditable": "Ranking is auditable",
    "diagnose_budget_spending": "Diagnose spending mechanism",
    "stop_repair_expansion": "Stop lightweight repair expansion",
}

FAILURE_MODE_LABELS = {
    "cost_matched_reversal": "Cost-matched reversal",
    "over_triggering_despite_plausible_geometry": "Over-triggering despite plausible geometry",
    "weak_score_floor_selectivity": "Weak score-floor selectivity",
    "repair_success_cost_dominance": "Repair remains success-cost dominated",
}


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    R056.mkdir(parents=True, exist_ok=True)
    r021_rows = read_csv_rows(R021)
    r024_rows = read_csv_rows(R024_AGG)
    r023_trace_rows = read_csv_rows(R023_TRACE)
    r024_trace_rows = read_csv_rows(R024_TRACE)

    gate_rows = build_protocol_gate_matrix(
        r021_rows, r024_rows, r023_trace_rows, r024_trace_rows
    )
    taxonomy_rows = build_failure_taxonomy_rows(
        r021_rows, r024_rows, r023_trace_rows, r024_trace_rows
    )
    metric_rows = build_derived_metric_rows(
        r021_rows, r024_rows, r023_trace_rows, r024_trace_rows
    )

    write_csv_rows(R056 / "protocol_gate_matrix.csv", gate_rows)
    write_csv_rows(R056 / "failure_taxonomy.csv", taxonomy_rows)
    write_csv_rows(R056 / "derived_attention_metrics.csv", metric_rows)

    gate_table_rows = [
        {**row, "verdict": GATE_VERDICT_LABELS.get(row["verdict"], row["verdict"])}
        for row in gate_rows
    ]
    taxonomy_table_rows = [
        {
            **row,
            "failure_mode": FAILURE_MODE_LABELS.get(row["failure_mode"], row["failure_mode"]),
        }
        for row in taxonomy_rows
    ]
    gate_latex = render_latex_table(
        gate_table_rows,
        caption=(
            "Protocol gate outcomes for the current Lift case study. R056 derives "
            "these rows from registered R021/R023/R024 evidence and uses them to "
            "formalize the diagnostic protocol rather than to introduce a new experiment."
        ),
        label="tab:protocol_gate_matrix_r056",
        columns=(
            ("gate_id", "Gate"),
            ("gate", "Diagnostic gate"),
            ("case_result", "Observed case result"),
            ("verdict", "Protocol verdict"),
        ),
        widths=(0.08, 0.23, 0.43, 0.20),
    )
    taxonomy_latex = render_latex_table(
        taxonomy_table_rows,
        caption=(
            "Failure-mode taxonomy induced by the current diagnostic evidence. "
            "Each row links a failure mode to a registered source and a protocol response."
        ),
        label="tab:failure_taxonomy_r056",
        columns=(
            ("failure_mode", "Failure mode"),
            ("diagnostic_observation", "Diagnostic observation"),
            ("evidence", "Evidence"),
            ("protocol_response", "Protocol response"),
        ),
        widths=(0.21, 0.34, 0.07, 0.30),
    )
    write_text(FIGURES / "TABLE_protocol_gate_matrix_r056.tex", gate_latex)
    write_text(FIGURES / "TABLE_failure_taxonomy_r056.tex", taxonomy_latex)

    print(f"[r056] wrote {R056 / 'protocol_gate_matrix.csv'}")
    print(f"[r056] wrote {R056 / 'failure_taxonomy.csv'}")
    print(f"[r056] wrote {R056 / 'derived_attention_metrics.csv'}")
    print(f"[r056] wrote {FIGURES / 'TABLE_protocol_gate_matrix_r056.tex'}")
    print(f"[r056] wrote {FIGURES / 'TABLE_failure_taxonomy_r056.tex'}")


if __name__ == "__main__":
    main()
