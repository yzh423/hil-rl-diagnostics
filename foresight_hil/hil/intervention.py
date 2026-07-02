"""Intervention controller: decides WHO acts (learner vs scripted oracle).

Implements the four strategies compared in the experiment:

    none          : never intervene (pure SAC/RLPD lower bound)
    always         : oracle escorts every step (budget-unaware oracle-data
                    stress test; not an autonomous-policy upper bound)
    random@budget : engage at random while budget remains (ablation baseline)
    voi@budget    : FORESIGHT-HIL -- engage when the model-based VoI trigger
                    fires (gate.candidates) while budget remains

Once engaged, the oracle escorts for `takeover_len` steps (a takeover latch, as
in HIL-SERL), then control returns to the learner. For a single robosuite env
the proposal's Module-B *cross-env* top-B allocation degenerates to greedy
on-trigger spending; the parallel allocator (`allocation/budget.py`) is exercised
in the vectorized toy demo (`scripts/run_demo.py`).

Budget pacing (``pace``): without pacing, an eager VoI trigger drains the whole
budget in the first few thousand steps and then trains unaided for the rest of
the run. ``pace="linear"`` imposes a *rate ceiling* -- the cumulative spend may
not exceed ``budget * (t / total_steps)`` (plus a small ``pace_warmup`` head
start) -- so interventions are spread across training. This is a ceiling, not a
quota: VoI still chooses *which* states within the allowance are worth a query,
preserving its selectivity while preventing early exhaustion.
"""

from __future__ import annotations

import numpy as np


class InterventionController:
    def __init__(self, strategy, gate=None, budget=10**9, total_steps=10000,
                 takeover_len=1, seed=0, pace="none", pace_warmup=0.0,
                 voi_score_floor_after_step=0,
                 voi_score_floor_after_value=0.0):
        assert strategy in ("none", "always", "random", "voi")
        assert pace in ("none", "linear")
        self.strategy = strategy
        self.gate = gate
        self.budget = int(budget)
        self.total_steps = int(total_steps)
        self.takeover_len = int(takeover_len)
        self.rng = np.random.default_rng(seed)
        # random@budget engages at a rate that spends ~budget over the run
        self.p = float(np.clip(budget / max(1, total_steps), 0.0, 1.0))
        # budget pacing: cap cumulative spend to a linear schedule + warm-up
        self.pace = pace
        self.pace_warmup = float(pace_warmup)  # fraction of budget allowed at t=0
        self.voi_score_floor_after_step = int(voi_score_floor_after_step)
        self.voi_score_floor_after_value = float(voi_score_floor_after_value)
        self.score_floor_blocks = 0
        self.spent = 0
        self.engagements = 0
        self.timer = 0
        self.t = 0  # global env-step counter (advances once per step() call)
        self.last_intervened = False
        self.last_started = False
        self.last_candidate = False
        self.last_score = float("nan")
        self.last_p_fail = float("nan")
        self.last_score_floor_blocked = False

    def reset_episode(self):
        self.timer = 0

    def _reset_last_decision(self):
        self.last_intervened = False
        self.last_started = False
        self.last_candidate = False
        self.last_score = float("nan")
        self.last_p_fail = float("nan")
        self.last_score_floor_blocked = False

    def remaining(self):
        return max(0, self.budget - self.spent)

    def _pace_allows_new(self):
        """Under linear pacing, may we START a new engagement at the current step?
        Allowed cumulative spend grows linearly from `pace_warmup*budget` to the
        full budget over the run. Ongoing (latched) takeovers are exempt."""
        if self.pace != "linear":
            return True
        frac = min(1.0, self.t / max(1, self.total_steps))
        allowed = self.budget * (self.pace_warmup + (1.0 - self.pace_warmup) * frac)
        return self.spent < allowed

    def _score_floor_allows_new(self):
        if self.strategy != "voi":
            return True
        if self.voi_score_floor_after_value <= 0.0:
            return True
        if self.t < self.voi_score_floor_after_step:
            return True
        return self.last_score >= self.voi_score_floor_after_value

    def step(self, obs, policy):
        """Return True if the oracle should act this step (and meter the cost)."""
        self.t += 1
        self._reset_last_decision()
        if self.strategy == "none":
            return False

        budgeted = self.strategy in ("random", "voi")
        if budgeted and self.spent >= self.budget:
            return False

        # continue an ongoing takeover (latch) -- exempt from the pacing ceiling
        if self.timer > 0:
            self.timer -= 1
            self.spent += 1
            self.last_intervened = True
            return True

        # pacing ceiling only gates the START of a new engagement
        if budgeted and not self._pace_allows_new():
            return False

        fire = False
        if self.strategy == "always":
            fire = True
        elif self.strategy == "random":
            fire = self.rng.random() < self.p
        elif self.strategy == "voi":
            cand, _score, _pf = self.gate.candidates(np.atleast_2d(obs), policy)
            self.last_candidate = bool(np.asarray(cand).ravel()[0])
            self.last_score = float(np.asarray(_score).ravel()[0])
            self.last_p_fail = float(np.asarray(_pf).ravel()[0])
            fire = self.last_candidate
            if fire and not self._score_floor_allows_new():
                fire = False
                self.last_score_floor_blocked = True
                self.score_floor_blocks += 1

        if fire:
            self.timer = max(0, self.takeover_len - 1)
            self.spent += 1
            self.engagements += 1
            self.last_intervened = True
            self.last_started = True
            return True
        return False
