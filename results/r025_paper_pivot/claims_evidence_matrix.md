# R025 Claims-Evidence Matrix

**Working paper direction**: Cost-matched HIL-RL diagnostic benchmark and negative findings for intervention triggers in robotic manipulation.

**Core reframing**: The evidence no longer supports a main claim that the current VoI trigger is superior to random intervention. The defensible contribution is a benchmark/protocol paper showing how seemingly promising HIL-RL trigger results can reverse under cost matching, repeated checkpoint evaluation, and intervention-timing diagnostics.

## Claims-Evidence Matrix

| Claim ID | Claim | Evidence | Status | Paper Section |
|---|---|---|---|---|
| C1 | Cost-matched random baselines are necessary in HIL-RL because nominally efficient learned triggers can be dominated after matching human cost. | R020 initially suggested LV-VoI scale3 was near-random at lower cost: `416/500 = 83.2%`, cost 202.0 vs random `426/500 = 85.2%`, cost 269.2. R021 added `random_b350`, which reached `439/500 = 87.8%`, cost 177.0, dominating LV-VoI on both success and cost. | Supported | Introduction, Main Results |
| C2 | Single restored/checkpoint evaluations are not enough for paper claims; repeated checkpoint evaluation changes interpretation and exposes variance. | R004/R007 showed seed-0 restored single-eval results differed from repeated best-checkpoint ranking. R020-R024 use `5 x 20` repeated checkpoint evaluation for paper-facing comparisons. R024 seed-level repeated results vary strongly: 61%, 94%, 78%. | Supported | Protocol, Evaluation Reliability |
| C3 | Intuitive trigger repairs based on action disagreement or score thresholds do not repair random dominance on Lift. | R022 min-disagreement LV-VoI: `226/300 = 75.3%`, cost 211.7 vs same-seed `random_b350` `259/300 = 86.3%`, cost 95.0. R024 score-floor LV-VoI: `233/300 = 77.7%`, cost 253.3 vs same random reference. | Supported for current Lift setup | Negative Findings |
| C4 | Intervention-timing diagnostics explain why raw trigger scores are insufficient: LV-VoI is not merely intervening far from the object; it over-triggers and spends budget inefficiently. | R023 traces: LV-VoI starts closer to cube than random (`g2c_norm` 0.217 vs 0.285) but has 96 starts vs random's 55 and early score saturation. R024 blocks sub-0.05 starts after 4000 steps but still has 94 starts, showing score floor did not create random-level selectivity. | Supported as diagnostic finding | Trace Analysis |
| C5 | Current results do not support a broad robotics-generalization claim. | Stack R018: no-online matched BC `131/180 = 72.8%`, random `107/180 = 59.4%`, Stack-tuned LV-VoI `107/180 = 59.4%`; R019 lightweight redesigns stayed below no-online. | Supported negative limitation | Limitations, Appendix |
| C6 | A credible future method must be evaluated against cost-matched random, strong no-online/BC baselines, repeated checkpoint evaluation, and trace-level budget diagnostics before claiming trigger superiority. | Cross-run synthesis from R020-R024 and Stack R018-R019. This is a protocol recommendation rather than a new positive algorithm. | Supported as protocol contribution | Discussion, Protocol Recommendations |

## Evidence That Must Not Be Overclaimed

| Tempting Claim | Why It Is Not Supported | Safer Framing |
|---|---|---|
| "FORESIGHT-HIL beats random." | R021 `random_b350` dominates LV-VoI scale3; R022/R024 redesigns remain dominated. | "FORESIGHT-HIL-style triggers are stress-tested and found insufficient under cost-matched evaluation." |
| "VoI asks at better contact windows." | R023 shows LV-VoI starts closer to the cube than random, but still spends more and performs worse. | "Geometric proximity alone does not explain intervention value." |
| "Score calibration fixes over-triggering." | R024 blocks low-score starts but total starts barely change: 94 vs original 96. | "Raw score floors are inadequate as standalone budget controllers." |
| "Stack proves generalization." | Stack online intervention variants are dominated by matched no-online BC. | "Stack is a negative transfer/failure-analysis case." |

## Minimum Evidence Package for Paper Draft

1. Main Lift cost-matched table: R020 + R021 + R022 + R024.
2. Trace mechanism table: R023 + R024 trace diagnostics.
3. Evaluation protocol figure: single eval vs repeated checkpoint evaluation.
4. Stack appendix table: R018/R019 negative generalization.
5. Clear limitation statement: scripted privileged-state oracle, robosuite Lift/Stack, no real-human or real-robot deployment yet.
