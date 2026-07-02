# R032 Code Audit and Framework Review

Date: 2026-07-02

Purpose: continue the all-code review after R030/R031 and apply one low-risk
framework optimization without changing scientific behavior.

## Codebase Findings

| Area | Finding | Action |
|---|---|---|
| `scripts/train_robosuite_hil.py` | Still the largest shallow module at about 49 KB, but R030/R031 removed bookkeeping and trace schema. | Continue extracting experiment protocol helpers before touching training logic. |
| `scripts/run_comparison.py` | Driver owned strategy pace flags, run-label construction, run-tag identity, and training CLI construction. This created configuration-drift risk for cost-matched experiments. | R032 extracted strategy identity and CLI construction into `foresight_hil/experiments/strategy_specs.py`. |
| `foresight_hil/experiments/` | Now has three experiment-protocol modules: bookkeeping, trace, and strategy specs. | Treat this package as the stable interface for experiment orchestration. |
| `tests/` | Existing tests cover bookkeeping and trace compatibility. Strategy identity had only indirect coverage through `run_comparison.py`. | R032 added direct strategy-spec tests. |
| `results/` and `figures/` | Paper-facing artifacts now have indexes, but registry rows are still curated manually. | Defer registry generation until manuscript draft stabilizes. |

## R032 Change

R032 adds `foresight_hil/experiments/strategy_specs.py` with this interface:

- `DEFAULT_COMPARISON_STRATEGIES`
- `strategy_extra_flags(strategy)`
- `build_driver_run_label(args, strategy)`
- `comparison_run_identity(args, seed, strategy)`
- `build_training_cli_args(args, seed, strategy, run_label=None)`

`scripts/run_comparison.py` now imports that interface instead of owning the
strategy specification implementation. The old `build_driver_run_label` name is
still available from `scripts.run_comparison` because it is imported at module
scope, preserving existing tests and callers.

## Behavior Boundary

This is a structural refactor only. It preserves:

- canonical strategy order: `none`, `always`, `random`, `voi`;
- budget pacing only for `random` and `voi`;
- historical driver run-label tokens;
- optional driver flags such as `--restore_best_model_at_end`,
  `--trace_interventions`, and `--eval_at_start`;
- training script behavior.

## Review Notes

- Correctness: the new tests verify strategy order, pace flags, label identity,
  run-tag identity, and CLI boolean flags.
- Architecture: strategy identity now has one module interface, improving
  locality for cost-matched evaluation changes.
- Security: no new external input surface and no new dependency.
- Performance: no hot-path change; command construction happens once per run.

## Next Optimization Queue

| Priority | Target | Reason |
|---|---|---|
| 1 | Evaluation protocol module | Repeated checkpoint summaries and Wilson intervals are central to the paper but split across scripts and `metrics.py`. |
| 2 | Driver dry-run / command-plan output | Cost-matched batches would benefit from a machine-readable planned-run table before launching hours-long jobs. |
| 3 | Registry validation helper | Useful after manuscript draft stabilizes; should check that registry primary sources exist and parse. |
| 4 | Training-loop extraction | Larger risk; defer until experiment protocol modules are stable. |
