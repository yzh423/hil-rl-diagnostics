"""Strategy identity and training CLI construction for comparison runs."""

from __future__ import annotations


DEFAULT_COMPARISON_STRATEGIES = ("none", "always", "random", "voi")
BUDGET_PACED_STRATEGIES = frozenset(("random", "voi"))


def label_value(value):
    return str(value).replace(".", "p")


def strategy_extra_flags(strategy):
    """Extra training flags implied by a comparison strategy."""
    if str(strategy) in BUDGET_PACED_STRATEGIES:
        return ["--pace", "linear"]
    return []


def strategy_pace_label(strategy):
    return "linear" if str(strategy) in BUDGET_PACED_STRATEGIES else "none"


def build_driver_run_label(args, strategy):
    """Run label used by the comparison driver for resumable run identity."""
    late_reg_coef = (
        args.bc_actor_reg_coef
        if args.bc_actor_reg_late_coef is None
        else args.bc_actor_reg_late_coef
    )
    return (
        f"steps{args.total_steps}_demo{args.n_demos}_ls{args.learning_starts}"
        f"_bs{args.batch_size}_gs{args.gradient_steps}"
        f"_bc{args.bc_pretrain_steps}_reg{label_value(args.bc_actor_reg_coef)}"
        f"_regs{args.bc_actor_reg_schedule}"
        f"_lreg{label_value(late_reg_coef)}"
        f"_lstart{label_value(args.bc_actor_reg_late_start_frac)}"
        f"_take{args.takeover_len}"
        f"_vtau{label_value(args.voi_tau)}"
        f"_vcq{label_value(args.voi_cquery)}"
        f"_vref{args.voi_reference_policy}"
        f"_vlv{label_value(args.voi_learning_value_scale)}"
        f"_vclip{label_value(args.voi_learning_value_clip)}"
        f"_vlvmin{label_value(args.voi_learning_value_min_disagreement)}"
        f"_vsfloorstep{label_value(args.voi_score_floor_after_step)}"
        f"_vsfloor{label_value(args.voi_score_floor_after_value)}"
        f"_vphase{args.voi_phase_guard}"
        f"_idemomode{args.intervention_demo_mode}"
        f"_restorebest{int(bool(args.restore_best_model_at_end))}"
        f"_pace{strategy_pace_label(strategy)}"
    )


def comparison_run_identity(args, seed, strategy):
    """Return `(run_label, run_tag)` for a driver-managed training run."""
    run_label = build_driver_run_label(args, strategy)
    run_tag = f"{args.task}_{strategy}_b{args.budget}_seed{seed}_{run_label}"
    return run_label, run_tag


def build_training_cli_args(args, seed, strategy, run_label=None):
    """Build CLI args for `scripts/train_robosuite_hil.py`.

    The order intentionally mirrors the historical driver output so run logs
    remain easy to compare across R020-R032.
    """
    if run_label is None:
        run_label = build_driver_run_label(args, strategy)

    cmd = [
        "--task", args.task,
        "--strategy", strategy,
        "--budget", str(args.budget),
        "--total_steps", str(args.total_steps),
        "--n_demos", str(args.n_demos),
        "--learning_starts", str(args.learning_starts),
        "--batch_size", str(args.batch_size),
        "--gradient_steps", str(args.gradient_steps),
        "--intervention_demo_mode", args.intervention_demo_mode,
        "--bc_pretrain_steps", str(args.bc_pretrain_steps),
        "--bc_pretrain_batch_size", str(args.bc_pretrain_batch_size),
        "--bc_actor_reg_coef", str(args.bc_actor_reg_coef),
        "--bc_actor_reg_every", str(args.bc_actor_reg_every),
        "--bc_actor_reg_schedule", args.bc_actor_reg_schedule,
        "--bc_actor_reg_late_start_frac", str(args.bc_actor_reg_late_start_frac),
        "--takeover_len", str(args.takeover_len),
        "--voi_tau", str(args.voi_tau),
        "--voi_cquery", str(args.voi_cquery),
        "--voi_reference_policy", args.voi_reference_policy,
        "--voi_reference_max_points", str(args.voi_reference_max_points),
        "--voi_learning_value_scale", str(args.voi_learning_value_scale),
        "--voi_learning_value_clip", str(args.voi_learning_value_clip),
        "--voi_learning_value_min_disagreement",
        str(args.voi_learning_value_min_disagreement),
        "--voi_score_floor_after_step", str(args.voi_score_floor_after_step),
        "--voi_score_floor_after_value", str(args.voi_score_floor_after_value),
        "--voi_phase_guard", args.voi_phase_guard,
        "--eval_every", str(args.eval_every),
        "--eval_episodes", str(args.eval_episodes),
        "--run_label", run_label,
        "--out_dir", args.out_dir,
        "--seed", str(seed),
    ]
    cmd.extend(strategy_extra_flags(strategy))
    if args.bc_actor_reg_late_coef is not None:
        cmd.extend(["--bc_actor_reg_late_coef", str(args.bc_actor_reg_late_coef)])
    if args.eval_at_start:
        cmd.append("--eval_at_start")
    if args.restore_best_model_at_end:
        cmd.append("--restore_best_model_at_end")
    if args.trace_interventions:
        cmd.append("--trace_interventions")
    if getattr(args, "trace_candidates", False):
        cmd.append("--trace_candidates")
    return cmd
