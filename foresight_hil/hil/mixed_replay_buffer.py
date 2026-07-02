"""RLPD-style mixed demo/online replay buffer (HIL-SERL backbone).

Holds two underlying SB3 `ReplayBuffer`s: a `demo` buffer (scripted-oracle
demonstrations + human-intervention transitions) and an `online` buffer (the
agent's own transitions). Each `sample()` draws ~`demo_frac` of the minibatch
from demos and the rest from online data -- the symmetric sampling that makes
RLPD / HIL-SERL sample-efficient.

This object is assigned to `SAC.replay_buffer`, so the unmodified SB3
`SAC.train()` (which only calls `self.replay_buffer.sample(...)`) gets the 50/50
mix for free.
"""

from __future__ import annotations

import numpy as np
import torch as th

from stable_baselines3.common.buffers import ReplayBuffer
from stable_baselines3.common.type_aliases import ReplayBufferSamples


class MixedReplayBuffer:
    def __init__(self, buffer_size, observation_space, action_space,
                 device="auto", demo_frac=0.5, n_envs=1):
        self.demo_frac = float(demo_frac)
        self.demo = ReplayBuffer(buffer_size, observation_space, action_space,
                                 device=device, n_envs=n_envs,
                                 handle_timeout_termination=False)
        self.online = ReplayBuffer(buffer_size, observation_space, action_space,
                                   device=device, n_envs=n_envs,
                                   handle_timeout_termination=False)

    # ---- adding ----
    def add_online(self, obs, next_obs, action, reward, done, infos=None):
        self.online.add(obs, next_obs, action, np.array([reward]),
                        np.array([done]), infos or [{}])

    def add_demo(self, obs, next_obs, action, reward, done, infos=None):
        self.demo.add(obs, next_obs, action, np.array([reward]),
                      np.array([done]), infos or [{}])

    def add(self, *args, **kwargs):
        # default SB3-compatible path -> treat as online data
        self.online.add(*args, **kwargs)

    # ---- sizes ----
    def demo_size(self):
        return self.demo.buffer_size if self.demo.full else self.demo.pos

    def online_size(self):
        return self.online.buffer_size if self.online.full else self.online.pos

    def size(self):
        return self.demo_size() + self.online_size()

    # ---- sampling (RLPD 50/50) ----
    def sample(self, batch_size, env=None) -> ReplayBufferSamples:
        d_avail = self.demo_size()
        o_avail = self.online_size()
        if d_avail == 0 and o_avail == 0:
            raise RuntimeError("MixedReplayBuffer is empty; cannot sample.")

        if d_avail == 0:
            return self.online.sample(batch_size, env=env)
        if o_avail == 0:
            return self.demo.sample(batch_size, env=env)

        n_demo = int(round(batch_size * self.demo_frac))
        n_demo = max(1, min(batch_size - 1, n_demo))
        n_online = batch_size - n_demo

        sd = self.demo.sample(n_demo, env=env)
        so = self.online.sample(n_online, env=env)
        return ReplayBufferSamples(
            observations=th.cat([sd.observations, so.observations], dim=0),
            actions=th.cat([sd.actions, so.actions], dim=0),
            next_observations=th.cat([sd.next_observations, so.next_observations], dim=0),
            dones=th.cat([sd.dones, so.dones], dim=0),
            rewards=th.cat([sd.rewards, so.rewards], dim=0),
        )
