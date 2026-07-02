import math
import unittest

import numpy as np

from foresight_hil.hil.intervention import InterventionController
from foresight_hil.gating.reference_policy import (
    DemoNearestActionPolicy,
    demo_arrays_from_mixed_buffer,
)
from foresight_hil.gating.voi_gate import VoIGate
from foresight_hil.metrics import wilson_interval


class StaticGate:
    def __init__(self, candidate=True, score=0.25, p_fail=0.75):
        self.candidate = candidate
        self.score = score
        self.p_fail = p_fail

    def candidates(self, states, policy):
        n = np.atleast_2d(states).shape[0]
        return (
            np.full(n, self.candidate, dtype=bool),
            np.full(n, self.score, dtype=float),
            np.full(n, self.p_fail, dtype=float),
        )


class OneStepDynamics:
    fitted = True

    def __init__(self, next_value):
        self.next_value = float(next_value)

    def predict_all(self, states, actions):
        states = np.atleast_2d(states).astype(np.float32)
        out = np.full((3, states.shape[0], states.shape[1]),
                      self.next_value, dtype=np.float32)
        return out


def zero_policy(states):
    return np.zeros((np.atleast_2d(states).shape[0], 1), dtype=np.float32)


def zero_policy_2d(states):
    return np.zeros((np.atleast_2d(states).shape[0], 2), dtype=np.float32)


def ones_reference_policy(states):
    return np.ones((np.atleast_2d(states).shape[0], 2), dtype=np.float32)


def first_state_value(states):
    states = np.atleast_2d(states)
    return states[:, 0]


class MetricsTest(unittest.TestCase):
    def test_wilson_interval_keeps_low_n_zero_honest(self):
        low, high = wilson_interval(0, 5)
        self.assertEqual(low, 0.0)
        self.assertGreater(high, 0.4)
        self.assertLess(high, 0.5)

    def test_wilson_interval_is_bounded(self):
        low, high = wilson_interval(20, 20)
        self.assertGreater(low, 0.8)
        self.assertEqual(high, 1.0)


class InterventionDiagnosticsTest(unittest.TestCase):
    def test_voi_records_last_gate_decision(self):
        controller = InterventionController(
            "voi", gate=StaticGate(True, 0.25, 0.75),
            budget=10, total_steps=100, takeover_len=2,
        )

        acted = controller.step(np.array([1.0, 2.0]), zero_policy)

        self.assertTrue(acted)
        self.assertTrue(controller.last_intervened)
        self.assertTrue(controller.last_started)
        self.assertTrue(controller.last_candidate)
        self.assertTrue(math.isclose(controller.last_score, 0.25))
        self.assertTrue(math.isclose(controller.last_p_fail, 0.75))

    def test_ongoing_takeover_is_not_a_new_gate_candidate(self):
        controller = InterventionController(
            "voi", gate=StaticGate(True, 0.25, 0.75),
            budget=10, total_steps=100, takeover_len=2,
        )
        controller.step(np.array([1.0, 2.0]), zero_policy)

        acted = controller.step(np.array([1.0, 2.0]), zero_policy)

        self.assertTrue(acted)
        self.assertTrue(controller.last_intervened)
        self.assertFalse(controller.last_started)
        self.assertFalse(controller.last_candidate)
        self.assertTrue(math.isnan(controller.last_score))

    def test_score_floor_blocks_low_score_after_step(self):
        controller = InterventionController(
            "voi", gate=StaticGate(True, 0.02, 0.25),
            budget=10, total_steps=100, takeover_len=1,
            voi_score_floor_after_step=2,
            voi_score_floor_after_value=0.05,
        )

        first = controller.step(np.array([1.0, 2.0]), zero_policy)
        second = controller.step(np.array([1.0, 2.0]), zero_policy)

        self.assertTrue(first)
        self.assertFalse(second)
        self.assertTrue(controller.last_candidate)
        self.assertTrue(math.isclose(controller.last_score, 0.02))
        self.assertTrue(controller.last_score_floor_blocked)
        self.assertEqual(controller.score_floor_blocks, 1)
        self.assertEqual(controller.spent, 1)
        self.assertEqual(controller.engagements, 1)

    def test_score_floor_preserves_high_score_after_step(self):
        controller = InterventionController(
            "voi", gate=StaticGate(True, 0.08, 0.25),
            budget=10, total_steps=100, takeover_len=1,
            voi_score_floor_after_step=1,
            voi_score_floor_after_value=0.05,
        )

        acted = controller.step(np.array([1.0, 2.0]), zero_policy)

        self.assertTrue(acted)
        self.assertFalse(controller.last_score_floor_blocked)
        self.assertEqual(controller.score_floor_blocks, 0)

    def test_score_floor_defaults_to_previous_voi_behavior(self):
        controller = InterventionController(
            "voi", gate=StaticGate(True, 0.02, 0.25),
            budget=10, total_steps=100, takeover_len=1,
        )

        first = controller.step(np.array([1.0, 2.0]), zero_policy)
        second = controller.step(np.array([1.0, 2.0]), zero_policy)

        self.assertTrue(first)
        self.assertTrue(second)
        self.assertFalse(controller.last_score_floor_blocked)
        self.assertEqual(controller.score_floor_blocks, 0)


class VoIGateStabilityTest(unittest.TestCase):
    def test_near_zero_value_baseline_does_not_explode_score(self):
        gate = VoIGate(
            OneStepDynamics(next_value=-0.1),
            value_fn=first_state_value,
            mode="value",
            horizon=1,
            c_query=0.0,
            value_scale_floor=1.0,
            score_clip=10.0,
        )

        score, p_like = gate.voi(np.array([[0.0]], dtype=np.float32), zero_policy)

        self.assertLess(float(score[0]), 1.0)
        self.assertAlmostEqual(float(p_like[0]), 0.1, places=5)

    def test_score_clip_bounds_extreme_value_scores(self):
        gate = VoIGate(
            OneStepDynamics(next_value=-100.0),
            value_fn=first_state_value,
            mode="value",
            horizon=1,
            c_query=0.0,
            value_scale_floor=1.0,
            score_clip=2.0,
        )

        score, _ = gate.voi(np.array([[0.0]], dtype=np.float32), zero_policy)

        self.assertEqual(float(score[0]), 2.0)

    def test_learning_value_multiplier_rewards_policy_reference_disagreement(self):
        base_gate = VoIGate(
            OneStepDynamics(next_value=-1.0),
            value_fn=first_state_value,
            mode="value",
            horizon=1,
            c_query=0.0,
            value_scale_floor=1.0,
            learning_value_scale=0.0,
        )
        learning_gate = VoIGate(
            OneStepDynamics(next_value=-1.0),
            value_fn=first_state_value,
            mode="value",
            horizon=1,
            c_query=0.0,
            value_scale_floor=1.0,
            reference_policy=ones_reference_policy,
            learning_value_scale=2.0,
            learning_value_clip=1.0,
        )

        base_score, _ = base_gate.voi(np.array([[0.0]], dtype=np.float32), zero_policy_2d)
        learning_score, _ = learning_gate.voi(
            np.array([[0.0]], dtype=np.float32), zero_policy_2d)

        self.assertAlmostEqual(float(base_score[0]), 1.0)
        self.assertAlmostEqual(float(learning_score[0]), 3.0)

    def test_min_reference_disagreement_masks_low_learning_value_candidates(self):
        gate = VoIGate(
            OneStepDynamics(next_value=-1.0),
            value_fn=first_state_value,
            mode="value",
            horizon=1,
            c_query=0.0,
            tau=0.5,
            value_scale_floor=1.0,
            reference_policy=zero_policy_2d,
            learning_value_scale=2.0,
            learning_value_min_disagreement=0.5,
        )

        candidate, score, _ = gate.candidates(
            np.array([[0.0]], dtype=np.float32), zero_policy_2d)

        self.assertGreater(float(score[0]), 0.5)
        self.assertFalse(bool(candidate[0]))


class ReferencePolicyTest(unittest.TestCase):
    def test_demo_nearest_action_policy_returns_nearest_demo_action(self):
        observations = np.array([[0.0, 0.0], [10.0, 0.0]], dtype=np.float32)
        actions = np.array([[0.1, 0.2], [0.9, 1.0]], dtype=np.float32)
        policy = DemoNearestActionPolicy(observations, actions, normalize=False)

        out = policy(np.array([[9.0, 0.0], [0.2, 0.0]], dtype=np.float32))

        np.testing.assert_allclose(out, np.array([[0.9, 1.0], [0.1, 0.2]], dtype=np.float32))

    def test_demo_arrays_from_mixed_buffer_extracts_valid_prefix(self):
        class FakeDemo:
            observations = np.arange(24, dtype=np.float32).reshape(4, 1, 6)
            actions = np.arange(12, dtype=np.float32).reshape(4, 1, 3)

        class FakeMixed:
            demo = FakeDemo()

            def demo_size(self):
                return 3

        obs, acts = demo_arrays_from_mixed_buffer(FakeMixed())

        self.assertEqual(obs.shape, (3, 6))
        self.assertEqual(acts.shape, (3, 3))
        np.testing.assert_allclose(obs[2], np.array([12, 13, 14, 15, 16, 17], dtype=np.float32))


if __name__ == "__main__":
    unittest.main()
