# R028 Section Architecture

Date: 2026-07-02

This is an outline contract, not prose. Each section has one job. If material
does not serve that job, move it or cut it.

## Abstract

Job: state the evaluation failure mode, the diagnostic protocol, the key case
study reversal, and the implication for HIL-RL trigger papers.

Must include:

- cost-matched random families;
- repeated checkpoint evaluation;
- trace diagnostics;
- `random_b350` vs LV-VoI reversal.

Must not include:

- a broad claim that random triggers are superior in general;
- a claim that the protocol is validated on real robots.

## 1. Introduction

Job: make the "why now" clear. Human interventions are expensive; trigger papers
need to know whether a learned trigger is genuinely more efficient than simple
budgeted random intervention.

Flow:

1. HIL-RL in robotic manipulation depends on scarce human attention.
2. Intervention-trigger quality is usually judged by success versus human cost.
3. That judgment is fragile when random baselines are not cost matched and
   checkpoint variance is under-measured.
4. This paper asks what happens when a plausible learned trigger is evaluated
   under a stricter diagnostic protocol.

Contributions:

1. diagnostic protocol;
2. cost-matched reversal case study;
3. trace-level mechanism diagnosis;
4. redesign stop/continue rules.

Must not do:

- open with "our method fails";
- promise a new trigger that beats random;
- spend too much space on untested future modules.

## 2. Related Work

Job: position the paper at the intersection of HIL-RL/intervention learning,
robot-gated querying, model-based uncertainty, and evaluation reliability.

Subsections:

1. Human-in-the-loop RL and intervention learning in robotics.
2. Robot-gated querying and budget-aware interactive learning.
3. Model-based uncertainty, VoI, and calibration.
4. Reliable evaluation in deep RL.

Must not do:

- become a catalog of every proposal-era reference;
- over-rely on 2026 arXiv preprints;
- imply prior work is invalid, only that this evaluation failure mode is
  under-controlled.

## 3. Diagnostic Protocol and Experimental Setup

Job: define the protocol before revealing the result, so the reader sees the
main contribution as a fair evaluation design.

Content:

- robosuite Lift/Stack setup;
- scripted privileged-state oracle as simulated human;
- SAC + demonstration replay / BC regularization backbone;
- strategies: none, random family, LV-VoI scale3, repairs;
- required metrics: repeated checkpoint success, Wilson CI, best-step human
  cost, raw final/restored best, intervention-start traces.

Must not do:

- hide the scripted-human limitation;
- call HIL-SERL results a reproduction;
- treat nominal budget as the only cost.

## 4. Main Case Study: Cost Matching Changes the Conclusion

Job: present R020 then R021 as a controlled reversal.

Evidence:

- R020 shows why the initial story was tempting.
- R021 shows `random_b350` dominates LV-VoI scale3.
- Fig. 2 and Table 1 carry the main quantitative result.

Key message:

> The method is not the point of victory; the protocol is what reveals the
> difference between apparent and actual trigger efficiency.

Must not do:

- make R020 sound like the final result;
- call LV-VoI useless in general.

## 5. Trigger Repairs and Mechanism Diagnosis

Job: show that two plausible lightweight repairs fail, then explain why using
trace diagnostics.

Evidence:

- R022 min-disagreement vs same-seed random_b350.
- R024 score-floor vs same-seed random_b350.
- R023/R024 trace timing, geometry, score, and p_fail.

Key message:

> The failure mode is not simply "wrong phase" or "far from cube"; it is
> insufficient selectivity and weak score/timing calibration.

Must not do:

- introduce a third untested heuristic;
- imply contact-aware or phase-aware triggers are guaranteed to work.

## 6. Discussion: Evaluation Rules for Future HIL-RL Triggers

Job: turn the case study into reusable guidance.

Protocol checklist:

- random budgets below and above method cost;
- repeated checkpoint estimates;
- best-step and final-policy cost/success;
- trace timing and geometry;
- score calibration diagnostics;
- same-seed stop gate before five-seed expansion.

Limitations:

- scripted oracle;
- robosuite tasks only;
- limited task breadth;
- no real-human or real-robot deployment;
- current LV-VoI implementation only.

Must not do:

- oversell the protocol as complete benchmark standard;
- bury limitations at the end.

## 7. Conclusion

Job: close with the evaluation lesson, not the failed trigger.

Final message:

> Before claiming an intervention trigger is more human-efficient, HIL-RL papers
> should show that the claim survives cost-matched random families, repeated
> checkpoint estimates, and trace-level budget diagnostics.

Must not do:

- end with "future work will fix the method" as the main takeaway.
