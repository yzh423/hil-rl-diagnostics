# R054 Data Profile

Date: 2026-07-03

This profile follows the scipilot figure workflow: inspect data shape before
choosing charts, then choose panels that match the paper claim. R054 uses
registered evidence only and treats all raw R021/R023/R024 outputs as immutable.

## Data Shape

| Dataset | Rows used | Notes |
|---|---:|---|
| R021 cost-matched aggregate | 5 strategies | Five-seed repeated checkpoint evaluation. |
| R024 repair aggregate | 3 strategies | Same-seed random b350, min-disagree, and score-floor comparison. |
| R023 random trace starts | 55 starts | Seeds 0-2, random b350. |
| R023 LV-VoI trace starts | 96 starts | Seeds 0-2, original LV-VoI scale3. |
| R024 score-floor trace starts | 94 starts | Seeds 0-2, score-floor LV-VoI. |

Random trace rows have no LV-VoI score or `p_fail` fields by design. Those
fields are only plotted for LV-VoI variants.

## Trace Summary

| Strategy | Starts | Timing fractions | Budget fraction, median [IQR] | Gripper-cube norm, median [IQR] | Gripper-cube XY, median [IQR] | EEF-cube z gap, median [IQR] | Score / saturation |
|---|---:|---|---|---|---|---|---|
| Random b350 | 55 | early 27.3%, mid 34.5%, late 38.2% | 0.4743 [0.2314, 0.7457] | 0.2903 [0.1871, 0.3560] | 0.2374 [0.1223, 0.3094] | 0.0774 [0.0479, 0.1408] | not applicable |
| LV-VoI scale3 | 96 | early 12.5%, mid 50.0%, late 37.5% | 0.4908 [0.2600, 0.7342] | 0.2131 [0.0170, 0.3205] | 0.1137 [0.0159, 0.2429] | 0.1050 [0.0075, 0.1800] | score 0.0330 [0.0193, 0.0543]; score and `p_fail` saturation 12.5% |
| Score-floor LV-VoI | 94 | early 12.8%, mid 48.9%, late 38.3% | 0.4975 [0.2433, 0.7346] | 0.2104 [0.0260, 0.3450] | 0.1120 [0.0182, 0.2794] | 0.0951 [0.0207, 0.1851] | score 0.0672 [0.0555, 0.0961]; score and `p_fail` saturation 12.8% |

## Chart Choice

The figure is designed around one claim: the evidence supports an
attention-allocation diagnostic protocol, not LV-VoI superiority.

| Panel | Data type | Question answered | Chart choice |
|---|---|---|---|
| a | Strategy-level success and cost | Does cost matching overturn LV-VoI? | Relative-delta scatter around LV-VoI. |
| b | Same-seed repair success and cost | Should lightweight repairs be expanded? | Relative-delta scatter around random b350. |
| c | Intervention-start events over time | When is budget spent? | Event raster with counts. |
| d | Budget fraction at starts | Is budget spent similarly or selectively? | Boxplot with raw start points. |
| e | Geometry at starts | Is LV-VoI merely querying far from the cube? | Median/IQR markers for 3D norm and XY distance. |
| f | LV-VoI score and `p_fail` | Are scores clipped or weakly selective? | Log-score vs `p_fail` scatter with floor/clip guides. |

## Interpretation Boundary

The profile strengthens the mechanism story already supported by R023/R024:
LV-VoI starts more interventions than random while starting closer to the cube,
and the score-floor repair raises the accepted score floor without reducing
starts enough to recover the random frontier. It does not create a new success
rate result or justify a new trigger design.
