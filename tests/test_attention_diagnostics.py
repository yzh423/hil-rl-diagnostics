import csv
import tempfile
import unittest
from pathlib import Path

from foresight_hil.evaluation.attention_diagnostics import (
    AttentionTraceSource,
    build_attention_trace_profile,
    collect_attention_trace_rows,
    write_profile_csv,
)


TRACE_FIELDS = [
    "env_step",
    "budget_used_frac",
    "gripper_to_cube_norm",
    "gripper_to_cube_xy",
    "eef_z",
    "cube_z",
    "score",
    "p_fail",
]


def trace_row(step, budget, norm, xy, eef_z, cube_z, score="", p_fail=""):
    return {
        "env_step": str(step),
        "budget_used_frac": str(budget),
        "gripper_to_cube_norm": str(norm),
        "gripper_to_cube_xy": str(xy),
        "eef_z": str(eef_z),
        "cube_z": str(cube_z),
        "score": str(score),
        "p_fail": str(p_fail),
    }


def write_trace_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TRACE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


class AttentionDiagnosticsTest(unittest.TestCase):
    def test_builds_attention_trace_profile_with_timing_geometry_and_score_fields(self):
        traces = []
        for row in [
            trace_row(1000, 0.1, 0.1, 0.05, 1.0, 0.8),
            trace_row(3000, 0.5, 0.2, 0.10, 1.1, 0.8),
            trace_row(7000, 1.0, 0.3, 0.15, 1.2, 0.8),
        ]:
            row["diagnostic_strategy"] = "random_b350"
            traces.append(row)
        for row in [
            trace_row(4000, 0.2, 0.05, 0.02, 0.9, 0.8, 10.0, 1.0),
            trace_row(8000, 0.8, 0.15, 0.08, 1.0, 0.8, 0.05, 0.02),
        ]:
            row["diagnostic_strategy"] = "lv_voi_scale3"
            traces.append(row)

        profile = build_attention_trace_profile(
            traces,
            strategy_order=("random_b350", "lv_voi_scale3"),
        )

        self.assertEqual(profile[0]["n_trace_starts"], 3)
        self.assertEqual(profile[0]["early_0_2k_frac"], "0.333333")
        self.assertEqual(profile[0]["mid_2_6k_frac"], "0.333333")
        self.assertEqual(profile[0]["late_6_10k_frac"], "0.333333")
        self.assertEqual(profile[0]["g2c_norm_median_iqr"], "0.2000 [0.1500, 0.2500]")
        self.assertEqual(profile[0]["eef_minus_cube_z_median_iqr"], "0.3000 [0.2500, 0.3500]")
        self.assertEqual(profile[0]["score_median_iqr"], "")

        self.assertEqual(profile[1]["n_trace_starts"], 2)
        self.assertEqual(profile[1]["score_ge_9p9_frac"], "0.500000")
        self.assertEqual(profile[1]["p_fail_ge_0p99_frac"], "0.500000")

    def test_collects_trace_rows_from_sources_and_writes_profile_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_trace_csv(
                root / "results" / "rA" / "trace_seed0.csv",
                [trace_row(100, 0.1, 0.1, 0.05, 1.0, 0.8)],
            )
            write_trace_csv(
                root / "results" / "rB" / "trace_seed0.csv",
                [trace_row(200, 0.2, 0.2, 0.10, 1.1, 0.8, 10.0, 1.0)],
            )
            sources = (
                AttentionTraceSource("random_b350", "results/rA", "trace_*.csv", "A"),
                AttentionTraceSource("lv_voi_scale3", "results/rB", "trace_*.csv", "B"),
            )

            traces = collect_attention_trace_rows(root, sources)
            profile = build_attention_trace_profile(
                traces,
                strategy_order=("random_b350", "lv_voi_scale3"),
            )
            output = root / "profile.csv"
            write_profile_csv(output, profile)

            self.assertEqual(len(traces), 2)
            self.assertEqual(traces[0]["diagnostic_strategy"], "random_b350")
            self.assertEqual(traces[1]["source_label"], "B")
            text = output.read_text()
            self.assertIn("random_b350", text)
            self.assertIn("lv_voi_scale3", text)


if __name__ == "__main__":
    unittest.main()
