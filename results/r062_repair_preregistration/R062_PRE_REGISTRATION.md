# R062 Pre-Registration For Candidate-Logged Repair Evaluation

Date: 2026-07-03

## Verdict

Do not launch a formal online repair as R062. R062 is the readiness gate:
confirm that candidate-state logging can be archived and that the next formal
experiment has a frozen rule, cost-matched comparison, and stop criteria before
spending compute.

Formal online repair evidence, if still needed, should start after a separate
go/no-go decision and after any new trigger rule is implemented in a separate
tested change.

## Frozen Context

| Prior result | Boundary it imposes |
|---|---|
| R021 | `random_b350` is the current cost-matched Lift baseline to beat. |
| R022 | Minimum-disagreement LV-VoI remains negative and should not be expanded as-is. |
| R023 | Accepted intervention starts diagnose timing/geometry/score patterns but do not provide rejected candidate states. |
| R024 | Score-floor LV-VoI remains dominated and still records nearly the same number of starts as original LV-VoI. |
| R060 | Post-hoc accepted-start filtering can be misleading as an online-performance predictor. |
| R061 | Future VoI runs can now log accepted and rejected gate-evaluated candidate states. |

## Claim Map

| Claim | Minimum convincing evidence | Status after R062 |
|---|---|---|
| Candidate-state logging is ready for a formal repair run. | A smoke run writes a candidate trace with the R061 schema, nonempty gate-evaluation rows, and interpretable accepted/rejected or score-floor decision fields. | R062-S0 smoke passed: 14 candidate rows, 8 accepted and 6 `gate_not_candidate` rejected. |
| A future repair improves attention allocation. | Fresh online result directory, exact commands/logs, repeated checkpoint evaluation, candidate trace, intervention trace, registry row, and cost-matched comparison to `random_b350`. | Not tested by R062. |
| The current diagnostic paper can remain evidence-first without new training. | R021/R022/R024 remain negative and R060/R061 only affect design readiness. | Supported as a process boundary. |

## Anti-Claims

R062 explicitly does not claim:

- LV-VoI superiority over cost-matched random baselines;
- score-floor or minimum-disagreement repair success;
- that post-hoc accepted-start filters predict online performance;
- that a smoke run is paper evidence;
- real-human or real-robot validation.

## R062 Smoke Gate

The only run eligible under R062 is `R062-S0`, a tiny local smoke whose purpose
is to verify logging, not learning:

- run with both `--trace_candidates` and `--trace_interventions`;
- write outputs under `results/r062_repair_preregistration/smoke_local/`;
- archive stdout/stderr if executed;
- inspect the candidate trace for schema, nonempty gate evaluations, accepted
  rows, and at least one rejected-state reason when available;
- do not copy smoke success rates into the manuscript or claim tables.

R062-S0 produced candidate rows and rejected-state coverage. The optional
score-floor smoke is therefore not needed.

## Formal-Run Gate

A formal online repair should be created only when all items below are true:

1. R062-S0 candidate logging smoke has passed.
2. The exact trigger rule is frozen before launch.
3. Any new trigger implementation is tested before training starts.
4. The run archives exact commands, stdout/stderr, Git commit or source state,
   environment summary, run CSV, intervention trace, candidate trace, and
   repeated-evaluation outputs.
5. The comparison set includes cost-matched `random_b350` or an explicitly
   justified stronger random-family match.
6. The stop rule is registered: if the repair fails to beat the cost-matched
   random baseline at similar or lower realized human-step cost, it remains a
   negative repair/diagnostic result.

## Manuscript Use

Use R062 only to describe experimental discipline for future work. Do not add a
new method-performance sentence, abstract claim, or figure caption from R062
unless a later registered R064+ result supplies empirical evidence and the
paper-claim audit is updated.
