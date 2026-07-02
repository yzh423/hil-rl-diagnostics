# R036 Trigger Repair Claims

| Strategy | Run | Success | 95% CI | Human steps | Delta | Source | Claim status |
|---|---|---:|---:|---:|---:|---|---|
| Random b350 | R024 | 259/300 = 86.3% | [82.0, 89.8] | 95.0 | +0.0 pp | `results/r024_score_floor_seed0_2/r024_score_floor_aggregate.csv` | baseline_success |
| Min-disagree LV-VoI | R022 | 226/300 = 75.3% | [70.2, 79.9] | 211.7 | -11.0 pp | `results/r022_lift_min_disagree_seed0_2/r022_min_disagree_aggregate.csv` | repair_negative |
| Score-floor LV-VoI | R024 | 233/300 = 77.7% | [72.6, 82.0] | 253.3 | -8.7 pp | `results/r024_score_floor_seed0_2/r024_score_floor_aggregate.csv` | repair_negative |
