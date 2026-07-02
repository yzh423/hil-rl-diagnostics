"""Foresighted Value-of-Information (VoI) intervention trigger (Module A).

Two trigger modes are provided:

* ``mode="value"`` (N1, the decision-theoretic trigger, default): an EVSI-style
  Value-of-Information computed from the learned **value function** and the
  ensemble **world model**. From state ``s`` we roll the *current policy* ``H``
  steps inside the model and estimate, at every step, (i) the value the critic
  assigns to where the policy is heading and (ii) the *disagreement of that value
  across ensemble members* (epistemic uncertainty in the decision-relevant
  quantity). The trigger fires when the policy is predicted to slide into a
  value collapse AND the model is uncertain about it:

      decline(s) = relu( V(s) - min_t  E_k V( s_t^rollout ) )
                   / max(|V(s)|, value_scale_floor)
      u(s)       = avg_t  CV_k[ V(s_t^rollout) ]            (coeff. of variation)
      VoI(s)     = psi(u(s)) * decline(s) - c_query

  This is value-based and scale-normalized (so a single threshold transfers
  across tasks/envs, feeding M2), with a scale floor and optional score clipping
  to prevent early near-zero critics from creating numerically meaningless
  trigger scores. Uncertainty is propagated *along* the rollout rather than
  measured only at ``s``. It is the model-based,
  *anticipatory* alternative to reactive value-stagnation triggers (UniIntervene)
  and a generalization of the model-policy agreement switch of Pinosky et al. to
  a human-model-policy gate.

* ``mode="risk"`` (the heuristic ablation): the original hand-crafted hazard /
  distance check (e.g. robosuite Lift: "gripper predicted to drift away from the
  cube within H"). Kept so the value-based trigger can be ablated against a
  geometry heuristic.

Final selection under a shared budget is done by the allocator
(``allocation/budget.py``); pacing is handled by the InterventionController.
"""

from __future__ import annotations

import numpy as np


class VoIGate:
    def __init__(
        self,
        model,
        hazard=None,
        hazard_radius=None,
        horizon=8,
        c_fail=1.0,
        c_query=0.05,
        unc_scale=50.0,
        tau=0.10,
        risk_fn=None,
        value_fn=None,
        mode="value",
        gamma=0.99,
        value_scale_floor=1.0,
        score_clip=10.0,
        reference_policy=None,
        learning_value_scale=0.0,
        learning_value_clip=1.0,
        learning_value_min_disagreement=0.0,
    ):
        self.model = model
        self.hazard = None if hazard is None else np.asarray(hazard, dtype=np.float64)
        self.hazard_radius = hazard_radius
        self.H = horizon
        self.c_fail = c_fail
        self.c_query = c_query
        self.unc_scale = unc_scale
        self.tau = tau
        self.gamma = float(gamma)
        self.value_scale_floor = max(1e-6, float(value_scale_floor))
        self.score_clip = None if score_clip is None or score_clip <= 0 else float(score_clip)
        self.reference_policy = reference_policy
        self.learning_value_scale = max(0.0, float(learning_value_scale))
        self.learning_value_clip = None if learning_value_clip is None or learning_value_clip <= 0 else float(learning_value_clip)
        self.learning_value_min_disagreement = max(
            0.0, float(learning_value_min_disagreement))
        # `risk_fn(states)->bool array` generalizes the 2D hazard check to any
        # task (e.g. robosuite Lift: "gripper predicted to drift away from cube").
        self.risk_fn = risk_fn
        # `value_fn(states)->(b,)` numpy value estimate V(s)=Q(s, pi(s)) from the
        # RLPD critic. Required for mode="value"; if absent we fall back to risk.
        self.value_fn = value_fn
        if mode == "value" and value_fn is None:
            mode = "risk"
        self.mode = mode

    def set_value_fn(self, value_fn):
        self.value_fn = value_fn
        if value_fn is not None and self.mode == "risk" and self.risk_fn is None:
            self.mode = "value"

    def set_reference_policy(self, reference_policy):
        self.reference_policy = reference_policy

    def _psi(self, u):
        # bounded monotone up-weighting of epistemic (value) uncertainty
        return 1.0 + np.tanh(self.unc_scale * u)

    def _reference_disagreement(self, states, policy):
        if self.reference_policy is None:
            return None
        states = np.atleast_2d(states).astype(np.float32)
        actor_actions = np.atleast_2d(np.asarray(policy(states), dtype=np.float64))
        ref_actions = np.atleast_2d(np.asarray(self.reference_policy(states), dtype=np.float64))
        if actor_actions.shape != ref_actions.shape:
            raise ValueError(
                "reference_policy must return actions with the same shape as policy")
        denom = np.sqrt(max(1, actor_actions.shape[1]))
        disagreement = np.linalg.norm(actor_actions - ref_actions, axis=1) / denom
        if self.learning_value_clip is not None:
            disagreement = np.clip(disagreement, 0.0, self.learning_value_clip)
        return disagreement

    def _learning_multiplier(self, states, policy):
        if self.reference_policy is None or self.learning_value_scale <= 0:
            return np.ones(np.atleast_2d(states).shape[0], dtype=np.float64)
        disagreement = self._reference_disagreement(states, policy)
        return 1.0 + self.learning_value_scale * disagreement

    # ---------------- mode="risk": geometry / hazard heuristic ----------------
    def _risk_check(self, st):
        if self.risk_fn is not None:
            return np.asarray(self.risk_fn(st), dtype=bool)
        d = np.linalg.norm(st[:, :2] - self.hazard[None, :], axis=1)
        return d < self.hazard_radius

    def predicted_failure_prob(self, s, policy):
        """Mean over ensemble members of 'rollout hits hazard within H steps'."""
        preds = self.model.predict_all(s, policy(s))      # (k,b,sdim) first step
        k, b, sdim = preds.shape
        states = preds.reshape(k * b, sdim)
        hit = np.zeros(k * b, dtype=bool)
        hit |= self._risk_check(states)
        for _ in range(self.H - 1):
            a = policy(states)
            states = self.model.predict_mean(states, a)
            hit |= self._risk_check(states)
        return hit.reshape(k, b).mean(axis=0)             # (b,)

    def _voi_risk(self, s, policy):
        p_fail = self.predicted_failure_prob(s, policy)
        u = self.model.disagreement(s, policy(s))
        utility = p_fail * self.c_fail * self._psi(u)
        score = utility * self._learning_multiplier(s, policy) - self.c_query
        return score, p_fail

    # ---------------- mode="value": decision-theoretic EVSI VoI ---------------
    def _voi_value(self, s, policy):
        """Value-based foresighted VoI with value-uncertainty propagated along
        an H-step model rollout of the current policy."""
        b, sdim = s.shape
        V0 = np.asarray(self.value_fn(s), dtype=np.float64).reshape(b)  # (b,)

        states = s.astype(np.float32)
        v_min = V0.copy()                       # lowest predicted mean value reached
        u_accum = np.zeros(b, dtype=np.float64)  # accumulated value coeff-of-variation
        for _ in range(self.H):
            a = policy(states)
            member_next = self.model.predict_all(states, a)   # (k, b, sdim)
            k = member_next.shape[0]
            flat = member_next.reshape(k * b, sdim)
            vk = np.asarray(self.value_fn(flat), dtype=np.float64).reshape(k, b)
            v_mean_t = vk.mean(axis=0)           # (b,) mean value across members
            v_std_t = vk.std(axis=0)             # (b,) value disagreement
            # scale-free uncertainty with a floor so near-zero early critics do
            # not dominate the trigger by numerical accident.
            u_accum += v_std_t / np.maximum(np.abs(v_mean_t), self.value_scale_floor)
            v_min = np.minimum(v_min, v_mean_t)
            states = member_next.mean(axis=0).astype(np.float32)  # continue on mean

        u = u_accum / max(1, self.H)             # avg value-CV along the rollout
        # predicted regret if we let the policy continue, as a fraction of |V0|
        decline = np.maximum(0.0, V0 - v_min) / np.maximum(
            np.abs(V0), self.value_scale_floor)
        utility = self._psi(u) * decline
        score = utility * self._learning_multiplier(s, policy) - self.c_query
        if self.score_clip is not None:
            score = np.clip(score, -self.score_clip, self.score_clip)
        # report a [0,1] "failure-like" signal for logging/calibration (M2)
        p_like = np.clip(decline, 0.0, 1.0)
        return score, p_like

    # ---------------- public API ----------------
    def voi(self, s, policy):
        s = np.atleast_2d(s)
        if not self.model.fitted:
            # no model yet -> uninformative; rely on threshold (no spurious firing)
            return np.full(s.shape[0], self.tau), np.zeros(s.shape[0])
        if self.mode == "value":
            return self._voi_value(s.astype(np.float32), policy)
        return self._voi_risk(s, policy)

    def candidates(self, s, policy):
        s = np.atleast_2d(s)
        score, p_fail = self.voi(s, policy)
        candidate = score > self.tau
        if (self.learning_value_min_disagreement > 0
                and self.reference_policy is not None):
            disagreement = self._reference_disagreement(s, policy)
            candidate = np.logical_and(
                candidate, disagreement >= self.learning_value_min_disagreement)
        return candidate, score, p_fail
