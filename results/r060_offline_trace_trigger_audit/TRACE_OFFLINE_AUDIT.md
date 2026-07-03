# R060 Offline Trace Trigger Audit

Date: 2026-07-03

## Verdict

The offline audit is useful as a design screen, but it does not justify a new
positive method claim. The strongest result is a cautionary one: post-hoc
filtering of accepted LV-VoI starts can look aggressive, while the actual
online score-floor repair still spends nearly as many starts and remains
dominated in R024.

Observed start counts:

| Trace | Starts | Relation to random target |
|---|---:|---|
| R023 random b350 | 55 | Reference |
| R023 LV-VoI scale3 | 96 | 41 above random |
| R024 observed score-floor LV-VoI | 94 | 39 above random |

## Key Offline Findings

| Gate / comparison | Retained starts | Excess vs random | Interpretation |
|---|---:|---:|---|
| Post-hoc score >=0.05 after 4k on R023 LV-VoI | 30 | -25 | Looks like it would over-reduce historical accepted starts, but actual R024 replacement dynamics contradict this as an online budget predictor. |
| Keep only starts after 4k | 84 | 29 | Phase-only filtering removes early starts but leaves substantial over-triggering. |
| Drop score >=9.9 saturation | 84 | 29 | Saturation is a diagnostic symptom, not enough by itself to match random spending. |
| Budget fraction <=0.60 | 60 | 5 | A hard cap can nearly match the start-count target, but gives no success-rate evidence. |
| Earliest count cap matching random starts | 55 | 0 | Matches count by construction; useful only as a control-design reminder. |

## Decision Matrix

| ID | Observation | Recommendation |
|---|---|---|
| D1 | Post-hoc score floor keeps 30 of 96 R023 LV-VoI starts, but the actual R024 score-floor run still records 94 starts. | Do not expand the existing score-floor repair; require candidate-state logs or a new cost-matched online run before claiming a better trigger. |
| D2 | Phase-only gating after 4k keeps 84 starts, leaving 29 starts above the random target. | Use phase information only as one component of a future pre-registered gate. |
| D3 | Budget fraction <=0.60 keeps 60 starts, while an earliest-count cap keeps 55 starts to match random. | Treat cost caps as experimental-control tools, not positive method evidence. |
| D4 | Dropping saturated score >=9.9 keeps 84 starts, still 29 above the random target. | Keep score saturation as a failure signal in the paper, not as a validated repair. |

## Boundary

These rows are derived from intervention-start traces only. They do not include
the full sequence of non-triggered candidate states, and they do not replay the
policy after a counterfactual rejection. Therefore, they should be used to
choose or reject future experiments, not to claim online trigger performance.

The next online experiment should be launched only if a gate is pre-registered,
logs accepted and rejected candidate states, and is compared against the
cost-matched random family before manuscript prose changes.
