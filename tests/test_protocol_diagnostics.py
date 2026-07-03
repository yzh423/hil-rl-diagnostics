import csv
import tempfile
import unittest
from pathlib import Path

from foresight_hil.evaluation.protocol_diagnostics import (
    build_derived_metric_rows,
    build_failure_taxonomy_rows,
    build_protocol_gate_matrix,
    render_latex_table,
    write_csv_rows,
)


def row(strategy, success, cost, successes="0", episodes="0"):
    return {
        "strategy": strategy,
        "repeated_success": str(success),
        "mean_best_human_steps": str(cost),
        "total_successes": successes,
        "total_episodes": episodes,
    }


def trace_row(strategy, starts, norm, xy, score="", low_score=""):
    return {
        "strategy": strategy,
        "trace_starts": str(starts),
        "mean_g2c_norm": str(norm),
        "mean_g2c_xy": str(xy),
        "median_score": str(score),
        "after_floor_low_score_starts": str(low_score),
    }


class ProtocolDiagnosticsTest(unittest.TestCase):
    def test_builds_gate_matrix_with_cost_reversal_and_repair_stop(self):
        r021 = [
            row("random_b350", 0.878, 177.0, "439", "500"),
            row("lv_voi_scale3", 0.832, 202.0, "416", "500"),
        ]
        r024 = [
            row("random_b350", 0.8633, 95.0, "259", "300"),
            row("score_floor_vlv3_after4000_floor0p05", 0.7767, 253.3333, "233", "300"),
        ]
        r023_trace = [
            trace_row("random_b350", 55, 0.284851, 0.235331),
            trace_row("lv_voi_scale3", 96, 0.217166, 0.152267),
        ]
        r024_trace = [
            trace_row("random_b350", 55, 0.284851, 0.235331),
            trace_row("lv_voi_scale3", 96, 0.217166, 0.152267),
            trace_row("score_floor_vlv3_after4000_floor0p05", 94, 0.234083, 0.160375, 0.067165, 0),
        ]

        rows = build_protocol_gate_matrix(r021, r024, r023_trace, r024_trace)

        self.assertEqual([r["gate_id"] for r in rows], ["G1", "G2", "G3", "G4"])
        self.assertIn("+4.6 pp", rows[0]["case_result"])
        self.assertIn("25.0 fewer", rows[0]["case_result"])
        self.assertEqual(rows[0]["verdict"], "reject_trigger_superiority")
        self.assertIn("96/55 = 1.75x", rows[2]["case_result"])
        self.assertEqual(rows[3]["verdict"], "stop_repair_expansion")

    def test_builds_failure_taxonomy_and_derived_metrics(self):
        r021 = [
            row("random_b350", 0.878, 177.0),
            row("lv_voi_scale3", 0.832, 202.0),
        ]
        r024 = [
            row("random_b350", 0.8633, 95.0),
            row("score_floor_vlv3_after4000_floor0p05", 0.7767, 253.3333),
        ]
        r023_trace = [
            trace_row("random_b350", 55, 0.284851, 0.235331),
            trace_row("lv_voi_scale3", 96, 0.217166, 0.152267),
        ]
        r024_trace = [
            trace_row("random_b350", 55, 0.284851, 0.235331),
            trace_row("lv_voi_scale3", 96, 0.217166, 0.152267),
            trace_row("score_floor_vlv3_after4000_floor0p05", 94, 0.234083, 0.160375, 0.067165, 0),
        ]

        taxonomy = build_failure_taxonomy_rows(r021, r024, r023_trace, r024_trace)
        metrics = build_derived_metric_rows(r021, r024, r023_trace, r024_trace)

        self.assertEqual(taxonomy[0]["failure_mode"], "cost_matched_reversal")
        self.assertIn("random_b350 dominates", taxonomy[0]["diagnostic_observation"])
        metric_by_name = {row["metric"]: row for row in metrics}
        self.assertEqual(metric_by_name["lv_voi_start_inflation_vs_random"]["value"], "1.745")
        self.assertEqual(metric_by_name["score_floor_start_reduction_vs_lv_voi"]["value"], "0.021")
        self.assertEqual(metric_by_name["score_floor_gap_closure_vs_random"]["value"], "0.049")

    def test_writes_csv_and_renders_latex_table(self):
        rows = [
            {"gate_id": "G1", "gate": "Cost matching", "verdict": "reject"},
            {"gate_id": "G2", "gate": "Repeated evaluation", "verdict": "require"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "gates.csv"
            write_csv_rows(path, rows)
            with path.open(newline="", encoding="utf-8") as f:
                loaded = list(csv.DictReader(f))
            latex = render_latex_table(
                rows,
                caption="Gate matrix",
                label="tab:test_gate_matrix",
                columns=(("gate_id", "Gate"), ("gate", "Requirement"), ("verdict", "Verdict")),
            )

        self.assertEqual(loaded[0]["gate_id"], "G1")
        self.assertIn("\\caption{Gate matrix}", latex)
        self.assertIn("\\label{tab:test_gate_matrix}", latex)
        self.assertIn("Cost matching", latex)


if __name__ == "__main__":
    unittest.main()
