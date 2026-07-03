"""Experiment orchestration helpers for FORESIGHT-HIL."""

from .bookkeeping import (
    SUMMARY_RESULT_FIELDS,
    best_eval_cost_metadata,
    build_run_tag,
    choose_reported_final_eval,
    config_run_label,
    effective_bc_actor_reg_coef,
    maybe_save_best_checkpoint,
    sanitize_run_label,
    should_add_intervention_demo,
    write_summary_row,
)
from .trace import (
    CANDIDATE_TRACE_FIELDS,
    INTERVENTION_TRACE_FIELDS,
    candidate_trace_row,
    intervention_trace_row,
)
from .strategy_specs import (
    DEFAULT_COMPARISON_STRATEGIES,
    build_driver_run_label,
    build_training_cli_args,
    comparison_run_identity,
    strategy_extra_flags,
)

__all__ = [
    "DEFAULT_COMPARISON_STRATEGIES",
    "CANDIDATE_TRACE_FIELDS",
    "INTERVENTION_TRACE_FIELDS",
    "SUMMARY_RESULT_FIELDS",
    "best_eval_cost_metadata",
    "build_run_tag",
    "build_driver_run_label",
    "build_training_cli_args",
    "candidate_trace_row",
    "choose_reported_final_eval",
    "comparison_run_identity",
    "config_run_label",
    "effective_bc_actor_reg_coef",
    "maybe_save_best_checkpoint",
    "sanitize_run_label",
    "should_add_intervention_demo",
    "strategy_extra_flags",
    "intervention_trace_row",
    "write_summary_row",
]
