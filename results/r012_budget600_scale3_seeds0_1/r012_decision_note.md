# R012 Decision Note

R012 repeated the R010 `budget600 / learning_value_scale=3.0` repair on seeds 0-1.

## Result

- Seed 0 repeated best checkpoint: `50/60 = 83.3%`, Wilson CI `72.0-90.7%`, best-step human cost `80`.
- Seed 1 repeated best checkpoint: `55/60 = 91.7%`, Wilson CI `81.9-96.4%`, best-step human cost `386`.
- Combined with R010 seed 2 scale-3 result: `47/60 = 78.3%`, best-step human cost `384`.

Three-seed aggregate: `152/180 = 84.4%`, Wilson CI `78.4-89.0%`, mean best-step human cost `283.3`.

## Interpretation

`budget600 / scale3` is now the strongest current learning-value VoI candidate. It is more expensive than the R011 budget300 ablation, but it is much more reliable after repeated checkpoint evaluation and improves substantially over the original R008/R009 scale2 aggregate (`131/180 = 72.8%`).

Use this as the next main-method candidate, then compare it against no-intervention and random repeated baselines under the same three-seed evaluation protocol.
