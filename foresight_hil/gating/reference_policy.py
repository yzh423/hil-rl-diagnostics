"""Reference policies used to estimate the learning value of interventions."""

from __future__ import annotations

import numpy as np


def demo_arrays_from_mixed_buffer(mixed, max_points=None, seed=0):
    """Extract flattened demo observations/actions from a MixedReplayBuffer."""
    n = int(mixed.demo_size())
    if n <= 0:
        raise ValueError("demo buffer is empty")

    observations = np.asarray(mixed.demo.observations[:n], dtype=np.float32)
    actions = np.asarray(mixed.demo.actions[:n], dtype=np.float32)
    observations = observations.reshape(n, -1)
    actions = actions.reshape(n, -1)

    if max_points is not None and int(max_points) > 0 and n > int(max_points):
        rng = np.random.default_rng(seed)
        idx = rng.choice(n, size=int(max_points), replace=False)
        observations = observations[idx]
        actions = actions[idx]
    return observations, actions


class DemoNearestActionPolicy:
    """Return the action from the nearest demonstration observation.

    This is a lightweight non-parametric reference policy for diagnosing whether
    the current actor has drifted away from the demonstrated behavior near a
    queried state. It deliberately avoids training another model in the loop.
    """

    def __init__(self, observations, actions, normalize=True, eps=1e-6):
        observations = np.asarray(observations, dtype=np.float32)
        actions = np.asarray(actions, dtype=np.float32)
        if observations.ndim != 2:
            raise ValueError("observations must be a 2-D array")
        if actions.ndim != 2:
            raise ValueError("actions must be a 2-D array")
        if observations.shape[0] == 0:
            raise ValueError("at least one demonstration observation is required")
        if observations.shape[0] != actions.shape[0]:
            raise ValueError("observations and actions must have the same length")

        self.observations = observations
        self.actions = actions
        self.normalize = bool(normalize)
        self.eps = float(eps)
        if self.normalize:
            self.mean = observations.mean(axis=0, keepdims=True)
            self.std = observations.std(axis=0, keepdims=True)
            self.std = np.maximum(self.std, self.eps)
            self._obs_index = (observations - self.mean) / self.std
        else:
            self.mean = np.zeros((1, observations.shape[1]), dtype=np.float32)
            self.std = np.ones((1, observations.shape[1]), dtype=np.float32)
            self._obs_index = observations

    def __call__(self, states):
        states = np.atleast_2d(np.asarray(states, dtype=np.float32))
        query = (states - self.mean) / self.std if self.normalize else states
        d2 = ((query[:, None, :] - self._obs_index[None, :, :]) ** 2).sum(axis=2)
        nn = np.argmin(d2, axis=1)
        return self.actions[nn].astype(np.float32)
