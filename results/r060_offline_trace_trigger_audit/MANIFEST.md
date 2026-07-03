# R060 Offline Trace Trigger Audit

Date: 2026-07-03

## Purpose

R060 executes the cheap trace/offline diagnostic step recommended by R059. It
uses existing R023/R024 intervention-start traces to audit whether simple
counterfactual gates would reduce LV-VoI intervention starts toward the
cost-matched random baseline.

This package does not add a new training run, edit historical CSVs, change
manuscript numerical claims, add citation keys, or support a positive LV-VoI
method claim.

## Inputs

| Source | Role |
|---|---|
| `results/r023_real_trace_seed0_2/trace_Lift_random_b350_seed*.csv` | Random b350 intervention-start reference. |
| `results/r023_real_trace_seed0_2/trace_Lift_voi_b600_seed*.csv` | Original LV-VoI scale3 intervention-start traces. |
| `results/r024_score_floor_seed0_2/trace_Lift_voi_b600_seed*.csv` | Observed score-floor repair intervention-start traces. |
| `results/r059_evidence_experiment_optimization/MANIFEST.md` | Planning source for the trace/offline audit route. |

## Outputs

| Artifact | Purpose |
|---|---|
| `phase_trace_summary.csv` | Phase-binned start counts and medians for random, original LV-VoI, and score-floor traces. |
| `offline_gate_audit.csv` | Post-hoc gate audit rows and observed-trace reference rows. |
| `offline_audit_decision_matrix.csv` | Decision rows translating the offline audit into next-experiment rules. |
| `TRACE_OFFLINE_AUDIT.md` | Human-readable audit narrative, limitations, and recommendation. |
| `foresight_hil/evaluation/offline_trace_audit.py` | Tested helper module for trace audit tables. |
| `scripts/generate_offline_trace_audit.py` | Regenerates this R060 package. |
| `tests/test_offline_trace_audit.py` | Regression tests for the R060 helper behavior. |

## Claim Boundary

R060 is diagnostic evidence about recorded intervention-start traces. It can
support statements about trace-level start counts, post-hoc gate retention, and
why accepted-start filtering should not be treated as online performance
evidence.

R060 does not support claims that a counterfactual gate improves success rate,
that score-floor LV-VoI is a positive method result, or that trace filtering
overturns the R021 cost-matched random dominance.

## Regeneration

```powershell
python scripts\generate_offline_trace_audit.py
```

## Verification Record

Executed on 2026-07-03 after R060 code, registry, and documentation updates:

| Command | Result |
|---|---|
| `python scripts\generate_claim_tables.py` | PASS: regenerated 5 R036 claim-table assets. |
| `python scripts\generate_methodology_extension.py` | PASS: regenerated 3 R056 CSVs and 2 LaTeX tables. |
| `python scripts\generate_offline_trace_audit.py` | PASS: regenerated 5 R060 audit artifacts. |
| `python scripts\generate_stack_boundary_appendix.py` | PASS: regenerated 2 R053 Stack appendix assets. |
| `python scripts\validate_evidence_registry.py` | PASS: 51 rows, 51 sources, 0 issues. |
| `python scripts\audit_registry_numbers.py` | PASS: 94 numeric checks, 0 issues. |
| `python scripts\validate_provenance_package.py` | PASS: 6 checks, 289 files, 0 issues. |
| `python scripts\validate_document_links.py` | PASS: 135 documents, 33 links, 0 issues. |
| `python -m unittest discover -s tests` | PASS: 89 tests. A Gym deprecation warning was printed and is not a current test failure. |
| `git diff --check` | PASS: no whitespace errors; Git printed line-ending normalization warnings for generated text assets. |
