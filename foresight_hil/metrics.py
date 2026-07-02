"""Small statistical helpers for experiment logging."""

from __future__ import annotations

import math


def wilson_interval(successes: int, trials: int, z: float = 1.96):
    """Wilson score interval for a binomial success rate.

    Returns ``(low, high)`` in ``[0, 1]``. This is more informative than logging
    only ``successes / trials`` when evaluation uses few episodes: for example,
    0/5 successes still has a wide upper confidence bound.
    """
    n = int(trials)
    if n <= 0:
        return 0.0, 1.0

    s = max(0, min(int(successes), n))
    phat = s / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (phat + z2 / (2.0 * n)) / denom
    half = z * math.sqrt((phat * (1.0 - phat) + z2 / (4.0 * n)) / n) / denom
    low = max(0.0, center - half)
    high = min(1.0, center + half)
    if s == 0:
        low = 0.0
    if s == n:
        high = 1.0
    return low, high
