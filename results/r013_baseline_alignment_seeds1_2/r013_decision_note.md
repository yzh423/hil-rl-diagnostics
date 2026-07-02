# R013 Decision Note

R013 aligned the strongest baselines with the current main method protocol: robosuite Lift, 10k steps, 20 demos, `learning_starts=500`, `bc_pretrain_steps=5000`, `bc_actor_reg_coef=50.0`, and restore-best checkpoint reporting.

## Repeated-best results

- No-intervention restore-best: R004 seed0 `49/60`, R013 seed1 `39/60`, R013 seed2 `46/60`; aggregate `134/180 = 74.4%`, Wilson CI `67.6-80.3%`, mean best-step human cost `0.0`.
- Random restore-best, budget 600: R004 seed0 `45/60`, R013 seed1 `60/60`, R013 seed2 `29/60`; aggregate `134/180 = 74.4%`, Wilson CI `67.6-80.3%`, mean best-step human cost `342.0`.
- Learning-value VoI, budget 600, scale 3: R012 seed0 `50/60`, R012 seed1 `55/60`, R010 seed2 `47/60`; aggregate `152/180 = 84.4%`, Wilson CI `78.4-89.0%`, mean best-step human cost `283.3`.

## Interpretation

The current method is now a credible main candidate. It improves repeated-best success by 10.0 percentage points over both no-intervention and random baselines. Compared with random, it also uses fewer mean best-step human steps (`283.3` vs `342.0`).

This is not yet the final SCI-level claim because seed-level variance remains visible, especially for random (`60/60` on seed1 but `29/60` on seed2). The next evidence step should expand to seeds 3-4 for the three systems or run a second manipulation task to test whether the advantage is task-specific.
