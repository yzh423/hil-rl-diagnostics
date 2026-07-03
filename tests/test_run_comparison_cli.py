import unittest

from scripts.run_comparison import build_parser


class RunComparisonCliTest(unittest.TestCase):
    def test_parser_accepts_candidate_trace_flag(self):
        args = build_parser().parse_args(["--trace_candidates"])

        self.assertTrue(args.trace_candidates)


if __name__ == "__main__":
    unittest.main()

