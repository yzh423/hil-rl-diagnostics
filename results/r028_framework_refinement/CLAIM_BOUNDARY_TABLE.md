# R028 Claim Boundary Table

Date: 2026-07-02

Use this table before writing any manuscript claim. If a sentence exceeds the
"Allowed claim" column, rewrite it or add evidence first.

| Claim ID | Allowed claim | Evidence anchor | Do not claim | Required caveat | Main section |
|---|---|---|---|---|---|
| P1 | HIL-RL trigger claims should include cost-matched random families, repeated checkpoint evaluation, and trace diagnostics. | R020-R024 synthesis; `results/r025_paper_pivot/evaluation_protocol.md` | This is a universal standard proven across all HIL-RL settings. | Presented as a protocol recommendation supported by this robotic case study. | Protocol / Discussion |
| P2 | Cost matching can reverse an initially promising trigger conclusion. | R020 vs R021: `random_b350` 439/500 at cost177.0 vs LV-VoI 416/500 at cost202.0. | Random always beats model-based triggers. | Applies to the current LV-VoI implementation and tested Lift setup. | Main Results |
| P3 | Simple trigger repairs did not recover the Pareto position. | R022 min-disagree 226/300 cost211.7; R024 score-floor 233/300 cost253.3; both below random_b350 259/300 cost95.0. | All disagreement or score-calibrated triggers are ineffective. | Only these two lightweight repairs were tested. | Repair Analysis |
| P4 | Trace diagnostics show over-triggering and score/timing mismatch. | R023: LV-VoI 96 starts vs random 55; closer g2c_norm 0.217 vs 0.285; early score saturation and low-score mid/late starts. | LV-VoI fails because it queries far from the cube. | Geometry proximity alone does not determine intervention value. | Mechanism Analysis |
| P5 | Current results do not support broad robotics generalization. | R018/R019 Stack variants dominated by matched no-online BC. | The protocol has been validated across many manipulation tasks. | Stack is boundary/failure evidence, not a positive transfer result. | Limitations / Appendix |
| P6 | Future trigger redesign should be gated before expansion. | R022/R024 stop decisions after same-seed random dominance. | The paper proposes a final new trigger method. | The paper proposes stop/continue rules, not a solved trigger. | Discussion |

## Numeric Claims Allowed in Main Text

| Number | Where it may be used | Source |
|---|---|---|
| `random_b350`: `439/500 = 87.8%`, cost 177.0 | Main result, abstract, introduction | `results/r021_random_costmatch/r021_costmatch_aggregate.csv` |
| LV-VoI scale3: `416/500 = 83.2%`, cost 202.0 | Main result, abstract, introduction | `results/r021_random_costmatch/r021_costmatch_aggregate.csv` |
| R022 min-disagree: `226/300 = 75.3%`, cost 211.7 | Repair analysis | `results/r022_lift_min_disagree_seed0_2/r022_min_disagree_aggregate.csv` |
| R024 score-floor: `233/300 = 77.7%`, cost 253.3 | Repair analysis | `results/r024_score_floor_seed0_2/r024_score_floor_aggregate.csv` |
| Same-seed `random_b350`: `259/300 = 86.3%`, cost 95.0 | Repair comparison | `results/r024_score_floor_seed0_2/r024_score_floor_aggregate.csv` |
| R023 starts: LV-VoI 96 vs random 55 | Trace analysis | `results/r023_real_trace_seed0_2/r023_trace_strategy_diagnostics.csv` |
| R023 g2c norm: LV-VoI 0.217 vs random 0.285 | Trace analysis | `results/r023_real_trace_seed0_2/r023_trace_strategy_diagnostics.csv` |

## Forbidden Shortcuts

- Do not write "FORESIGHT-HIL improves human efficiency" without immediately
  restricting it to early/prototype results and noting R021 reversal.
- Do not describe `always` as an upper bound on autonomous performance.
- Do not call Stack a positive generalization result.
- Do not imply real-human or real-robot validation.
- Do not cite 2026 arXiv competitors as stable facts without labeling them as
  recent preprints when appropriate.
