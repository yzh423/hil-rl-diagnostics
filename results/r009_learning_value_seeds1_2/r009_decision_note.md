# R009 Decision Note

Learning-value VoI (`demo_nn`, scale 2.0) was repeated on seeds 1-2 and combined with R008 seed 0.

The three-seed repeated best-checkpoint estimate is `131/180 = 72.8%` with Wilson CI `65.9-78.8%`. The matching best-policy human costs are `60`, `80`, and `390` human steps for seeds 0, 1, and 2 respectively, with mean `176.7` steps. This is a better research direction than plain tuned VoI, but seed 2 is weaker and the current evidence is not strong enough for a main-paper dominance claim.

Next decision: run a small scale/budget ablation before adding more seeds. Most promising axis is reducing late budget waste and selecting checkpoints by best-step cost, not simply spending the full 600 steps.
