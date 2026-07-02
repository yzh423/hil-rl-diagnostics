# R031 Trace Schema Module Manifest

Date: 2026-07-02

Purpose: record the trace-schema module extraction.

| File | Purpose |
|---|---|
| `TRACE_SCHEMA_MODULE.md` | Rationale, interface, compatibility note, and next target. |

Repo-level files added or updated in this step:

| File | Purpose |
|---|---|
| `foresight_hil/experiments/trace.py` | New trace schema and row-construction module. |
| `foresight_hil/experiments/__init__.py` | Exports the trace interface. |
| `scripts/train_robosuite_hil.py` | Imports trace interface instead of owning implementation. |
| `tests/test_experiment_trace_module.py` | Direct tests for trace interface and Stack geometry rows. |
| `CONTEXT.md` | Updates current module-deepening state. |
| `PROJECT_STRUCTURE.md` | Adds R031 and marks trace schema done. |
| `results/RESULTS_INDEX.md` | Adds R031 to project-structure support artifacts. |
| `refine-logs/EXPERIMENT_TRACKER.md` | Adds R031 milestone row. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Adds R031 support row. |
