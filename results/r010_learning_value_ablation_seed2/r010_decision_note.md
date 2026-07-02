# R010 Decision Note

R010 targeted the weakest R009 case: seed 2 with learning-value VoI (`demo_nn`, scale 2.0, budget 600), whose repeated best checkpoint was `38/60 = 63.3%`.

Two seed-2 variants were tested:

- Budget 300, scale 2.0: repeated best `45/60 = 75.0%`, best-step human cost `255`.
- Budget 600, scale 3.0: repeated best `47/60 = 78.3%`, best-step human cost `384`.

Both repair the weak seed-2 result. Replacing the original seed-2 point in the three-seed aggregate gives:

- Budget-300 option: `138/180 = 76.7%`, Wilson CI `70.0-82.3%`, mean best-step human cost `131.7`.
- Scale-3 option: `140/180 = 77.8%`, Wilson CI `71.2-83.2%`, mean best-step human cost `174.7`.

Decision: budget 300 is the more efficient Pareto candidate; scale 3 is the higher-success candidate. The next paper-facing experiment should repeat budget 300 and/or scale 3 across seeds 0-1, then compare against none/random with repeated checkpoint evaluation.
