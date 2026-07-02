"""M2 -- Calibrated trigger uncertainty so a single VoI threshold transfers.

The VoI gate fires when a predicted-failure signal (`p_fail`, from ensemble
foresight rollouts) crosses a threshold tau. If that probability is *miscalibrated*
-- systematically over- or under-confident -- tau must be re-tuned per task/env and
queries are mis-spent. With many parallel environments (Module B) we want ONE tau
to transfer, which requires the trigger's probabilities to mean what they say.

This module is numpy-only and provides:

  - `reliability_curve(probs, labels, n_bins)` : binned (confidence, accuracy)
    points + counts for a reliability diagram.
  - `expected_calibration_error(...)`          : ECE (and MCE) summary.
  - `TemperatureScaler`                        : 1-parameter logistic temperature
    scaling (a Platt-style special case) fit on held-out (p_fail, failed?) pairs.
  - `PlattScaler`                              : full 2-parameter logistic (a*z+b)
    calibration for when a bias term is also needed.
  - `TriggerCalibrationLogger`                 : accumulates (p_fail, outcome)
    pairs online and dumps a reliability diagram / ECE to CSV.

Framing follows the calibration view used by Cal-QL (Nakamoto et al., NeurIPS
2023, arXiv:2303.05479) for value pre-training, here applied to the *trigger's*
failure probability rather than the value function. PETS-style ensembles
(arXiv:1805.12114) supply the raw uncertainty being calibrated.

Everything here is OPTIONAL diagnostics/post-processing: it does not alter the
gate unless the caller explicitly wraps `p_fail` through a fitted scaler.
"""

from __future__ import annotations

import numpy as np


def _logit(p, eps=1e-6):
    p = np.clip(np.asarray(p, dtype=np.float64), eps, 1.0 - eps)
    return np.log(p / (1.0 - p))


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.asarray(z, dtype=np.float64)))


def reliability_curve(probs, labels, n_bins=10):
    """Equal-width binning of predicted probabilities vs empirical accuracy.

    Returns a dict with arrays:
        bin_edges (n_bins+1,), bin_conf, bin_acc, bin_count (n_bins,)
    Empty bins report NaN confidence/accuracy and zero count.
    """
    probs = np.asarray(probs, dtype=np.float64).ravel()
    labels = np.asarray(labels, dtype=np.float64).ravel()
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    idx = np.clip(np.digitize(probs, edges[1:-1], right=False), 0, n_bins - 1)
    conf = np.full(n_bins, np.nan)
    acc = np.full(n_bins, np.nan)
    cnt = np.zeros(n_bins, dtype=int)
    for b in range(n_bins):
        m = idx == b
        cnt[b] = int(m.sum())
        if cnt[b] > 0:
            conf[b] = probs[m].mean()
            acc[b] = labels[m].mean()
    return {"bin_edges": edges, "bin_conf": conf, "bin_acc": acc, "bin_count": cnt}


def expected_calibration_error(probs, labels, n_bins=10):
    """ECE (count-weighted |confidence-accuracy|) and MCE (max gap).

    Returns (ece, mce). For a perfectly calibrated trigger both are ~0.
    """
    curve = reliability_curve(probs, labels, n_bins)
    cnt = curve["bin_count"]
    n = cnt.sum()
    if n == 0:
        return 0.0, 0.0
    gaps = np.abs(curve["bin_conf"] - curve["bin_acc"])
    valid = cnt > 0
    ece = float(np.sum(cnt[valid] * gaps[valid]) / n)
    mce = float(np.max(gaps[valid])) if valid.any() else 0.0
    return ece, mce


def brier_score(probs, labels):
    """Mean squared error between predicted probability and outcome."""
    probs = np.asarray(probs, dtype=np.float64).ravel()
    labels = np.asarray(labels, dtype=np.float64).ravel()
    if probs.size == 0:
        return 0.0
    return float(np.mean((probs - labels) ** 2))


class TemperatureScaler:
    """Single-parameter temperature scaling on the trigger logit.

        p_cal = sigmoid( logit(p) / T )

    T>1 softens overconfident probabilities, T<1 sharpens. Fit by minimizing
    NLL via a small 1-D Newton/gradient loop (no torch needed).
    """

    def __init__(self, temperature=1.0):
        self.T = float(temperature)
        self.fitted_ = False

    def fit(self, probs, labels, lr=0.05, iters=500):
        z = _logit(probs)
        y = np.asarray(labels, dtype=np.float64).ravel()
        if z.size == 0:
            return self
        log_T = np.log(self.T)
        for _ in range(iters):
            T = np.exp(log_T)
            p = _sigmoid(z / T)
            # dNLL/d(logT): chain rule through T = exp(logT)
            grad_logit = (p - y)              # dNLL/d(z/T)
            dz_dlogT = -z / T                 # d(z/T)/d(logT)
            grad = np.mean(grad_logit * dz_dlogT)
            log_T -= lr * grad
            log_T = float(np.clip(log_T, -4.0, 4.0))
        self.T = float(np.exp(log_T))
        self.fitted_ = True
        return self

    def transform(self, probs):
        return _sigmoid(_logit(probs) / self.T)

    def fit_transform(self, probs, labels, **kw):
        return self.fit(probs, labels, **kw).transform(probs)


class PlattScaler:
    """Two-parameter logistic calibration: p_cal = sigmoid(a * logit(p) + b).

    Generalizes temperature scaling with a bias term; fit by gradient descent on
    NLL. Use when the trigger is biased (not just over/under-confident).
    """

    def __init__(self, a=1.0, b=0.0):
        self.a = float(a)
        self.b = float(b)
        self.fitted_ = False

    def fit(self, probs, labels, lr=0.1, iters=1000):
        z = _logit(probs)
        y = np.asarray(labels, dtype=np.float64).ravel()
        if z.size == 0:
            return self
        a, b = self.a, self.b
        for _ in range(iters):
            p = _sigmoid(a * z + b)
            err = p - y
            ga = np.mean(err * z)
            gb = np.mean(err)
            a -= lr * ga
            b -= lr * gb
        self.a, self.b = float(a), float(b)
        self.fitted_ = True
        return self

    def transform(self, probs):
        return _sigmoid(self.a * _logit(probs) + self.b)

    def fit_transform(self, probs, labels, **kw):
        return self.fit(probs, labels, **kw).transform(probs)


class TriggerCalibrationLogger:
    """Accumulate (p_fail, true_outcome) pairs and emit calibration diagnostics.

    Intended as an optional hook in the HIL loop: each step (or each episode end)
    record the trigger's predicted failure probability and whether that state
    actually led to failure. At the end, `summary()` gives ECE/MCE/Brier and
    `to_csv()` writes the reliability diagram for plotting.
    """

    def __init__(self, n_bins=10):
        self.n_bins = int(n_bins)
        self._p = []
        self._y = []

    def record(self, p_fail, failed):
        p = np.atleast_1d(np.asarray(p_fail, dtype=np.float64)).ravel()
        y = np.atleast_1d(np.asarray(failed, dtype=np.float64)).ravel()
        # broadcast a scalar outcome across a batch of probabilities if needed
        if y.size == 1 and p.size > 1:
            y = np.full(p.shape, float(y[0]))
        self._p.extend(p.tolist())
        self._y.extend(y.tolist())

    def __len__(self):
        return len(self._p)

    def summary(self):
        if not self._p:
            return {"n": 0, "ece": 0.0, "mce": 0.0, "brier": 0.0}
        p = np.asarray(self._p)
        y = np.asarray(self._y)
        ece, mce = expected_calibration_error(p, y, self.n_bins)
        return {"n": len(self._p), "ece": ece, "mce": mce,
                "brier": brier_score(p, y)}

    def reliability(self):
        return reliability_curve(np.asarray(self._p), np.asarray(self._y),
                                 self.n_bins)

    def to_csv(self, path):
        """Write the reliability diagram (one row per bin) to `path`."""
        import csv
        c = self.reliability()
        edges = c["bin_edges"]
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["bin_lo", "bin_hi", "confidence", "accuracy", "count"])
            for b in range(self.n_bins):
                conf = c["bin_conf"][b]
                acc = c["bin_acc"][b]
                w.writerow([
                    f"{edges[b]:.4f}", f"{edges[b + 1]:.4f}",
                    "" if np.isnan(conf) else f"{conf:.6f}",
                    "" if np.isnan(acc) else f"{acc:.6f}",
                    int(c["bin_count"][b]),
                ])
        return path
