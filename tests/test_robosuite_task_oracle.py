import unittest

import numpy as np

from foresight_hil.envs.robosuite_env import RobosuiteGymEnv
from foresight_hil.oracle.robosuite_oracle import ScriptedLiftOracle
from scripts.train_robosuite_hil import stack_phase_guard_allows


class StackPrivilegedStateTest(unittest.TestCase):
    def test_stack_privileged_state_exposes_cube_a_and_cube_b(self):
        env = RobosuiteGymEnv.__new__(RobosuiteGymEnv)
        env.task = "Stack"
        env._last_obs_dict = {
            "robot0_eef_pos": np.array([0.0, 0.0, 0.2]),
            "robot0_gripper_qpos": np.array([0.0, 0.0]),
            "cubeA_pos": np.array([0.1, 0.0, 0.82]),
            "cubeB_pos": np.array([0.0, 0.1, 0.82]),
            "gripper_to_cubeA": np.array([0.1, 0.0, -0.1]),
            "gripper_to_cubeB": np.array([0.0, 0.1, -0.1]),
        }

        priv = env.privileged_state()

        np.testing.assert_allclose(priv["cubeA_pos"], [0.1, 0.0, 0.82])
        np.testing.assert_allclose(priv["cubeB_pos"], [0.0, 0.1, 0.82])
        np.testing.assert_allclose(priv["gripper_to_cubeA"], [0.1, 0.0, -0.1])
        np.testing.assert_allclose(priv["gripper_to_cubeB"], [0.0, 0.1, -0.1])


class StackOracleTest(unittest.TestCase):
    def test_stack_oracle_reaches_toward_cube_a_before_stacking(self):
        oracle = ScriptedLiftOracle(action_dim=7, task="Stack", pos_gain=10.0)
        priv = {
            "eef_pos": np.array([0.0, 0.0, 0.9]),
            "cubeA_pos": np.array([0.1, 0.0, 0.82]),
            "cubeB_pos": np.array([0.0, 0.1, 0.82]),
            "gripper_qpos": np.array([0.0, 0.0]),
        }

        action = oracle.act(priv)

        self.assertGreater(action[0], 0.5)
        self.assertLess(abs(action[1]), 0.1)
        self.assertLess(action[6], 0.0)


class StackPhaseGuardTest(unittest.TestCase):
    def test_stack_phase_guard_blocks_far_initial_approach(self):
        priv = {
            "task": "Stack",
            "eef_pos": np.array([0.4, 0.4, 1.0]),
            "cubeA_pos": np.array([0.1, 0.0, 0.82]),
            "cubeB_pos": np.array([0.0, 0.1, 0.82]),
        }

        self.assertFalse(stack_phase_guard_allows(priv, "stack_pick_place"))

    def test_stack_phase_guard_allows_pick_window(self):
        priv = {
            "task": "Stack",
            "eef_pos": np.array([0.11, 0.0, 0.89]),
            "cubeA_pos": np.array([0.1, 0.0, 0.82]),
            "cubeB_pos": np.array([0.0, 0.1, 0.82]),
        }

        self.assertTrue(stack_phase_guard_allows(priv, "stack_pick_place"))

    def test_stack_phase_guard_allows_lifted_cube_near_place_window(self):
        priv = {
            "task": "Stack",
            "eef_pos": np.array([0.01, 0.1, 0.98]),
            "cubeA_pos": np.array([0.01, 0.1, 0.94]),
            "cubeB_pos": np.array([0.0, 0.1, 0.82]),
        }

        self.assertTrue(stack_phase_guard_allows(priv, "stack_pick_place"))


if __name__ == "__main__":
    unittest.main()
