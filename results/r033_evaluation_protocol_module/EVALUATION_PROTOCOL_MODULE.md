# R033 Evaluation Protocol Module

Date: 2026-07-02

Purpose: move repeated-checkpoint evaluation summary logic into a reusable
module because it is part of the paper's diagnostic protocol, not merely a CLI
script detail.

## Change

R033 adds `foresight_hil/evaluation/protocol.py` with this interface:

- `summarize_repeats(rows)`
- `repeat_summary_row(checkpoint, task, summary)`

`scripts/evaluate_checkpoint.py` now imports these functions and keeps only CLI,
checkpoint loading, environment evaluation, and CSV IO.

## Behavior Boundary

This is a structural refactor only. It preserves:

- total success/episode aggregation;
- mean and standard deviation for repeated success rates and returns;
- Wilson confidence intervals through `foresight_hil.metrics.wilson_interval`;
- summary CSV column names and formatting;
- the legacy `scripts.evaluate_checkpoint.summarize_repeats` import path.

## Why This Matters

Repeated checkpoint evaluation is a central claim-support rule in the current
paper framing. Keeping its aggregation logic behind a dedicated module improves
locality: figure scripts, registry validation, and future paper-table builders
can reuse the same tested implementation.

## Tests

R033 adds `tests/test_evaluation_protocol.py` for:

- count aggregation;
- variance aggregation;
- Wilson CI presence;
- summary-row formatting;
- empty-input validation.

Existing `tests/test_checkpoint_reeval.py` still verifies the old script-level
import path.

## Next Candidate

R034 should add a registry/source validation helper that checks whether every
`results/EXPERIMENT_EVIDENCE_REGISTRY.csv` primary source exists and, for CSV
sources, parses cleanly. This would directly reduce paper-claim drift.
