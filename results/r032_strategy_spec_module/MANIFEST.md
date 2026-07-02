# R032 Strategy Spec Module Manifest

Date: 2026-07-02

Purpose: record the code audit and strategy-specification module extraction.

| File | Purpose |
|---|---|
| `CODE_AUDIT_AND_FRAMEWORK_REVIEW.md` | All-code audit findings, R032 change boundary, review notes, and next optimization queue. |

Repo-level files added or updated in this step:

| File | Purpose |
|---|---|
| `foresight_hil/experiments/strategy_specs.py` | Declarative strategy identity and training CLI construction. |
| `foresight_hil/experiments/__init__.py` | Exports the strategy-spec interface. |
| `scripts/run_comparison.py` | Delegates strategy labels, run tags, and CLI args to the strategy-spec module. |
| `tests/test_strategy_specs.py` | Direct tests for strategy order, pace flags, run labels, run tags, and CLI args. |
| `CONTEXT.md` | Updates current module-deepening state. |
| `PROJECT_STRUCTURE.md` | Adds R032 and marks strategy specification done first pass. |
| `results/RESULTS_INDEX.md` | Adds R032 to project-structure support artifacts. |
| `refine-logs/EXPERIMENT_TRACKER.md` | Adds R032 milestone row. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Adds R032 support row. |
