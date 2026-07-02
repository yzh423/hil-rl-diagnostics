"""Online ensemble dynamics model with epistemic uncertainty.

A deliberately lightweight (numpy-only) stand-in for a PETS-style probabilistic
ensemble / latent world model. Each member predicts the *delta* state from
features phi(s, a) via ridge regression on a bootstrapped replay buffer:

    s_{t+1} - s_t  ~=  W_k . phi(s_t, a_t)

Ensemble disagreement (variance across members of the predicted next state)
is used as the epistemic-uncertainty signal that drives the VoI gate. In
unseen / poorly-modeled regions disagreement is high -> the agent should be
more willing to ask the human.

Swap this class for a neural PETS ensemble or DreamerV3 latent model without
changing the gate's interface (predict / rollout / disagreement).
"""

from __future__ import annotations

import numpy as np


def _features(s, a):
    """Quadratic-ish features so a linear member can capture the point-mass dynamics."""
    s = np.atleast_2d(s)
    a = np.atleast_2d(a)
    bias = np.ones((s.shape[0], 1))
    return np.concatenate([s, a, bias], axis=1)


class EnsembleDynamics:
    def __init__(self, state_dim, act_dim, n_members=5, ridge=1e-2, seed=0):
        self.state_dim = state_dim
        self.act_dim = act_dim
        self.k = n_members
        self.ridge = ridge
        self.rng = np.random.default_rng(seed)
        self.feat_dim = state_dim + act_dim + 1
        self.W = [np.zeros((self.feat_dim, state_dim)) for _ in range(self.k)]
        self._fitted = False
        # replay buffer
        self._S, self._A, self._D = [], [], []

    def add(self, s, a, ns):
        s = np.atleast_2d(s)
        a = np.atleast_2d(a)
        ns = np.atleast_2d(ns)
        self._S.append(s)
        self._A.append(a)
        self._D.append(ns - s)

    def fit(self):
        if not self._S:
            return
        S = np.concatenate(self._S, 0)
        A = np.concatenate(self._A, 0)
        D = np.concatenate(self._D, 0)
        X = _features(S, A)
        m = X.shape[0]
        I = np.eye(self.feat_dim) * self.ridge
        for k in range(self.k):
            # bootstrap subset for member k -> diversity -> epistemic disagreement
            idx = self.rng.integers(0, m, size=m)
            Xk, Dk = X[idx], D[idx]
            self.W[k] = np.linalg.solve(Xk.T @ Xk + I, Xk.T @ Dk)
        self._fitted = True

    def predict_all(self, s, a):
        """Return (k, batch, state_dim) next-state predictions from every member."""
        X = _features(s, a)
        preds = np.stack([X @ self.W[k] for k in range(self.k)], axis=0)  # (k,b,sdim) deltas
        return np.atleast_2d(s)[None, :, :] + preds

    def predict_mean(self, s, a):
        return self.predict_all(s, a).mean(axis=0)

    def disagreement(self, s, a):
        """Epistemic uncertainty: mean per-member variance of predicted next state."""
        preds = self.predict_all(s, a)            # (k,b,sdim)
        return preds.var(axis=0).mean(axis=1)     # (b,)

    @property
    def fitted(self):
        return self._fitted
