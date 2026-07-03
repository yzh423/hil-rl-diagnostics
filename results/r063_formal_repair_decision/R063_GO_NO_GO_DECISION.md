# R063-P0 Formal Repair Go/No-Go Decision

Date: 2026-07-03

## Decision

**NO-GO for formal online trigger repair before the current submission.**

The project should not launch a formal R064+ online repair from the current
state. R062 proved that candidate-state logging works, but it did not identify
a new trigger mechanism that is likely to beat the cost-matched random family.
The current manuscript is stronger as a diagnostic-protocol paper than as a
method-repair paper.

## Why This Is The Right Default

| Question | Current evidence | Decision implication |
|---|---|---|
| Is the current paper claim already supported? | Yes. R021 rejects LV-VoI superiority under cost matching; R022/R024 show two repairs remain dominated; R023/R024 explain failure modes. | New repair training is not required for the current thesis. |
| Did R062 create a method candidate? | No. It created logging readiness only: 14 candidate rows, 8 accepted and 6 rejected in a tiny smoke. | R062 should not be promoted into method evidence. |
| Is a simple extension promising? | No. R060 shows post-hoc score filtering can look selective while R024 online score-floor still over-spends and remains dominated. | Do not expand score-floor or accepted-start filters. |
| Would a formal run answer a manuscript-critical risk now? | Not under the current T-ASE diagnostic route. Packaging, claim audit, and final visual QA are higher leverage. | Defer formal repair compute. |
| Would a negative formal repair harm the paper? | It could add clutter, compute burden, and another negative result without changing the main contribution. | Keep the paper compact. |

## Disallowed Immediate Experiments

Do not launch a formal online repair that is only:

- another score-floor threshold sweep;
- another minimum-disagreement threshold sweep;
- an accepted-start post-hoc filter turned into an online claim;
- a phase-only gate;
- a hard budget cap described as a positive trigger method;
- a training run without a frozen trigger rule and cost-matched random
  comparison.

## Go Conditions For Future R064+

A future formal online repair can be reconsidered only if all of these become
true:

1. There is a concrete reviewer, advisor, venue, or thesis-risk reason that the
   current diagnostic paper needs a positive repair attempt.
2. The trigger rule is frozen before launch and is mechanistically distinct from
   R022 minimum-disagreement and R024 score-floor repairs.
3. The rule is specified using candidate-state information available online,
   not only post-hoc accepted-start filters.
4. The implementation is tested separately before training.
5. The run plan includes exact command logging, stdout/stderr archival,
   candidate-state traces, intervention traces, repeated checkpoint evaluation,
   and a registry row before manuscript use.
6. The comparison includes cost-matched `random_b350` or an explicitly justified
   stronger random-family baseline.
7. The stop rule is accepted in advance: if the repair does not beat
   cost-matched random at similar or lower human-step cost, it remains a
   negative repair/diagnostic result.

## Recommended Next Work

Prioritize submission-readiness work:

1. Keep the current diagnostic manuscript route.
2. Rerun PDF compile and visual QA after any venue-template or layout change.
3. Run a final paper-claim audit if captions, numerical claims, comparison
   claims, or scope claims change.
4. Create a final institutional/source archive only from a clean verified
   submission tag.

## Manuscript Boundary

R063 can support process language such as "we pre-registered and rejected a
formal repair expansion under the current submission route." It cannot support
claims that any trigger improves performance, beats random, generalizes to
Stack, uses real humans, or transfers to real robots.
