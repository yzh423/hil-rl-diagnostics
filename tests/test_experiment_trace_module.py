import unittest
from types import SimpleNamespace

from foresight_hil.experiments.trace import (
    INTERVENTION_TRACE_FIELDS,
    intervention_trace_row,
)


class InterventionTraceModuleTest(unittest.TestCase):
    def test_trace_fields_include_lift_and_stack_diagnostics(self):
        self.assertEqual(INTERVENTION_TRACE_FIELDS[:6], [
            "env_step", "episode", "episode_step", "task", "strategy", "seed",
        ])
        self.assertIn("gripper_to_cube_norm", INTERVENTION_TRACE_FIELDS)
        self.assertIn("cubeA_z", INTERVENTION_TRACE_FIELDS)
        self.assertIn("cubeB_z", INTERVENTION_TRACE_FIELDS)
        self.assertIn("stack_cubeA_lifted", INTERVENTION_TRACE_FIELDS)

    def test_trace_row_records_stack_geometry(self):
        args = SimpleNamespace(task="Stack", strategy="voi", seed=1, budget=300)
        controller = SimpleNamespace(
            spent=45,
            engagements=3,
            last_candidate=False,
            last_score=0.0625,
            last_p_fail=0.5,
        )
        priv = {
            "task": "Stack",
            "eef_pos": [0.25, 0.15, 0.95],
            "cubeA_pos": [0.20, 0.10, 0.88],
            "cubeB_pos": [0.22, 0.10, 0.80],
            "gripper_to_cubeA": [0.05, 0.05, -0.07],
            "gripper_to_cubeB": [0.03, 0.05, -0.15],
        }

        row = intervention_trace_row(
            step=2000, ep_idx=7, ep_len=40,
            args=args, controller=controller, priv=priv)

        self.assertEqual(row["task"], "Stack")
        self.assertEqual(row["candidate"], 0)
        self.assertEqual(row["score"], "0.062500")
        self.assertEqual(row["p_fail"], "0.500000")
        self.assertEqual(row["budget_used_frac"], "0.1500")
        self.assertEqual(row["cubeA_z"], "0.880000")
        self.assertEqual(row["cubeB_z"], "0.800000")
        self.assertEqual(row["gripper_to_cubeA_norm"], "0.099499")
        self.assertEqual(row["gripper_to_cubeB_norm"], "0.160935")
        self.assertEqual(row["stack_cubeA_lifted"], 1)


if __name__ == "__main__":
    unittest.main()
