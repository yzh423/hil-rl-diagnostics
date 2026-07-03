# R062 Repair Pre-Registration And Candidate-Logging Smoke Plan

Date: 2026-07-03

## Purpose

R062 turns the R060/R061 lesson into a pre-experiment gate before any new
online trigger repair. It freezes the claim boundary, required logs, smoke-test
pass criteria, and escalation rule for future R063+ online repair experiments.

This package now includes one tiny candidate-logging smoke run. It does not
run a formal training experiment, edit historical CSVs, change manuscript
numerical claims, add citation keys, or support a positive LV-VoI method
claim.

## Inputs

| Source | Role |
|---|---|
| `results/r021_random_costmatch/r021_costmatch_aggregate.csv` | Current cost-matched Lift reversal: `random_b350` dominates LV-VoI scale3. |
| `results/r022_lift_min_disagree_seed0_2/r022_min_disagree_aggregate.csv` | Negative minimum-disagreement repair boundary. |
| `results/r023_real_trace_seed0_2/` | Accepted-start trace diagnosis for random b350 and LV-VoI scale3. |
| `results/r024_score_floor_seed0_2/` | Negative score-floor repair and observed score-floor trace follow-up. |
| `results/r060_offline_trace_trigger_audit/TRACE_OFFLINE_AUDIT.md` | Shows accepted-start post-hoc filtering is only a design screen. |
| `results/r061_candidate_state_logging/CANDIDATE_STATE_LOGGING_DESIGN.md` | Defines accepted/rejected candidate-state logging for future VoI runs. |

## Outputs

| Artifact | Purpose |
|---|---|
| `R062_PRE_REGISTRATION.md` | Claim map, anti-claims, formal-run gate, and R063+ escalation rule. |
| `CANDIDATE_LOGGING_SMOKE_PLAN.md` | Candidate-state logging smoke command, required artifacts, and pass/fail criteria. |
| `SMOKE_RESULT.md` | R062-S0 execution result, artifact inventory, and gate checks. |
| `EXPERIMENT_TRACKER.md` | Execution tracker separating R062 smoke validation from future R063+ online repairs. |
| `smoke_local/candidate_trace_Lift_voi_b40_seed0_r062_candidate_trace_smoke.csv` | Candidate-state trace from the tiny smoke: accepted and rejected gate evaluations. |
| `smoke_local/trace_Lift_voi_b40_seed0_r062_candidate_trace_smoke.csv` | Intervention-start trace from the tiny smoke. |
| `smoke_local/run_Lift_voi_b40_seed0_r062_candidate_trace_smoke.csv` | Run CSV from the tiny smoke; not paper evidence. |
| `smoke_local/robosuite_hil_summary.csv` | Summary CSV from the tiny smoke; not paper evidence. |
| `smoke_local/r062_candidate_trace_smoke_console.log` | Captured console log for the tiny smoke. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Registers R062 as a planning and pre-registration artifact row. |

## Current Verdict

R062-S0 passed the logging-readiness gate: the tiny smoke wrote 14 candidate
trace rows, including 8 accepted rows and 6 `gate_not_candidate` rejected rows.
It does not make a formal online repair eligible by itself.

A future R063+ online repair must be separately pre-registered after the smoke
pass, must archive accepted and rejected candidate-state traces, and must be
compared against the cost-matched random family before manuscript claims can
change.

## Claim Boundary

R062 can support statements that the project has pre-registered the logging
and audit requirements for a future online repair. It cannot support claims
that a trigger improves success rate, beats random, generalizes to Stack, uses
real humans, or transfers to a real robot.
