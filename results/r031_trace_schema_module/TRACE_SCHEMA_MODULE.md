# R031 Trace Schema Module

Date: 2026-07-02

Purpose: deepen the experiment-trace module without changing training behavior.

## Change

R031 extracts intervention trace schema and row construction from
`scripts/train_robosuite_hil.py` into `foresight_hil/experiments/trace.py`.

The new module interface is:

- `INTERVENTION_TRACE_FIELDS`
- `intervention_trace_row(step, ep_idx, ep_len, args, controller, priv)`

The training script imports these names, so existing callers and tests that use
`scripts.train_robosuite_hil.intervention_trace_row` remain compatible.

## Why This Matters

Trace diagnostics are now part of the paper's diagnostic protocol. Keeping the
schema in a dedicated module improves locality: changes to trace columns,
geometry fields, or formatting can be tested without reading the training loop.

This is a structural refactor only. It does not change:

- SAC training;
- oracle behavior;
- intervention trigger logic;
- budget accounting;
- CSV field names or formatting.

## Tests

Added `tests/test_experiment_trace_module.py` to exercise the new module
interface directly, including Stack geometry fields.

Existing `tests/test_experiment_bookkeeping.py` still imports the old training
script entry point and verifies compatibility.

## Next Candidate

R032 should extract declarative strategy specifications. The repeated
cost-matching work has shown that random-budget families and LV-VoI flags are a
scientific risk if driver and training scripts drift.
