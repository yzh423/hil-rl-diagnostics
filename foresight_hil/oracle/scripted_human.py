"""Configurable scripted "human" oracle.

The clean oracle is a proportional reach-avoid controller: steer toward the
goal while pushing away from the hazard. Imperfection knobs let us *sweep* the
human-model family (the robustness contribution of the paper):

    noise_std     : Gaussian action noise (unsteady hand)
    delay         : reaction delay in steps (acts on a stale observation)
    bias          : systematic directional offset (miscalibrated operator)
    skill         : in [0,1], blends the optimal action with a random one
    p_dropout     : probability the operator gives no useful correction this step

This is what makes simulation an *advantage*: we can control and quantify human
imperfection, which is impossible to do cleanly on a real robot.
"""

from __future__ import annotations

import numpy as np


def apply_imperfections(rng, a, skill=1.0, noise_std=0.0, bias=0.0,
                        p_dropout=0.0, clip_lo=-1.0, clip_hi=1.0):
    """Apply the shared imperfect-human knobs to a clean action batch.

    Shared by the 2D toy `ScriptedHuman` and the robosuite `ScriptedLiftOracle`
    so the *same* human-model family (skill / noise / bias / dropout) is used
    everywhere. `delay` is handled by each controller (it needs an obs history).

    a        : (b, adim) clean optimal action
    skill    : in [0,1], blends optimal with a uniform-random action
    noise_std: Gaussian action noise std (unsteady hand)
    bias     : scalar or (adim,) systematic offset (miscalibrated operator)
    p_dropout: probability the operator gives no useful correction this step
    """
    a = np.atleast_2d(a).astype(np.float64)
    if skill < 1.0:
        rand = rng.uniform(clip_lo, clip_hi, size=a.shape)
        a = skill * a + (1.0 - skill) * rand
    if noise_std > 0:
        a = a + rng.normal(0, noise_std, size=a.shape)
    a = a + np.asarray(bias, dtype=np.float64)
    if p_dropout > 0:
        drop = rng.random(a.shape[0]) < p_dropout
        a[drop] = 0.0
    return np.clip(a, clip_lo, clip_hi)


class ScriptedHuman:
    def __init__(
        self,
        goal,
        hazard,
        hazard_radius,
        noise_std=0.0,
        delay=0,
        bias=(0.0, 0.0),
        skill=1.0,
        p_dropout=0.0,
        seed=0,
    ):
        self.goal = np.asarray(goal, dtype=np.float64)
        self.hazard = np.asarray(hazard, dtype=np.float64)
        self.hazard_radius = hazard_radius
        self.noise_std = noise_std
        self.delay = int(delay)
        self.bias = np.asarray(bias, dtype=np.float64)
        self.skill = float(skill)
        self.p_dropout = float(p_dropout)
        self.rng = np.random.default_rng(seed)
        self._hist = []

    def _optimal(self, s):
        s = np.atleast_2d(s)
        pos, vel = s[:, :2], s[:, 2:]
        to_goal = self.goal[None, :] - pos
        to_goal /= (np.linalg.norm(to_goal, axis=1, keepdims=True) + 1e-8)
        # vector from hazard center to agent
        d = pos - self.hazard[None, :]
        dist = np.linalg.norm(d, axis=1, keepdims=True) + 1e-8
        radial = d / dist
        # tangential (go-around) component avoids the potential-field local minimum
        # directly in front of the hazard. Pick the side that points toward the goal.
        tang = np.stack([-radial[:, 1], radial[:, 0]], axis=1)
        side = np.sign(np.sum(tang * to_goal, axis=1, keepdims=True))
        side[side == 0] = 1.0
        tang = tang * side
        influence = 2.2 * self.hazard_radius
        prox = np.clip((influence - dist) / influence, 0, None)  # in [0,1]
        a = (1.0 * to_goal
             + 3.0 * radial * prox            # push out
             + 2.5 * tang * prox              # circulate around
             - 0.25 * vel)
        return np.clip(a, -1.0, 1.0)

    def act(self, s):
        s = np.atleast_2d(s)
        # reaction delay: act on a stale observation
        self._hist.append(s.copy())
        s_used = self._hist[-1 - self.delay] if len(self._hist) > self.delay else s
        a = self._optimal(s_used)
        return apply_imperfections(
            self.rng, a, skill=self.skill, noise_std=self.noise_std,
            bias=self.bias[None, :], p_dropout=self.p_dropout,
        )
