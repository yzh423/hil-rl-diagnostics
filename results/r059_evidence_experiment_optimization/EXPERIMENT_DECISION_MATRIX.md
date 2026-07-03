# R059 Experiment Decision Matrix

Date: 2026-07-03

## Current Decision

Do not add a broad new experiment by default before submission. R058 resolves
the current PDF/packaging gate, and R060 executes the first trace/offline audit.
R061 now adds candidate-state logging, and R062 records the smoke and
pre-registration gate. R063 records no-go for formal repair before the current
submission. If an experiment is still needed later, it should be a narrowly
pre-registered R064+ online repair with that logging and cost matching.

## Options

| Option | Run now? | Why |
|---|---|---|
| Fix PDF compile and visual QA | Yes | Required before credible submission packaging. |
| Final paper-claim audit after PDF compile | Yes, if text/captions change | Prevents unsupported scope or numerical claims. |
| Offline R023/R024 counterfactual trigger audit | Done in R060 | Low compute; directly uses the failure diagnosis while preserving the no-online-claim boundary. |
| More R021-style cost-matched seeds | Useful if negative-result robustness is challenged | Strengthens the current conclusion but costs compute. |
| New phase/contact-aware online trigger | Only after the R063 no-go is explicitly reversed and a pre-registered R064+ design exists | Could become a positive repair, but must log accepted/rejected candidate states and beat `random_b350`. |
| Additional robotics task beyond Stack | Defer unless venue/advisor demands it | Adds breadth but also adds evidence, prose, and verification burden. |
| Refactor training script before new experiments | No, unless separately tested | Avoids coupling behavior changes with new scientific results. |

## Selection Rule

Pick the next experiment by this order:

1. Does it answer a concrete reviewer/submission risk?
2. Does it preserve cost matching and repeated evaluation?
3. Does it have a registered baseline stronger than LV-VoI?
4. Can it be logged and audited without editing historical evidence?
5. Is it cheaper than a broader robotics-breadth run?

If the answer to any item is no, keep the work as a planning note rather than a
paper-facing result.
