# R028 Reviewer Objection Map

Date: 2026-07-02

This file anticipates likely reviewer objections and the minimum response needed
before drafting or submission.

| Objection | Risk | Minimum response | Current status |
|---|---|---|---|
| "There is no positive algorithmic contribution." | High | Frame the paper as a diagnostic protocol paper, not a method paper. Make the protocol checklist and stop/continue rules first-class contributions. | Addressed by R028 framing and reflected in `PAPER_PLAN.md`. |
| "This is just one failed trigger." | High | Show the general evaluation failure mode: R020 looked plausible, R021 cost matching reversed it, R022/R024 repairs also failed, R023 traces explain mechanism. | Evidence exists in R020-R024. |
| "Random is too simple; why is this publishable?" | Medium | The point is precisely that simple baselines must be cost matched. A learned trigger that cannot beat cost-matched random should not be claimed superior. | Needs strong Introduction framing. |
| "Scripted oracle is not a real human." | High | State this early. Claim simulated-HIL diagnostic validity, not real-human deployment. Treat scripted oracle as controlled intervention generator. | Must be explicit in Setup and Limitations. |
| "No real robot experiments." | High for robotics journals | Target as diagnostic/evaluation protocol with robosuite manipulation, or choose an AI/RL/control venue more tolerant of simulation. Do not imply real-robot validation. | Venue choice still open. |
| "Only Lift main result; Stack is negative." | Medium | Use Stack as boundary evidence and appendix limitation. Do not present broad task generalization. | Addressed by claim boundary P5. |
| "Best checkpoint selection may bias results." | Medium | Report repeated checkpoint evaluation and best-step human cost transparently; include raw final policy metrics where available. Explain why single final eval is unstable. | Protocol supports this; final paper must show enough details. |
| "Wilson intervals are not enough for RL uncertainty." | Medium | Use Wilson for binomial episode success, and cite RL reliability work for broader seed/checkpoint variance. Avoid implying Wilson solves all RL statistics. | R027 candidates include Henderson/Agarwal/Wilson. |
| "Trace diagnostics are descriptive, not causal." | Medium | Present traces as mechanism diagnosis and hypothesis rejection, not causal proof. They reject the far-from-cube explanation and motivate stop rules. | Needs careful wording. |
| "The method was tuned until failure?" | Low/Medium | Preserve chronological experiment record R020-R024 and show stop rules were applied after each repair. | Tracker and registry support this. |
| "Recent related work is unstable or preprint-heavy." | Medium | Use stable published work for core framing; label 2025/2026 preprints as recent context only. | R027 source bank started; needs metadata audit. |
| "The protocol is obvious." | Medium | Emphasize the empirical reversal: without cost matching, the interpretation was different. The value is the demonstrated failure mode plus concrete required diagnostics. | Needs strong hero figure and Section 4. |

## Pre-Draft Fix List

1. Update `PAPER_PLAN.md` to foreground protocol contribution.
2. Polish Fig. 1 so the protocol and reversal are visible in the first figure.
3. Add a table/checklist of required HIL-RL trigger diagnostics.
4. Complete metadata audit for SAC, robosuite, Henderson, Agarwal, and Wilson.
5. Decide target venue family before deciding how hard to emphasize robotics
   breadth versus evaluation-methodology contribution.
