import csv
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from scripts.plot_results import (
    SUPPORTED_SUCCESS_METRICS,
    dedupe_rows,
    human_cost_for_metric,
)
from scripts.run_comparison import build_driver_run_label
from scripts.train_robosuite_hil import (
    best_eval_cost_metadata,
    build_run_tag,
    choose_reported_final_eval,
    effective_bc_actor_reg_coef,
    intervention_trace_row,
    maybe_save_best_checkpoint,
    should_add_intervention_demo,
    write_summary_row,
)


def args_for(**overrides):
    base = dict(
        task="Lift",
        strategy="voi",
        budget=1000,
        seed=0,
        total_steps=5000,
        n_demos=20,
        learning_starts=500,
        batch_size=128,
        gradient_steps=1,
        bc_pretrain_steps=5000,
        bc_actor_reg_coef=50.0,
        bc_actor_reg_schedule="constant",
        bc_actor_reg_late_coef=None,
        voi_reference_policy="none",
        voi_learning_value_scale=0.0,
        voi_learning_value_clip=1.0,
        voi_learning_value_min_disagreement=0.0,
        voi_score_floor_after_step=0,
        voi_score_floor_after_value=0.0,
        voi_phase_guard="none",
        intervention_demo_mode="all",
        pace="linear",
        run_label="",
        auto_run_label=True,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


class RunTagTest(unittest.TestCase):
    def test_auto_run_label_changes_with_bc_regularization(self):
        tag_a, _ = build_run_tag(args_for(bc_actor_reg_coef=10.0))
        tag_b, _ = build_run_tag(args_for(bc_actor_reg_coef=50.0))

        self.assertNotEqual(tag_a, tag_b)
        self.assertIn("reg10p0", tag_a)
        self.assertIn("reg50p0", tag_b)

    def test_auto_run_label_changes_with_bc_schedule(self):
        tag_a, _ = build_run_tag(args_for(bc_actor_reg_schedule="constant"))
        tag_b, _ = build_run_tag(args_for(
            bc_actor_reg_schedule="linear_late",
            bc_actor_reg_late_coef=150.0))

        self.assertNotEqual(tag_a, tag_b)
        self.assertIn("regsconstant", tag_a)
        self.assertIn("lreg50p0", tag_a)
        self.assertNotIn("lregNone", tag_a)
        self.assertIn("regslinear_late", tag_b)
        self.assertIn("lreg150p0", tag_b)

    def test_auto_run_label_changes_with_restore_best_flag(self):
        tag_a, _ = build_run_tag(args_for(restore_best_model_at_end=False))
        tag_b, _ = build_run_tag(args_for(restore_best_model_at_end=True))

        self.assertNotEqual(tag_a, tag_b)
        self.assertIn("restorebest0", tag_a)
        self.assertIn("restorebest1", tag_b)

    def test_auto_run_label_changes_with_learning_value_gate(self):
        tag_a, _ = build_run_tag(args_for(voi_reference_policy="none"))
        tag_b, _ = build_run_tag(args_for(
            voi_reference_policy="demo_nn",
            voi_learning_value_scale=2.0,
            voi_learning_value_min_disagreement=0.25))

        self.assertNotEqual(tag_a, tag_b)
        self.assertIn("vrefnone", tag_a)
        self.assertIn("vrefdemo_nn", tag_b)
        self.assertIn("vlv2p0", tag_b)
        self.assertIn("vlvmin0p25", tag_b)

    def test_auto_run_label_changes_with_voi_score_floor(self):
        tag_a, _ = build_run_tag(args_for())
        tag_b, _ = build_run_tag(args_for(
            voi_score_floor_after_step=4000,
            voi_score_floor_after_value=0.05))

        self.assertNotEqual(tag_a, tag_b)
        self.assertIn("vsfloorstep0", tag_a)
        self.assertIn("vsfloor0p0", tag_a)
        self.assertIn("vsfloorstep4000", tag_b)
        self.assertIn("vsfloor0p05", tag_b)

    def test_auto_run_label_changes_with_intervention_demo_mode(self):
        tag_a, _ = build_run_tag(args_for(intervention_demo_mode="all"))
        tag_b, _ = build_run_tag(args_for(intervention_demo_mode="starts"))

        self.assertNotEqual(tag_a, tag_b)
        self.assertIn("idemomodeall", tag_a)
        self.assertIn("idemomodestarts", tag_b)

    def test_driver_run_label_tracks_voi_and_takeover_config(self):
        base = dict(
            total_steps=10000,
            n_demos=20,
            learning_starts=500,
            batch_size=256,
            gradient_steps=1,
            bc_pretrain_steps=5000,
            bc_actor_reg_coef=50.0,
            bc_actor_reg_schedule="constant",
            bc_actor_reg_late_coef=None,
            bc_actor_reg_late_start_frac=0.5,
            restore_best_model_at_end=True,
            takeover_len=20,
            voi_tau=0.01,
            voi_cquery=0.0,
            voi_reference_policy="demo_nn",
            voi_learning_value_scale=2.0,
            voi_learning_value_clip=1.0,
            voi_learning_value_min_disagreement=0.25,
            voi_score_floor_after_step=4000,
            voi_score_floor_after_value=0.05,
            voi_phase_guard="none",
            intervention_demo_mode="all",
        )

        label = build_driver_run_label(SimpleNamespace(**base), "voi")

        self.assertIn("take20", label)
        self.assertIn("vtau0p01", label)
        self.assertIn("vcq0p0", label)
        self.assertIn("vrefdemo_nn", label)
        self.assertIn("vlv2p0", label)
        self.assertIn("vlvmin0p25", label)
        self.assertIn("vsfloorstep4000", label)
        self.assertIn("vsfloor0p05", label)
        self.assertIn("vphasenone", label)
        self.assertIn("restorebest1", label)
        self.assertIn("idemomodeall", label)


class SummaryUpsertTest(unittest.TestCase):
    def test_write_summary_row_replaces_same_config(self):
        header = [
            "task", "strategy", "budget", "seed", "run_label",
            "final_success_rate", "best_success_rate", "wall_time_s",
        ]
        first = ["Lift", "voi", 1000, 0, "cfg", "0.1000", "0.2000", "10.0"]
        second = ["Lift", "voi", 1000, 0, "cfg", "0.6000", "0.9000", "12.0"]

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "summary.csv"
            write_summary_row(path, header, first)
            write_summary_row(path, header, second)

            with path.open(newline="") as f:
                rows = list(csv.DictReader(f))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["final_success_rate"], "0.6000")
        self.assertEqual(rows[0]["best_success_rate"], "0.9000")


class BestCheckpointTest(unittest.TestCase):
    def test_saves_first_eval_and_strict_improvements_only(self):
        class FakeModel:
            def __init__(self):
                self.saved = []

            def save(self, path):
                self.saved.append(str(path))

        model = FakeModel()
        path = Path("best_model.zip")

        best_success, best_step, saved = maybe_save_best_checkpoint(
            model, path, step=0, success_rate=0.2,
            best_success=0.0, best_step=None, enabled=True)
        self.assertTrue(saved)
        self.assertEqual(best_success, 0.2)
        self.assertEqual(best_step, 0)
        self.assertEqual(model.saved, [str(path)])

        best_success, best_step, saved = maybe_save_best_checkpoint(
            model, path, step=1000, success_rate=0.2,
            best_success=best_success, best_step=best_step, enabled=True)
        self.assertFalse(saved)
        self.assertEqual(best_success, 0.2)
        self.assertEqual(best_step, 0)
        self.assertEqual(model.saved, [str(path)])

        best_success, best_step, saved = maybe_save_best_checkpoint(
            model, path, step=2000, success_rate=0.6,
            best_success=best_success, best_step=best_step, enabled=True)
        self.assertTrue(saved)
        self.assertEqual(best_success, 0.6)
        self.assertEqual(best_step, 2000)
        self.assertEqual(model.saved, [str(path), str(path)])

    def test_checkpoint_can_be_disabled(self):
        class FakeModel:
            def save(self, path):
                raise AssertionError("save should not be called")

        best_success, best_step, saved = maybe_save_best_checkpoint(
            FakeModel(), Path("best_model.zip"), step=0, success_rate=1.0,
            best_success=0.0, best_step=None, enabled=False)

        self.assertFalse(saved)
        self.assertEqual(best_success, 1.0)
        self.assertEqual(best_step, 0)


class BestEvalCostMetadataTest(unittest.TestCase):
    def test_updates_cost_only_when_best_step_changes_to_current_eval(self):
        current = {"human_steps": 10, "budget_used_frac": "0.1000", "engagements": 1}

        unchanged = best_eval_cost_metadata(
            previous_best_step=1000,
            new_best_step=1000,
            current_step=2000,
            human_steps=80,
            budget_used_frac=0.8,
            engagements=4,
            current=current,
        )
        updated = best_eval_cost_metadata(
            previous_best_step=1000,
            new_best_step=2000,
            current_step=2000,
            human_steps=80,
            budget_used_frac=0.8,
            engagements=4,
            current=current,
        )

        self.assertEqual(unchanged, current)
        self.assertEqual(updated["human_steps"], 80)
        self.assertEqual(updated["budget_used_frac"], "0.8000")
        self.assertEqual(updated["engagements"], 4)


class FinalPolicySelectionTest(unittest.TestCase):
    def test_uses_last_policy_when_no_restored_eval_is_available(self):
        raw = {"success": 0.2, "successes": 4, "episodes": 20}

        chosen, source = choose_reported_final_eval(raw, None)

        self.assertIs(chosen, raw)
        self.assertEqual(source, "last_policy")

    def test_uses_restored_best_policy_when_eval_is_available(self):
        raw = {"success": 0.2, "successes": 4, "episodes": 20}
        restored = {"success": 0.8, "successes": 16, "episodes": 20}

        chosen, source = choose_reported_final_eval(raw, restored)

        self.assertIs(chosen, restored)
        self.assertEqual(source, "best_checkpoint")


class BcRegScheduleTest(unittest.TestCase):
    def test_constant_schedule_returns_base_coefficient(self):
        coef = effective_bc_actor_reg_coef(
            step=7500, total_steps=10000, base_coef=50.0,
            schedule="constant", late_coef=150.0, late_start_frac=0.5)

        self.assertEqual(coef, 50.0)

    def test_linear_late_schedule_interpolates_after_start_fraction(self):
        before = effective_bc_actor_reg_coef(
            step=4000, total_steps=10000, base_coef=50.0,
            schedule="linear_late", late_coef=150.0, late_start_frac=0.5)
        middle = effective_bc_actor_reg_coef(
            step=7500, total_steps=10000, base_coef=50.0,
            schedule="linear_late", late_coef=150.0, late_start_frac=0.5)
        end = effective_bc_actor_reg_coef(
            step=10000, total_steps=10000, base_coef=50.0,
            schedule="linear_late", late_coef=150.0, late_start_frac=0.5)

        self.assertEqual(before, 50.0)
        self.assertEqual(middle, 100.0)
        self.assertEqual(end, 150.0)


class InterventionDemoReplayModeTest(unittest.TestCase):
    def test_all_mode_keeps_existing_takeover_demo_replay_behavior(self):
        controller = SimpleNamespace(last_started=False)

        self.assertTrue(should_add_intervention_demo(True, controller, "all"))

    def test_starts_mode_keeps_only_engagement_start_in_demo_replay(self):
        start = SimpleNamespace(last_started=True)
        latched = SimpleNamespace(last_started=False)

        self.assertTrue(should_add_intervention_demo(True, start, "starts"))
        self.assertFalse(should_add_intervention_demo(True, latched, "starts"))
        self.assertFalse(should_add_intervention_demo(False, start, "starts"))

    def test_none_mode_disables_intervention_demo_replay(self):
        controller = SimpleNamespace(last_started=True)

        self.assertFalse(should_add_intervention_demo(True, controller, "none"))


class InterventionTraceTest(unittest.TestCase):
    def test_trace_row_records_budget_gate_and_lift_geometry(self):
        args = SimpleNamespace(task="Lift", strategy="voi", seed=2, budget=600)
        controller = SimpleNamespace(
            spent=80,
            engagements=4,
            last_candidate=True,
            last_score=0.125,
            last_p_fail=0.25,
        )
        priv = {
            "task": "Lift",
            "eef_pos": [0.1, 0.2, 0.9],
            "cube_pos": [0.1, 0.25, 0.82],
            "gripper_to_cube": [0.0, 0.05, -0.08],
        }

        row = intervention_trace_row(
            step=1234, ep_idx=5, ep_len=67,
            args=args, controller=controller, priv=priv)

        self.assertEqual(row["env_step"], 1234)
        self.assertEqual(row["episode"], 5)
        self.assertEqual(row["episode_step"], 67)
        self.assertEqual(row["strategy"], "voi")
        self.assertEqual(row["seed"], 2)
        self.assertEqual(row["human_steps"], 80)
        self.assertEqual(row["engagements"], 4)
        self.assertEqual(row["candidate"], 1)
        self.assertEqual(row["score"], "0.125000")
        self.assertEqual(row["p_fail"], "0.250000")
        self.assertEqual(row["budget_used_frac"], "0.1333")
        self.assertEqual(row["eef_z"], "0.900000")
        self.assertEqual(row["cube_z"], "0.820000")
        self.assertEqual(row["gripper_to_cube_norm"], "0.094340")
        self.assertEqual(row["gripper_to_cube_xy"], "0.050000")


class PlotDedupeTest(unittest.TestCase):
    def test_dedupe_rows_keeps_latest_matching_config(self):
        rows = [
            {"task": "Lift", "strategy": "voi", "seed": "0", "run_label": "cfg",
             "final_success_rate": "0.1", "best_success_rate": "0.2",
             "best_eval_step": "1000", "best_checkpoint_path": "old.zip",
             "human_steps": "10", "engagements": "1"},
            {"task": "Lift", "strategy": "voi", "seed": "0", "run_label": "cfg",
             "final_success_rate": "0.6", "best_success_rate": "0.9",
             "best_eval_step": "2000", "best_checkpoint_path": "new.zip",
             "human_steps": "12", "engagements": "2"},
        ]

        deduped, removed = dedupe_rows(rows)

        self.assertEqual(removed, 1)
        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0]["final_success_rate"], "0.6")

    def test_dedupe_treats_restore_fields_as_results(self):
        rows = [
            {"task": "Lift", "strategy": "voi", "seed": "0", "run_label": "cfg",
             "restore_best_model_at_end": "1",
             "final_success_rate": "0.5", "final_policy_source": "last_policy",
             "raw_final_success_rate": "0.2", "restored_best_success_rate": "",
             "human_steps": "600"},
            {"task": "Lift", "strategy": "voi", "seed": "0", "run_label": "cfg",
             "restore_best_model_at_end": "1",
             "final_success_rate": "0.7", "final_policy_source": "best_checkpoint",
             "raw_final_success_rate": "0.3", "restored_best_success_rate": "0.7",
             "human_steps": "600"},
        ]

        deduped, removed = dedupe_rows(rows)

        self.assertEqual(removed, 1)
        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0]["final_policy_source"], "best_checkpoint")

    def test_raw_final_metric_is_supported_for_plotting(self):
        self.assertIn("raw_final_success_rate", SUPPORTED_SUCCESS_METRICS)

    def test_best_success_metric_uses_best_human_cost_when_available(self):
        row = {"human_steps": "600", "best_human_steps": "80"}

        self.assertEqual(human_cost_for_metric(row, "best_success_rate"), 80.0)
        self.assertEqual(human_cost_for_metric(row, "final_success_rate"), 600.0)


if __name__ == "__main__":
    unittest.main()
