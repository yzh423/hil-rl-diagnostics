import unittest

from foresight_hil.evaluation.protocol import (
    repeat_summary_row,
    summarize_repeats,
)


class EvaluationProtocolTest(unittest.TestCase):
    def test_summarize_repeats_combines_counts_variance_and_wilson_ci(self):
        rows = [
            {"success_rate": "0.8000", "successes": "16", "episodes": "20", "return_mean": "100.0"},
            {"success_rate": "0.9000", "successes": "18", "episodes": "20", "return_mean": "120.0"},
            {"success_rate": "0.7000", "successes": "14", "episodes": "20", "return_mean": "80.0"},
        ]

        summary = summarize_repeats(rows)

        self.assertEqual(summary["n_repeats"], 3)
        self.assertEqual(summary["total_successes"], 48)
        self.assertEqual(summary["total_episodes"], 60)
        self.assertAlmostEqual(summary["success_mean"], 0.8)
        self.assertAlmostEqual(summary["success_std"], 0.081649658, places=6)
        self.assertAlmostEqual(summary["return_mean"], 100.0)
        self.assertLess(summary["success_ci_low"], summary["success_mean"])
        self.assertGreater(summary["success_ci_high"], summary["success_mean"])

    def test_repeat_summary_row_formats_paper_facing_values(self):
        summary = summarize_repeats([
            {"success_rate": 0.5, "successes": 5, "episodes": 10, "return_mean": 1.0},
            {"success_rate": 0.7, "successes": 7, "episodes": 10, "return_mean": 3.0},
        ])

        row = repeat_summary_row("best.zip", "Lift", summary)

        self.assertEqual(row["checkpoint"], "best.zip")
        self.assertEqual(row["task"], "Lift")
        self.assertEqual(row["n_repeats"], 2)
        self.assertEqual(row["success_mean"], "0.6000")
        self.assertEqual(row["return_mean"], "2.0000")
        self.assertEqual(row["total_successes"], 12)
        self.assertEqual(row["total_episodes"], 20)
        self.assertRegex(row["success_ci_low"], r"^0\.\d{4}$")

    def test_summarize_repeats_requires_at_least_one_row(self):
        with self.assertRaises(ValueError):
            summarize_repeats([])


if __name__ == "__main__":
    unittest.main()
