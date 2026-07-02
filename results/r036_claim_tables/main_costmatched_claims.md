# R036 Main Cost-Matched Claims

| Strategy | Run | Success | 95% CI | Human steps | Delta | Source | Claim status |
|---|---|---:|---:|---:|---:|---|---|
| No intervention | R020 | 400/500 = 80.0% | [76.3, 83.3] | 0.0 | -3.2 pp | `results/r020_lift_highn_reliability/r020_lift_highn_aggregate.csv` | baseline_success |
| Random b350 | R021 | 439/500 = 87.8% | [84.6, 90.4] | 177.0 | +4.6 pp | `results/r021_random_costmatch/r021_costmatch_aggregate.csv` | cost_matched_random_dominates |
| LV-VoI scale3 | R021 | 416/500 = 83.2% | [79.7, 86.2] | 202.0 | +0.0 pp | `results/r021_random_costmatch/r021_costmatch_aggregate.csv` | trigger_superiority_rejected |
| Random b450 | R021 | 426/500 = 85.2% | [81.8, 88.0] | 250.0 | +2.0 pp | `results/r021_random_costmatch/r021_costmatch_aggregate.csv` | random_family_frontier |
| Random b600 | R021 | 426/500 = 85.2% | [81.8, 88.0] | 269.2 | +2.0 pp | `results/r021_random_costmatch/r021_costmatch_aggregate.csv` | random_family_frontier |
