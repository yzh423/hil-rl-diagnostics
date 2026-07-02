"""Neural (torch) ensemble dynamics model for higher-dim robosuite states.

Drop-in replacement for the numpy `EnsembleDynamics` with the SAME interface
(`add`, `fit`, `predict_all`, `predict_mean`, `disagreement`, `fitted`, `k`) so
the `VoIGate` works unchanged. Each member is a small MLP predicting the
state *delta* from (s, a); members are trained on bootstrapped minibatches so
ensemble disagreement is a usable epistemic-uncertainty signal.

The numpy linear `EnsembleDynamics` remains the dependency-light fallback; this
class is used when the state dim is large (robosuite ~60-D) where a linear model
is too weak to give meaningful rollouts.

M1 (decision-aware / value-equivalent dynamics, OPTIONAL, default OFF)
---------------------------------------------------------------------
By default each member minimizes next-state MSE (a maximum-likelihood / PETS
objective). When `value_aware=True` and a `value_fn` is supplied, we ADD an
IterVAML-style value-equivalence term (Farahmand, NeurIPS 2018, arXiv:1806.01265;
Value-Equivalence Principle, Grimm et al., NeurIPS 2020, arXiv:2011.03506):

    L = (1 - beta) * || s_hat' - s' ||^2          # MLE / PETS term (kept as anchor)
      +      beta  * || V(s_hat') - V(s') ||^2     # value-equivalent term

so model error and ensemble disagreement concentrate where they change the
*value* the VoI gate reads, instead of on decision-irrelevant state detail. The
MLE term is always retained (`beta < 1`) for stability, since pure value-aware
losses can be unstable in stochastic / contact dynamics (documented by
lambda-models, arXiv:2306.17366). This is OFF by default so existing runs are
byte-for-byte unaffected.
"""

from __future__ import annotations

import numpy as np

try:
    import torch
    import torch.nn as nn
    _TORCH_OK = True
except Exception:  # pragma: no cover
    _TORCH_OK = False


class _MLP(nn.Module if _TORCH_OK else object):
    def __init__(self, in_dim, out_dim, hidden=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.SiLU(),
            nn.Linear(hidden, hidden), nn.SiLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x):
        return self.net(x)


class TorchEnsembleDynamics:
    def __init__(self, state_dim, act_dim, n_members=5, hidden=256,
                 lr=1e-3, device=None, seed=0,
                 value_aware=False, value_aware_coef=0.5, value_fn=None):
        if not _TORCH_OK:
            raise ImportError("PyTorch is required for TorchEnsembleDynamics")
        self.state_dim = int(state_dim)
        self.act_dim = int(act_dim)
        self.k = int(n_members)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        torch.manual_seed(seed)
        self.rng = np.random.default_rng(seed)

        self.members = [_MLP(state_dim + act_dim, state_dim, hidden).to(self.device)
                        for _ in range(self.k)]
        self.opts = [torch.optim.Adam(m.parameters(), lr=lr) for m in self.members]

        # M1: decision-aware / value-equivalent loss (OFF by default).
        # `value_aware_coef` is beta in [0, 1]; `value_fn(states_tensor)->(b,)`
        # is a differentiable (or detached) value estimate, e.g. V(s)=Q(s, pi(s))
        # built from the SAC critic. If value_fn is None the term is skipped and
        # training falls back to pure MLE, regardless of `value_aware`.
        self.value_aware = bool(value_aware)
        self.value_aware_coef = float(np.clip(value_aware_coef, 0.0, 1.0))
        self.value_fn = value_fn

        self._S, self._A, self._D = [], [], []
        self._fitted = False
        # normalization stats (set at fit)
        self._x_mu = None
        self._x_sd = None
        self._d_mu = None
        self._d_sd = None

    def set_value_fn(self, value_fn):
        """Attach/replace the value function used by the M1 value-aware term."""
        self.value_fn = value_fn

    def add(self, s, a, ns):
        s = np.atleast_2d(s).astype(np.float32)
        a = np.atleast_2d(a).astype(np.float32)
        ns = np.atleast_2d(ns).astype(np.float32)
        self._S.append(s)
        self._A.append(a)
        self._D.append(ns - s)

    def _stack(self):
        S = np.concatenate(self._S, 0)
        A = np.concatenate(self._A, 0)
        D = np.concatenate(self._D, 0)
        X = np.concatenate([S, A], axis=1)
        return X, D

    def fit(self, epochs=40, batch_size=256):
        if not self._S:
            return
        X, D = self._stack()
        self._x_mu = X.mean(0, keepdims=True)
        self._x_sd = X.std(0, keepdims=True) + 1e-6
        self._d_mu = D.mean(0, keepdims=True)
        self._d_sd = D.std(0, keepdims=True) + 1e-6
        Xn = ((X - self._x_mu) / self._x_sd).astype(np.float32)
        Dn = ((D - self._d_mu) / self._d_sd).astype(np.float32)
        n = Xn.shape[0]

        Xt = torch.as_tensor(Xn, device=self.device)
        Dt = torch.as_tensor(Dn, device=self.device)

        # M1: tensors needed to reconstruct the *raw* next state s' = s + delta
        # so the value-equivalent term can evaluate V on real (un-normalized)
        # states. Only built when the value-aware path is actually active.
        use_value = self.value_aware and (self.value_fn is not None)
        if use_value:
            St = torch.as_tensor(X[:, : self.state_dim].astype(np.float32),
                                 device=self.device)
            d_mu_t = torch.as_tensor(self._d_mu.astype(np.float32), device=self.device)
            d_sd_t = torch.as_tensor(self._d_sd.astype(np.float32), device=self.device)
            beta = self.value_aware_coef

        loss_fn = nn.MSELoss()
        for m, opt in zip(self.members, self.opts):
            m.train()
            for _ in range(epochs):
                idx = self.rng.integers(0, n, size=min(batch_size, n))  # bootstrap
                bx = Xt[idx]
                bd = Dt[idx]
                opt.zero_grad()
                pred = m(bx)
                mle = loss_fn(pred, bd)
                if use_value:
                    # denormalize predicted/true deltas -> raw next states
                    s = St[idx]
                    s_hat = s + (pred * d_sd_t + d_mu_t)
                    s_true = s + (bd * d_sd_t + d_mu_t)
                    v_hat = self.value_fn(s_hat).reshape(-1)
                    v_true = self.value_fn(s_true).reshape(-1)
                    val = loss_fn(v_hat, v_true)
                    loss = (1.0 - beta) * mle + beta * val
                else:
                    loss = mle
                loss.backward()
                opt.step()
            m.eval()
        self._fitted = True

    def _predict_delta_all(self, s, a):
        s = np.atleast_2d(s).astype(np.float32)
        a = np.atleast_2d(a).astype(np.float32)
        X = np.concatenate([s, a], axis=1)
        Xn = ((X - self._x_mu) / self._x_sd).astype(np.float32)
        Xt = torch.as_tensor(Xn, device=self.device)
        with torch.no_grad():
            preds = []
            for m in self.members:
                dn = m(Xt).cpu().numpy()
                preds.append(dn * self._d_sd + self._d_mu)  # denormalize
        return np.stack(preds, axis=0)  # (k, b, sdim)

    def predict_all(self, s, a):
        s2 = np.atleast_2d(s)
        deltas = self._predict_delta_all(s, a)  # (k,b,sdim)
        return s2[None, :, :] + deltas

    def predict_mean(self, s, a):
        return self.predict_all(s, a).mean(axis=0)

    def disagreement(self, s, a):
        preds = self.predict_all(s, a)        # (k,b,sdim)
        return preds.var(axis=0).mean(axis=1)  # (b,)

    @property
    def fitted(self):
        return self._fitted
