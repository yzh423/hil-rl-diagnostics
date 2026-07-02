"""A weak, hazard-unaware policy used as a stand-in 'learner-in-progress'.

It greedily heads toward the goal but does NOT account for the hazard (and adds
exploration noise), so on its own it frequently drives into the hazard. This is
exactly the regime where a foresighted trigger should request help: the model
rollout predicts an impending failure several steps ahead.

Replace with an actual SAC/RLPD actor when wiring the MuJoCo / Isaac backends.
"""

from __future__ import annotations

import numpy as np


class WeakReachPolicy:
    def __init__(self, goal, noise=0.25, seed=0):
        self.goal = np.asarray(goal, dtype=np.float64)
        self.noise = noise
        self.rng = np.random.default_rng(seed)

    def __call__(self, s):
        s = np.atleast_2d(s)
        to_goal = self.goal[None, :] - s[:, :2]
        to_goal /= (np.linalg.norm(to_goal, axis=1, keepdims=True) + 1e-8)
        a = to_goal - 0.2 * s[:, 2:]                 # head to goal, mild damping
        if self.noise > 0:
            a = a + self.rng.normal(0, self.noise, size=a.shape)
        return np.clip(a, -1.0, 1.0)
