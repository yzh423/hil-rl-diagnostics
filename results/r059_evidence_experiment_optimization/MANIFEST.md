# R059 Evidence And Experiment Optimization Plan

Date: 2026-07-03

## Purpose

R059 records a gated route for improving evidence strength and deciding which
future experiments, if any, should be run after the current manuscript and
packaging gates are stable.

This package is a plan and decision artifact. It does not add a new experiment,
change raw evidence, change manuscript numerical claims, add citation keys, or
change the protected negative LV-VoI result boundary.

## Inputs Reviewed

| Artifact | Role |
|---|---|
| R021 | Current decisive cost-matched Lift reversal. |
| R022 | Negative minimum-disagreement repair. |
| R023 | Start-level trace diagnosis for random_b350 and LV-VoI scale3. |
| R024 | Negative score-floor repair and trace follow-up. |
| R053 | Stack boundary appendix. |
| R054 | Attention-allocation diagnostic figure and trace profile. |
| R056 | Protocol gate matrix, failure taxonomy, and stop-rule metrics. |
| R058 | Submission packaging and compile-readiness gate. |

## Outputs

| Artifact | Purpose |
|---|---|
| `results/r059_evidence_experiment_optimization/EVIDENCE_EXPERIMENT_OPTIMIZATION_PLAN.md` | Ordered evidence and experiment optimization route with stop gates. |
| `results/r059_evidence_experiment_optimization/EXPERIMENT_DECISION_MATRIX.md` | Decision matrix for selecting the next experiment without overclaiming. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Registers R059 as a planning/experiment-design artifact row. |

## Current Verdict

The next optimization should be evidence-first, not method-first:

1. complete submission/runtime gates from R058;
2. harden provenance and claim audits around existing evidence;
3. run cheap trace/offline diagnostics from R023/R024 before launching new
   training; R060 now executes the first accepted-start offline audit;
4. only run new training if it answers a manuscript-critical question under the
   cost-matched protocol.

The default near-term recommendation is not to add robotics breadth before
submission unless the target venue, advisor, or reviewer feedback explicitly
requires it. The current Stack appendix is enough as boundary evidence for the
diagnostic-protocol paper route. After R060, any new online repair should add
accepted and rejected candidate-state logging and remain cost-matched against
the random family before it can change manuscript claims.

## Claim Boundary

R059 is not empirical evidence. It is a decision and planning artifact for
future evidence generation.
