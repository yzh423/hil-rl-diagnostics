# R061 Candidate-State Logging Interface

Date: 2026-07-03

## Purpose

R061 implements the logging prerequisite identified by R060 before any future
online trigger repair. The new candidate-state trace records every VoI gate
evaluation, including accepted starts and rejected candidate states, so future
offline audits are not limited to accepted intervention starts.

This package does not add a new training run, edit historical CSVs, change
manuscript numerical claims, add citation keys, or support a positive LV-VoI
method claim.

## Inputs

| Source | Role |
|---|---|
| `results/r060_offline_trace_trigger_audit/TRACE_OFFLINE_AUDIT.md` | Identifies accepted-start-only filtering as insufficient for online claims. |
| `foresight_hil/hil/intervention.py` | Source of intervention decisions and gate metadata. |
| `foresight_hil/experiments/trace.py` | Existing intervention-start trace schema and geometry helpers. |
| `scripts/train_robosuite_hil.py` | Training entry point that writes run and trace CSVs. |

## Outputs

| Artifact | Purpose |
|---|---|
| `foresight_hil/experiments/trace.py` | Adds `CANDIDATE_TRACE_FIELDS` and `candidate_trace_row`. |
| `foresight_hil/hil/intervention.py` | Adds per-step gate-evaluation metadata and rejection reasons. |
| `scripts/train_robosuite_hil.py` | Adds `--trace_candidates` and `--candidate_trace_path` CSV writing. |
| `scripts/run_comparison.py` | Adds driver-level `--trace_candidates` support. |
| `foresight_hil/experiments/strategy_specs.py` | Allows comparison drivers to pass `--trace_candidates`. |
| `tests/test_experiment_trace_module.py` | Tests candidate trace schema and rejected-state row construction. |
| `tests/test_metrics_and_intervention.py` | Tests gate-evaluation metadata and rejection reasons. |
| `tests/test_strategy_specs.py` | Tests driver CLI propagation for candidate tracing. |
| `tests/test_run_comparison_cli.py` | Tests driver parser support for candidate tracing. |
| `results/r061_candidate_state_logging/CANDIDATE_STATE_LOGGING_DESIGN.md` | Records the interface, intended use, and boundaries. |

## Claim Boundary

R061 is instrumentation and design infrastructure. It can support future claims
that a run archived accepted and rejected VoI gate-evaluation states. It cannot
support any claim that a trigger improves success rate, beats random, or
generalizes to real humans or real robots.

Any future R063+ online repair still needs a fresh result directory, exact
command logs, candidate-state traces, repeated evaluation, cost-matched random
comparison, registry rows, and claim audit before manuscript prose changes.
R062 should be used first as the candidate-logging smoke and pre-registration
gate.

## Verification Record

Executed on 2026-07-03 after R061 code, registry, and documentation updates:

| Command | Result |
|---|---|
| `python -m unittest tests.test_metrics_and_intervention` | PASS: 14 tests. |
| `python -m unittest tests.test_experiment_trace_module` | PASS: 3 tests. |
| `python -m unittest tests.test_strategy_specs` | PASS: 5 tests. |
| `python -m unittest tests.test_run_comparison_cli` | PASS: 1 test. |
| `python scripts\train_robosuite_hil.py --help` | PASS: parser exposes `--trace_candidates` and `--candidate_trace_path`; existing Gym warning printed. |
| `python scripts\run_comparison.py --help` | PASS: parser exposes `--trace_candidates`. |
| `python scripts\generate_claim_tables.py` | PASS: regenerated 5 R036 claim-table assets. |
| `python scripts\generate_methodology_extension.py` | PASS: regenerated 3 R056 CSVs and 2 LaTeX tables. |
| `python scripts\generate_offline_trace_audit.py` | PASS: regenerated 5 R060 audit artifacts. |
| `python scripts\generate_stack_boundary_appendix.py` | PASS: regenerated 2 R053 Stack appendix assets. |
| `python scripts\validate_evidence_registry.py` | PASS: 52 rows, 52 sources, 0 issues. |
| `python scripts\audit_registry_numbers.py` | PASS: 94 numeric checks, 0 issues. |
| `python scripts\validate_provenance_package.py` | PASS: 6 checks, 289 files, 0 issues. |
| `python scripts\validate_document_links.py` | PASS: 137 documents, 35 links, 0 issues. |
| `python -m unittest discover -s tests` | PASS: 92 tests. A Gym deprecation warning was printed and is not a current test failure. |
| `git diff --check` | PASS: no whitespace errors; Git printed line-ending normalization warnings for generated text assets. |
