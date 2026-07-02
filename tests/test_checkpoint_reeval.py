import unittest

from scripts.evaluate_checkpoint import summarize_repeats


class CheckpointReevalSummaryTest(unittest.TestCase):
    def test_summarize_repeats_combines_success_counts_and_variance(self):
        rows = [
            {"success_rate": 0.8, "successes": 16, "episodes": 20, "return_mean": 100.0},
            {"success_rate": 0.9, "successes": 18, "episodes": 20, "return_mean": 120.0},
            {"success_rate": 0.7, "successes": 14, "episodes": 20, "return_mean": 80.0},
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


if __name__ == "__main__":
    unittest.main()
