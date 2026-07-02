# R029 Hero Figure Rationale

## Design Goal

The old Fig. 1 summarized the diagnostic story, but the paper's refined R028
identity needs the first figure to show the protocol contribution explicitly.
The new candidate figure should make the reader see three facts in order:

1. the paper proposes a diagnostic protocol, not a new winning trigger;
2. cost matching changes the Lift conclusion;
3. trace diagnostics explain the failure mode.

## Candidate Figure Structure

- **Panel A: Protocol gates.** A compact checklist of the five required gates:
  cost-matched random family, repeated checkpoint evaluation, best/final policy
  accounting, trace diagnostics, and same-seed stop gate.
- **Panel B: Cost-matched reversal.** The main quantitative result:
  `random_b350` achieves higher repeated success and lower best-step human cost
  than LV-VoI scale3.
- **Panel C: Trace diagnosis.** Intervention-start count and gripper-to-cube
  distance show that the issue is over-triggering/score timing mismatch, not a
  simple far-from-cube failure.

## Caption Draft

Diagnostic protocol for HIL-RL intervention-trigger claims. The proposed
protocol requires cost-matched random families, repeated checkpoint evaluation,
best/final policy accounting, trace-level intervention diagnostics, and a
same-seed stop gate before expansion. Applied to robosuite Lift, the protocol
reverses an initially plausible LV-VoI conclusion: `random_b350` reaches higher
repeated success at lower best-step human cost than LV-VoI scale3. Trace
diagnostics show that LV-VoI starts more interventions while starting closer to
the cube, rejecting a simple far-from-object explanation and pointing instead
to insufficient selectivity and score/timing mismatch.

## Use Rule

Use this figure as the manuscript's Fig. 1 if the final paper keeps the R028
protocol-centered framing. Keep the older R026 Fig. 1 only as a fallback or
supplement if this protocol figure becomes too dense in the target template.
