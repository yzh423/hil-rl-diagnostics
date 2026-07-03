# R063 Formal Repair Go/No-Go Decision

Date: 2026-07-03

## Purpose

R063-P0 decides whether the project should launch a formal online trigger
repair experiment after the R062 candidate-logging smoke. It is a decision and
planning artifact, not a training run.

The current verdict is **NO-GO for formal online repair before submission**.
The diagnostic-protocol paper already has supported evidence for its central
claims, while no frozen, substantially different repair mechanism is ready to
justify new online compute.

## Inputs

| Source | Role |
|---|---|
| `results/r021_random_costmatch/r021_costmatch_aggregate.csv` | Decisive cost-matched Lift reversal and baseline to beat. |
| `results/r022_lift_min_disagree_seed0_2/r022_min_disagree_aggregate.csv` | Negative minimum-disagreement repair boundary. |
| `results/r023_real_trace_seed0_2/` | Trace diagnosis for random b350 and LV-VoI scale3. |
| `results/r024_score_floor_seed0_2/` | Negative score-floor repair and trace follow-up. |
| `results/r059_evidence_experiment_optimization/` | Evidence-first experiment-selection rules. |
| `results/r060_offline_trace_trigger_audit/` | Offline trace audit warning against accepted-start filtering as online evidence. |
| `results/r061_candidate_state_logging/` | Candidate-state logging interface for future online repairs. |
| `results/r062_repair_preregistration/` | Passed candidate-logging smoke and formal-run prerequisites. |
| `paper/PAPER_CLAIM_AUDIT.md` | Current manuscript claim-audit state. |

## Outputs

| Artifact | Purpose |
|---|---|
| `R063_GO_NO_GO_DECISION.md` | Main go/no-go decision, rationale, and next action. |
| `FORMAL_REPAIR_ENTRY_CRITERIA.md` | Conditions that must be met before a future R064+ formal repair can launch. |
| `EXPERIMENT_TRACKER.md` | Tracks the R063-P0 decision and the blocked future R064+ training path. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Registers R063 as a planning/decision artifact row. |

## Current Verdict

Do not launch formal online repair training from the current state. Use the
current manuscript route: cost-matched diagnostic protocol, negative repair
evidence, trace diagnostics, R062 logging readiness, and submission packaging.

If a formal repair becomes necessary later, it should use a fresh R064+ result
directory, a frozen trigger rule, candidate-state traces, repeated checkpoint
evaluation, and cost-matched random comparison.

## Claim Boundary

R063 does not add empirical evidence and does not change manuscript numerical,
comparison, citation, real-human, or real-robot claims.
