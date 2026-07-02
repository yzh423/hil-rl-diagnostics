import unittest
from types import SimpleNamespace

from foresight_hil.experiments.strategy_specs import (
    DEFAULT_COMPARISON_STRATEGIES,
    build_driver_run_label,
    build_training_cli_args,
    comparison_run_identity,
    strategy_extra_flags,
)


def args_for(**overrides):
    base = dict(
        task="Lift",
        budget=350,
        total_steps=10000,
        n_demos=20,
        learning_starts=500,
        batch_size=256,
        gradient_steps=1,
        intervention_demo_mode="all",
        bc_pretrain_steps=5000,
        bc_pretrain_batch_size=256,
        bc_actor_reg_coef=50.0,
        bc_actor_reg_every=1,
        bc_actor_reg_schedule="constant",
        bc_actor_reg_late_coef=None,
        bc_actor_reg_late_start_frac=0.5,
        takeover_len=20,
        voi_tau=0.01,
        voi_cquery=0.0,
        voi_reference_policy="demo_nn",
        voi_reference_max_points=2048,
        voi_learning_value_scale=3.0,
        voi_learning_value_clip=1.0,
        voi_learning_value_min_disagreement=0.25,
        voi_score_floor_after_step=4000,
        voi_score_floor_after_value=0.05,
        voi_phase_guard="none",
        eval_every=10000,
        eval_episodes=20,
        eval_at_start=False,
        restore_best_model_at_end=True,
        trace_interventions=True,
        out_dir="results/r032_smoke",
    )
    base.update(overrides)
    return SimpleNamespace(**base)


class StrategySpecsTest(unittest.TestCase):
    def test_default_comparison_strategies_are_canonical_order(self):
        self.assertEqual(DEFAULT_COMPARISON_STRATEGIES,
                         ("none", "always", "random", "voi"))

    def test_strategy_extra_flags_only_pace_budgeted_strategies(self):
        self.assertEqual(strategy_extra_flags("none"), [])
        self.assertEqual(strategy_extra_flags("always"), [])
        self.assertEqual(strategy_extra_flags("random"), ["--pace", "linear"])
        self.assertEqual(strategy_extra_flags("voi"), ["--pace", "linear"])

    def test_driver_run_label_keeps_scientific_config_identity(self):
        label = build_driver_run_label(args_for(), "voi")

        self.assertIn("steps10000_demo20_ls500", label)
        self.assertIn("reg50p0", label)
        self.assertIn("take20", label)
        self.assertIn("vtau0p01", label)
        self.assertIn("vrefdemo_nn", label)
        self.assertIn("vlv3p0", label)
        self.assertIn("vlvmin0p25", label)
        self.assertIn("vsfloorstep4000", label)
        self.assertIn("vsfloor0p05", label)
        self.assertIn("restorebest1", label)
        self.assertTrue(label.endswith("_pacelinear"))

    def test_comparison_run_identity_matches_training_run_tag_shape(self):
        run_label, run_tag = comparison_run_identity(args_for(), seed=2, strategy="random")

        self.assertTrue(run_tag.startswith("Lift_random_b350_seed2_"))
        self.assertIn(run_label, run_tag)
        self.assertTrue(run_label.endswith("_pacelinear"))

    def test_training_cli_args_include_strategy_flags_and_optional_booleans(self):
        args = args_for()
        run_label, _ = comparison_run_identity(args, seed=0, strategy="voi")
        cli = build_training_cli_args(args, seed=0, strategy="voi", run_label=run_label)

        self.assertIn("--pace", cli)
        self.assertIn("linear", cli)
        self.assertIn("--restore_best_model_at_end", cli)
        self.assertIn("--trace_interventions", cli)
        self.assertIn("--run_label", cli)
        self.assertEqual(cli[cli.index("--run_label") + 1], run_label)
        self.assertEqual(cli[cli.index("--strategy") + 1], "voi")


if __name__ == "__main__":
    unittest.main()
