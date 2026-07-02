# R030 Structure Audit

Date: 2026-07-02

Question: after the R028/R029 paper-framing pivot, what project-structure and
low-risk code-structure changes improve reliability without changing experiment
behavior?

## Findings

1. The main research route is now clear, but navigation was split across
   `README.md`, `PAPER_PLAN.md`, `refine-logs/EXPERIMENT_TRACKER.md`, figure
   manifests, and result directories.
2. `results/` is now a large evidence archive. Without a human-readable index,
   it is easy to confuse paper-core runs with smoke or superseded runs.
3. `figures/` contains both R026 and R029 assets. The preferred Fig. 1 changed
   after R029, but that preference was not visible from a single figure index.
4. `scripts/train_robosuite_hil.py` is the central shallow module. Its interface
   is broad because one script owns configuration, trace schema, training,
   evaluation, and summary output. Before R030 it also owned run identity and
   checkpoint bookkeeping.
5. There was no `CONTEXT.md` or decision record explaining the current route,
   so future agents could easily revive the obsolete positive-superiority
   framing.

## Optimizations Applied

| File | Purpose |
|---|---|
| `CONTEXT.md` | Adds project vocabulary, claim rules, and architecture terms. |
| `PROJECT_STRUCTURE.md` | Adds a top-level navigation map and module-deepening candidates. |
| `results/RESULTS_INDEX.md` | Separates paper-core, historical, and smoke result artifacts. |
| `figures/FIGURE_ASSET_INDEX.md` | Consolidates R026/R029 figure and table assets. |
| `docs/decisions/ADR-001-paper-facing-artifact-indexes.md` | Records the decision to keep paper-facing indexes and registries as stable interfaces. |
| `README.md` | Adds links to the new structure and result indexes. |
| `refine-logs/EXPERIMENT_TRACKER.md` | Adds R030 as a completed structure milestone. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Adds R030 as a project-structure support row. |
| `foresight_hil/experiments/bookkeeping.py` | Extracts run labels, summary upsert, best-checkpoint metadata, final-policy selection, BC regularization schedule, and intervention-demo replay mode. |
| `tests/test_experiment_bookkeeping_module.py` | Adds direct tests for the new bookkeeping module interface. |

## Module Deepening Candidates

| Candidate | Recommendation | Why |
|---|---|---|
| Experiment bookkeeping module | Done first pass | Best-checkpoint selection, run labels, summary rows, and final-report policy now live behind `foresight_hil/experiments/bookkeeping.py`. |
| Trace schema module | Strong | Trace fields are part of the diagnostic protocol. A stable interface reduces claim drift and makes tests easier. |
| Strategy specification module | Worth exploring | Random budget families and LV-VoI flags should be declared once so drivers and training agree. |
| Evaluation protocol module | Worth exploring | Repeated checkpoint summaries and Wilson intervals are central paper contributions and should not stay scattered. |
| Registry generator | Speculative | Useful after the manuscript draft stabilizes; premature automation could encode the wrong claim shape. |

## Recommended Next Step

R031 should extract the trace schema from `scripts/train_robosuite_hil.py` with
tests first. The safe interface is:

- `INTERVENTION_TRACE_FIELDS`;
- `_trace_float` and `_trace_vec`;
- `intervention_trace_row`;
- task-specific geometry fields for Lift and Stack.

This avoids touching SAC updates, oracle behavior, dynamics fitting, or trigger
logic while reducing the highest-friction module.

## Stop Rule

Do not start a new trigger method in the same step as structural refactoring.
Keep scientific changes and architecture changes separate so future results can
be trusted.
