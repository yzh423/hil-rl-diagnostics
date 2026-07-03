import csv
import tempfile
import unittest
from pathlib import Path

from foresight_hil.evaluation.offline_trace_audit import (
    build_offline_gate_audit,
    build_phase_trace_summary,
    write_csv_rows,
)


def trace_row(step, budget, score="", norm=0.1, xy=0.05, strategy="lv_voi_scale3"):
    return {
        "env_step": str(step),
        "budget_used_frac": str(budget),
        "score": str(score),
        "p_fail": str(score),
        "gripper_to_cube_norm": str(norm),
        "gripper_to_cube_xy": str(xy),
        "diagnostic_strategy": strategy,
    }


class OfflineTraceAuditTest(unittest.TestCase):
    def test_builds_phase_summary_from_trace_rows(self):
        traces = [
            trace_row(1000, 0.1, strategy="random_b350"),
            trace_row(3000, 0.2, strategy="random_b350"),
            trace_row(5000, 0.3, strategy="random_b350"),
            trace_row(9000, 0.4, strategy="random_b350"),
        ]

        rows = build_phase_trace_summary(traces, ("random_b350",))

        counts = {row["phase"]: row["start_count"] for row in rows}
        self.assertEqual(counts["early_0_2k"], "1")
        self.assertEqual(counts["quiet_2_4k"], "1")
        self.assertEqual(counts["post_floor_4_6k"], "1")
        self.assertEqual(counts["late_6_10k"], "1")
        self.assertEqual(rows[0]["start_fraction"], "0.250000")

    def test_audits_posthoc_gates_and_observed_score_floor(self):
        random_rows = [
            trace_row(1000, 0.1, strategy="random_b350"),
            trace_row(6000, 0.6, strategy="random_b350"),
        ]
        lv_rows = [
            trace_row(1000, 0.1, 10.0),
            trace_row(5000, 0.3, 0.01),
            trace_row(7000, 0.5, 0.08),
            trace_row(9000, 0.9, 0.02),
        ]
        score_floor_rows = [
            trace_row(1000, 0.1, 10.0, strategy="score_floor_vlv3_after4000_floor0p05"),
            trace_row(5000, 0.3, 0.06, strategy="score_floor_vlv3_after4000_floor0p05"),
            trace_row(9000, 0.8, 0.07, strategy="score_floor_vlv3_after4000_floor0p05"),
        ]

        rows = build_offline_gate_audit(random_rows, lv_rows, score_floor_rows)
        by_id = {row["gate_id"]: row for row in rows}

        self.assertEqual(by_id["r023_random_reference"]["retained_starts"], "2")
        self.assertEqual(by_id["r023_lv_voi_original"]["excess_starts_vs_random"], "2")
        self.assertEqual(by_id["r024_score_floor_observed"]["retained_starts"], "3")
        self.assertEqual(by_id["posthoc_score_after4k_ge0p05"]["retained_starts"], "2")
        self.assertEqual(by_id["posthoc_score_after4k_ge0p05"]["gap_closed_vs_original_lv_voi"], "1.000000")
        self.assertEqual(by_id["posthoc_drop_score_ge9p9"]["retained_starts"], "3")
        self.assertEqual(by_id["posthoc_earliest_random_count_cap"]["retained_starts"], "2")

    def test_writes_csv_rows(self):
        rows = [{"gate_id": "g1", "retained_starts": "2"}]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audit.csv"
            write_csv_rows(path, rows)
            with path.open(newline="", encoding="utf-8") as f:
                loaded = list(csv.DictReader(f))

        self.assertEqual(loaded[0]["gate_id"], "g1")


if __name__ == "__main__":
    unittest.main()

