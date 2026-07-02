# R025 Figure and Table Plan

## Main Figures

| ID | Type | Description | Data Source | Priority | Paper Role |
|---|---|---|---|---|---|
| Fig. 1 | Hero diagnostic summary | Three-panel story: (A) HIL-RL intervention pipeline, (B) cost-matched success-cost frontier showing random_b350 dominates LV-VoI, (C) trace-level start counts showing LV-VoI over-triggers. | `results/r021_random_costmatch/r021_costmatch_success_cost.png`, `results/r024_score_floor_seed0_2/r024_success_cost_compare.png`, trace tables | HIGH | Introduces the protocol and the reversal of the initial claim |
| Fig. 2 | Success-cost scatter | Five-seed Lift comparison: none, random_b350, random_b450, random_b600, LV-VoI scale3. | `results/r021_random_costmatch/r021_costmatch_aggregate.csv` | HIGH | Main result: cost matching changes conclusion |
| Fig. 3 | Negative trigger repair comparison | Seeds 0-2 repeated success vs human cost for random_b350, R022 min-disagree, R024 score-floor. | `results/r024_score_floor_seed0_2/r024_score_floor_aggregate.csv` | HIGH | Shows intuitive repairs do not recover Pareto frontier |
| Fig. 4 | Intervention timing distribution | Compare random_b350, original LV-VoI scale3, R024 score-floor timing bins. | `results/r024_score_floor_seed0_2/r024_intervention_timing_bins_compare.png` | HIGH | Mechanism analysis |
| Fig. 5 | Score-over-time diagnostic | R024 intervention start scores with floor threshold and step boundary. | `results/r024_score_floor_seed0_2/r024_score_over_time.png` | MEDIUM | Explains why raw score threshold is insufficient |

## Main Tables

| ID | Type | Description | Data Source | Priority | Paper Role |
|---|---|---|---|---|---|
| Table 1 | Main cost-matched results | R020/R021 five-seed Lift repeated checkpoint success and cost. | `r020_lift_highn_aggregate.csv`, `r021_costmatch_aggregate.csv` | HIGH | Main evidence table |
| Table 2 | Negative findings | Hypothesis, variant, expected result, observed result, decision. | `results/r025_paper_pivot/negative_findings_table.csv` | HIGH | Makes the negative contribution explicit |
| Table 3 | Trace diagnostics | Starts, timing distribution, gripper-to-cube geometry, score saturation. | `r023_trace_strategy_diagnostics.csv`, `r024_trace_strategy_compare.csv` | HIGH | Mechanism evidence |
| Table 4 | Evaluation protocol checklist | Required baseline/eval diagnostics for HIL-RL claims. | synthesized from R020-R024 | MEDIUM | Protocol contribution |
| Appendix Table A1 | Stack negative transfer | Stack R018/R019 no-online/random/LV-VoI results. | tracker + R018/R019 result files | MEDIUM | Boundary of generalization |

## Caption Drafts

**Fig. 1 draft**: Cost matching reverses an initially promising HIL-RL trigger result. LV-VoI scale3 appears competitive against a budget-600 random baseline, but a lower-budget random baseline (`random_b350`) achieves higher repeated success with fewer best-step human interventions. Trace diagnostics reveal that LV-VoI does not simply query far from the object; it over-triggers relative to random and spends budget inefficiently.

**Table 2 draft**: Negative findings are treated as first-class evidence. Each redesign was tested against the same cost-matched random reference before expansion; variants that remained dominated were stopped rather than tuned further.
