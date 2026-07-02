# R025 Evaluation Protocol Recommendation

## Why a New Protocol Is Needed

The current project produced a useful failure pattern: a trigger can look promising when compared against a poorly matched random baseline, then lose once random is cost-matched and checkpoints are repeatedly evaluated. This protocol is designed to prevent that failure mode in HIL-RL papers.

## Required Comparators

1. **No-online-human baseline**: same demonstrations, same RL/BC schedule, zero intervention cost.
2. **Random@budget family**: multiple budgets around the proposed method's realized human cost, not only the same nominal budget.
3. **Method under test**: report both nominal budget and realized best-step human cost.
4. **Stress/upper diagnostic**: always-oracle or high-budget intervention may be included, but must not be called an autonomous upper bound.

## Required Metrics

| Metric | Why It Is Required |
|---|---|
| Repeated checkpoint success | Single 20-episode evals are too noisy and can reverse rankings. |
| Best-step human cost | Final spent budget can be misleading when the best policy occurs earlier. |
| Raw final policy success | Shows late-policy collapse or instability. |
| Restored best policy success | Separates checkpoint selection from final-policy degradation. |
| Wilson CI | Avoids overreading low-N success rates. |
| Intervention starts and human steps | Separates long latch cost from start frequency. |
| Intervention timing bins | Identifies early/mid/late budget spending patterns. |
| Task geometry at intervention start | Tests whether triggers query in plausible contact/task phases. |
| Trigger score and p_fail distributions | Detects saturation, low-score starts, and calibration failure. |

## Stop/Continue Rules

- Do not expand a trigger variant to five seeds if it is dominated by same-seed random on both repeated success and best-step human cost.
- Do not claim a Pareto advantage without at least one random budget below and one random budget above the method's realized cost.
- Do not use a single restored evaluation as the final claim; use repeated checkpoint evaluation.
- If a trigger repair fails mechanically, debug the implementation. If it works mechanically but remains dominated, record it as a negative finding and stop.

## Current Protocol Outcome

R024 worked mechanically but failed scientifically. The score floor blocked low-score starts after step 4000, yet R024 remained dominated by random_b350. This is exactly the kind of result the protocol is meant to surface before a paper overclaims trigger superiority.
