# Formal Repair Entry Criteria For Future R064+

Date: 2026-07-03

## Purpose

This file defines what must be true before the project can spend compute on a
future formal online repair experiment. It prevents R062 logging readiness from
being mistaken for a method candidate.

## Entry Checklist

| Gate | Requirement | Current status |
|---|---|---|
| Manuscript need | A reviewer/advisor/venue or thesis-risk reason requires a positive repair attempt. | Not present. |
| Mechanism | The trigger rule is substantially different from R022 and R024. | Not present. |
| Online observability | The rule uses candidate-state information available during training. | Possible after R061/R062, but no rule is frozen. |
| Tests | Any new implementation is covered before training. | Not applicable yet. |
| Logging | Candidate-state traces, intervention traces, commands, stdout/stderr, and environment/source state are archived. | Logging interface ready; formal plan absent. |
| Baseline | Cost-matched `random_b350` or stronger random-family comparison is included. | Required, not planned. |
| Evaluation | Repeated checkpoint evaluation is included before manuscript use. | Required, not planned. |
| Stop rule | Failure to beat cost-matched random remains a negative diagnostic result. | Required. |

## Forbidden Shortcuts

- Do not treat smoke success rate as evidence.
- Do not tune thresholds after seeing formal results and call the result
  pre-registered.
- Do not launch a repair in the same step as a training-script refactor.
- Do not compare only against LV-VoI scale3.
- Do not use a budget cap by itself as a positive method claim.

## Minimal Future Design Shape

If the no-go decision is later reversed, the next artifact should be a fresh
R064+ pre-registration that states:

- exact trigger rule;
- exact compared systems;
- seeds and checkpoint-evaluation plan;
- target human-step cost range;
- primary and secondary metrics;
- command templates;
- expected compute;
- stop and interpretation rules.

No training should begin until that R064+ pre-registration exists.
