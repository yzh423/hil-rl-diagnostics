# ADR-001: Maintain Paper-Facing Artifact Indexes

## Status

Accepted

## Date

2026-07-02

## Context

The project now contains many raw experiment outputs, paper figure builds,
proposal notes, and research-planning artifacts. After R021-R029, the paper
route changed from a positive LV-VoI superiority claim to a cost-matched
diagnostic protocol with a robotic manipulation case study.

Without stable paper-facing indexes, future work can easily cite smoke runs,
revive superseded claims, or choose the older Fig. 1 candidate by accident.

## Decision

Maintain a small set of paper-facing indexes as the stable interface for future
writing and experiments:

- `CONTEXT.md` for vocabulary and claim rules;
- `PROJECT_STRUCTURE.md` for navigation and module-deepening targets;
- `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` for claim-support rows;
- `results/RESULTS_INDEX.md` for human-readable result provenance;
- `figures/FIGURE_ASSET_INDEX.md` for figure/table provenance.

Raw result directories remain the implementation behind these indexes.

## Alternatives Considered

### Rely only on README

Pros: fewer files.

Cons: README becomes too long and mixes onboarding, claims, commands, and
artifact provenance.

Rejected because the project already needs separate research, result, and figure
interfaces.

### Move or rename historical result directories

Pros: cleaner filesystem.

Cons: high risk of breaking provenance, scripts, and references to historical
outputs.

Rejected because indexes give clarity without mutating evidence archives.

### Refactor training code first

Pros: addresses the largest shallow module.

Cons: code refactoring can change experiment behavior if done before the current
paper-facing evidence structure is stable.

Deferred to R031 with tests.

## Consequences

- Future paper claims should pass through the evidence registry.
- Future figure references should pass through the figure asset index.
- Historical results stay intact.
- R030 completed the first `scripts/train_robosuite_hil.py` bookkeeping
  extraction.
- The next structural code step can focus on trace schema or strategy
  specification with less context ambiguity.
