# R028 Framework Decision

Date: 2026-07-02

Status: accepted for pre-draft planning.

## Decision

Frame the paper as a **protocol-centered diagnostic paper** for HIL-RL
intervention-trigger evaluation in robotic manipulation.

The paper should not present itself primarily as:

- a positive method paper claiming that the current LV-VoI trigger wins;
- a generic negative-result report about one failed method;
- a broad benchmark suite across many simulators and tasks.

Instead, the paper's identity is:

> HIL-RL intervention triggers can appear efficient under weak evaluation, but
> the conclusion can reverse after cost-matched random baselines, repeated
> checkpoint evaluation, and trace-level intervention diagnostics. We make this
> failure mode concrete in a robotic manipulation case study and turn it into a
> reusable evaluation protocol.

## Working Title Direction

Preferred:

**When Cost Matching Changes the Conclusion: A Diagnostic Evaluation Protocol
for Human-in-the-Loop RL Intervention Triggers in Robotic Manipulation**

Alternatives:

1. **Cost-Matched Diagnostics for Human-in-the-Loop Reinforcement Learning in
   Robotic Manipulation**
2. **Before Claiming Better Intervention Triggers: Cost-Matched Diagnostics for
   HIL-RL**
3. **When Intervention Triggers Fail: Cost-Matched Evaluation for HIL-RL in
   Robotic Manipulation**

The first title is strongest because it foregrounds the scientific lesson
rather than the failed trigger.

## Contribution Hierarchy

1. **Protocol contribution**: cost-matched random families, repeated checkpoint
   evaluation, and trace-level intervention diagnostics as a minimum evaluation
   standard for HIL-RL trigger claims.
2. **Case-study evidence**: a seemingly plausible model-based LV-VoI trigger is
   dominated by `random_b350` on robosuite Lift after cost matching.
3. **Mechanism diagnosis**: trace diagnostics show over-triggering and
   score/timing mismatch, not a simple far-from-object trigger failure.
4. **Redesign gate**: future trigger variants should stop unless they pass
   same-seed cost-matched random and repeated-evaluation gates.

## Why This Framing Is Stronger

- It converts the negative result into a reusable evaluation lesson.
- It avoids overclaiming method novelty unsupported by R021-R024.
- It keeps the robotics anchor through robosuite Lift/Stack and scripted
  intervention traces.
- It gives reviewers a concrete artifact to evaluate: the protocol and its
  diagnostic metrics.

## Alternatives Rejected

### Positive LV-VoI Method Paper

Rejected because R021 `random_b350` dominates LV-VoI scale3: `439/500 = 87.8%`
at cost 177.0 versus `416/500 = 83.2%` at cost 202.0.

### Negative-Findings-Only Paper

Rejected because it undersells the contribution. The stronger story is not that
one trigger fails; it is that a weak evaluation protocol would have made the
trigger look better than it is.

### New-Method Redesign Paper

Rejected for now because R022 and R024 are negative. A new method would need a
substantially different trigger mechanism and must first pass the R021/R024
gates.

### Broad Robotics Benchmark Paper

Rejected for now because task breadth is limited. Stack is useful as boundary
evidence, not as a positive generalization result.

## Immediate Consequence

Before drafting, update all paper-planning artifacts so that "negative findings"
are treated as evidence inside a diagnostic-protocol paper, not as the paper's
main identity.
