"""Vectorized 2D point-mass reach-avoid environment (numpy only).

This stands in for a contact-rich manipulation / navigation task and is the
contract that MuJoCo / Isaac Lab backends should implement:

    obs = env.reset()                      -> (N, obs_dim)
    obs, rew, done, info = env.step(act)   -> batched transition
    env.true_dynamics(s, a)                -> (N, state_dim)  [eval-only oracle model]

State  s = [px, py, vx, vy]
Action a = [ax, ay] in [-1, 1] (acceleration command)

A circular GOAL gives sparse +1 and terminates with success.
A circular HAZARD is (near-)irrecoverable: entering it gives -1 and terminates
with failure. This creates *impending failure* that a foresighted model
rollout can anticipate several steps before it happens.
"""

from __future__ import annotations

import numpy as np


class VectorReachEnv:
    obs_dim = 4
    state_dim = 4
    act_dim = 2

    def __init__(
        self,
        num_envs: int = 64,
        dt: float = 0.1,
        max_steps: int = 80,
        goal=(0.0, 1.6),
        goal_radius: float = 0.25,
        hazard=(0.0, 0.8),
        hazard_radius: float = 0.28,
        accel_scale: float = 1.4,
        vel_damp: float = 0.92,
        proc_noise: float = 0.01,
        seed: int = 0,
    ):
        self.n = int(num_envs)
        self.dt = dt
        self.max_steps = max_steps
        self.goal = np.asarray(goal, dtype=np.float64)
        self.goal_radius = goal_radius
        self.hazard = np.asarray(hazard, dtype=np.float64)
        self.hazard_radius = hazard_radius
        self.accel_scale = accel_scale
        self.vel_damp = vel_damp
        self.proc_noise = proc_noise
        self.rng = np.random.default_rng(seed)
        self._t = 0
        self.s = None
        self.alive = None
        self.reset()

    # ---- core API ----
    def reset(self):
        self.s = np.zeros((self.n, self.state_dim))
        # start spread out below the hazard, must pass near it to reach goal
        self.s[:, 0] = self.rng.uniform(-0.5, 0.5, self.n)   # px
        self.s[:, 1] = self.rng.uniform(-0.4, 0.0, self.n)   # py
        self.alive = np.ones(self.n, dtype=bool)
        self._t = 0
        return self.s.copy()

    def _advance(self, s, a, noise=True):
        a = np.clip(a, -1.0, 1.0) * self.accel_scale
        ns = s.copy()
        ns[:, 2:] = s[:, 2:] * self.vel_damp + a * self.dt          # velocity
        ns[:, :2] = s[:, :2] + ns[:, 2:] * self.dt                  # position
        if noise and self.proc_noise > 0:
            ns[:, :2] += self.rng.normal(0, self.proc_noise, size=(s.shape[0], 2))
        return ns

    def true_dynamics(self, s, a):
        """Noise-free transition; used only as an eval-only ground-truth model."""
        return self._advance(np.atleast_2d(s), np.atleast_2d(a), noise=False)

    def _dist(self, pos, center):
        return np.linalg.norm(pos - center[None, :], axis=1)

    def step(self, a):
        ns = self._advance(self.s, a, noise=True)
        d_goal = self._dist(ns[:, :2], self.goal)
        d_haz = self._dist(ns[:, :2], self.hazard)

        success = (d_goal < self.goal_radius) & self.alive
        failure = (d_haz < self.hazard_radius) & self.alive

        rew = np.zeros(self.n)
        rew[success] = 1.0
        rew[failure] = -1.0

        newly_done = success | failure
        self.alive = self.alive & (~newly_done)
        self.s = ns
        self._t += 1

        timeout = self._t >= self.max_steps
        done = newly_done | (timeout & (self.s[:, 0] * 0 == 0))  # all done at timeout
        if timeout:
            done = np.ones(self.n, dtype=bool)

        info = {
            "success": success,
            "failure": failure,
            "d_goal": d_goal,
            "d_haz": d_haz,
            "timeout": timeout,
        }
        return self.s.copy(), rew, done, info

    # ---- helpers for evaluation / oracle ----
    def in_hazard(self, pos):
        return self._dist(np.atleast_2d(pos), self.hazard) < self.hazard_radius

    def reached_goal(self, pos):
        return self._dist(np.atleast_2d(pos), self.goal) < self.goal_radius
