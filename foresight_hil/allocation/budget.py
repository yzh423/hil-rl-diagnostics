"""Budgeted query allocation across N parallel environments (Module B).

The headline problem enabled by massively-parallel simulation (Isaac Lab):
given per-env VoI scores and a shared per-step query budget B, decide *which*
environments get the scarce human query this step.

We provide:
  - allocate_topk : greedy top-B over candidates (the basic strategy)
  - allocate_random : random-B over candidates (ablation baseline)

A submodular / diversity-aware allocator (penalizing redundant near-duplicate
states across envs) is a natural extension and is left as a TODO hook.
"""

from __future__ import annotations

import numpy as np


def allocate_topk(scores, candidate_mask, budget, rng=None):
    """Select up to `budget` env indices with the highest score among candidates."""
    elig = np.where(candidate_mask)[0]
    if elig.size == 0 or budget <= 0:
        return np.array([], dtype=int)
    order = elig[np.argsort(-scores[elig])]
    return order[:budget]


def allocate_random(scores, candidate_mask, budget, rng=None):
    rng = rng or np.random.default_rng(0)
    elig = np.where(candidate_mask)[0]
    if elig.size == 0 or budget <= 0:
        return np.array([], dtype=int)
    if elig.size <= budget:
        return elig
    return rng.choice(elig, size=budget, replace=False)


# TODO: allocate_submodular(scores, states, budget) -> diversity-aware selection
