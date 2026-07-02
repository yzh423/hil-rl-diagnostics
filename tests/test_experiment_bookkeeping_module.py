import csv
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from foresight_hil.experiments.bookkeeping import (
    build_run_tag,
    effective_bc_actor_reg_coef,
    maybe_save_best_checkpoint,
    write_summary_row,
)


def args_for(**overrides):
    base = dict(
        task="Lift",
        strategy="voi",
        budget=600,
        seed=2,
        total_steps=10000,
        n_demos=20,
        learning_starts=500,
        batch_size=256,
        gradient_steps=1,
        bc_pretrain_steps=5000,
        bc_actor_reg_coef=50.0,
        bc_actor_reg_schedule="constant",
        bc_actor_reg_late_coef=None,
        voi_reference_policy="demo_nn",
        voi_learning_value_scale=3.0,
        voi_learning_value_min_disagreement=0.25,
        voi_score_floor_after_step=4000,
        voi_score_floor_after_value=0.05,
        voi_phase_guard="none",
        intervention_demo_mode="all",
        restore_best_model_at_end=True,
        pace="linear",
        run_label="",
        auto_run_label=True,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


class BookkeepingModuleTest(unittest.TestCase):
    def test_module_builds_canonical_run_tags(self):
        tag, label = build_run_tag(args_for())

        self.assertTrue(tag.startswith("Lift_voi_b600_seed2_"))
        self.assertIn("vrefdemo_nn", label)
        self.assertIn("vlv3p0", label)
        self.assertIn("vlvmin0p25", label)
        self.assertIn("vsfloorstep4000", label)
        self.assertIn("restorebest1", label)

    def test_module_upserts_summary_rows_by_non_result_config(self):
        header = [
            "task", "strategy", "budget", "seed", "run_label",
            "best_success_rate", "wall_time_s",
        ]
        first = ["Lift", "voi", 600, 2, "cfg", "0.1", "10.0"]
        second = ["Lift", "voi", 600, 2, "cfg", "0.8", "12.0"]

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "summary.csv"
            write_summary_row(path, header, first)
            write_summary_row(path, header, second)
            with path.open(newline="") as f:
                rows = list(csv.DictReader(f))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["best_success_rate"], "0.8")

    def test_module_tracks_best_checkpoint_without_forcing_save(self):
        class FakeModel:
            def save(self, path):
                raise AssertionError("save should not be called")

        best_success, best_step, saved = maybe_save_best_checkpoint(
            FakeModel(), Path("best.zip"), step=1000, success_rate=0.75,
            best_success=0.0, best_step=None, enabled=False)

        self.assertFalse(saved)
        self.assertEqual(best_success, 0.75)
        self.assertEqual(best_step, 1000)

    def test_module_computes_linear_late_bc_regularization(self):
        coef = effective_bc_actor_reg_coef(
            step=7500, total_steps=10000, base_coef=50.0,
            schedule="linear_late", late_coef=150.0, late_start_frac=0.5)

        self.assertEqual(coef, 100.0)


if __name__ == "__main__":
    unittest.main()
