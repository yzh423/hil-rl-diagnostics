# R062 Experiment Tracker

Date: 2026-07-03

| Run ID | Milestone | Purpose | Priority | Status | Decision Gate |
|---|---|---|---|---|---|
| R062-S0 | Candidate logging smoke | Verify `--trace_candidates` writes nonempty gate-evaluation rows in a tiny Lift VoI run. | MUST | PASS: 14 candidate rows, 8 accepted, 6 rejected | Satisfies logging smoke prerequisite for the R063-P0 go/no-go decision. |
| R062-S0b | Optional rejection-coverage smoke | Use an existing score-floor setting only if S0 has no rejected rows. | CONDITIONAL | Not needed | S0 already exercised rejected-state logging. |
| R063-P0 | Formal repair go/no-go decision | Decide whether a formal online repair is manuscript-critical after the logging smoke. | MUST BEFORE TRAINING | NO-GO for current submission route | Do not train unless future go conditions are met. |
| R064-P0 | Future repair pre-registration | Freeze the exact trigger rule, baseline comparison, repeated-eval plan, and stop rule if repair becomes necessary. | CONDITIONAL | Not started | Needed before launching any future online repair compute. |
| R064+ | Future formal online repair | Test a pre-registered trace-derived repair against cost-matched random-family evidence. | OPTIONAL | Not eligible yet | Eligible only after R064-P0 and tested implementation if new code is needed. |

## Current Status

R062-S0 has been executed as a smoke only. It confirms candidate-state logging
coverage for accepted and rejected gate-evaluated rows, but it does not support
any method-performance claim. R063-P0 later records no-go for formal online
repair before the current submission.
