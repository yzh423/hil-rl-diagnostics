# R014 Decision Note

R014 expanded the aligned Lift experiment from three seeds to five seeds by adding seeds 3-4 for the current method, no-intervention, and random baselines.

## Incremental seeds 3-4

- Learning-value VoI, budget 600, scale 3: `104/120 = 86.7%`, mean best-step human cost `80.0`.
- No-intervention restore-best: `103/120 = 85.8%`, mean best-step human cost `0.0`.
- Random restore-best, budget 600: `117/120 = 97.5%`, mean best-step human cost `160.0`.

## Five-seed aggregate

- Learning-value VoI, budget 600, scale 3: `256/300 = 85.3%`, Wilson CI `80.9-88.9%`, mean best-step human cost `202.0`.
- No-intervention restore-best: `237/300 = 79.0%`, Wilson CI `74.0-83.2%`, mean best-step human cost `0.0`.
- Random restore-best, budget 600: `251/300 = 83.7%`, Wilson CI `79.1-87.4%`, mean best-step human cost `269.2`.

## Interpretation

The three-seed story survives against no-intervention but becomes more nuanced against random. The method remains the best aggregate success point, but only by `1.7` percentage points over random after seeds 3-4. Its stronger claim is now efficiency: it matches or slightly exceeds random's repeated-best success while using fewer mean best-step human steps (`202.0` vs. `269.2`).

For a strong SCI-level paper claim, the next step should move from more Lift seeds to task breadth: run a second robosuite manipulation task with the same three systems and protocol.
