"""T1 -- Plasticity preservation under intervention-induced distribution shift.

Human-in-the-loop RL injects *bursts* of off-distribution expert/correction data
and is typically trained at a high update-to-data (UTD) ratio for sample
efficiency -- exactly the regime that triggers **primacy bias / loss of
plasticity / dormant neurons**:

  - Primacy bias & periodic resets ........ Nikishin et al., ICML 2022, arXiv:2205.07802
  - ReDo / dormant-neuron recycling ....... Sokar et al., ICML 2023, arXiv:2302.12902
  - BBF (resets + high replay ratio) ...... Schwarzer et al., ICML 2023, arXiv:2305.19452

A more plastic learner recovers from an intervention with *fewer* future
queries, so training health is directly coupled to FORESIGHT-HIL's human-cost
objective. This module provides three OPTIONAL, dependency-light mechanisms,
all OFF by default and usable on any `torch.nn.Module` (actor, critic, or the
dynamics head):

  - `dormant_fraction(...)`  : ReDo diagnostic -- fraction of (near-)dead units.
  - `redo_reset(...)`        : recycle dormant units (re-init in-weights, zero
                               out-weights) per ReDo.
  - `perturb_reset(...)`     : shrink-and-perturb soft reset of a parameter
                               fraction (a cheap primacy-bias mitigation).
  - `PlasticityManager`      : schedules either mechanism every `reset_every`
                               steps over a set of modules + their optimizers.

`numpy` is the only hard dependency; torch is imported lazily and guarded so the
numpy-only toy demo still imports this file without torch installed.
"""

from __future__ import annotations

import numpy as np

try:
    import torch
    import torch.nn as nn
    _TORCH_OK = True
except Exception:  # pragma: no cover
    _TORCH_OK = False


def _require_torch():
    if not _TORCH_OK:
        raise ImportError("PyTorch is required for the plasticity reset utilities")


@torch.no_grad() if _TORCH_OK else (lambda f: f)
def dormant_fraction(module, inputs, tau=0.0):
    """Fraction of dormant units across the Linear/activation layers of `module`.

    Following ReDo (arXiv:2302.12902): a unit is "dormant" when its normalized
    average activation magnitude over a batch is <= `tau` (tau=0 -> exactly dead,
    small tau -> near-dead). `inputs` is a tensor/array fed through the module's
    sub-network to collect post-activation statistics via forward hooks.

    Returns a float in [0, 1]. Cheap diagnostic; no parameters are modified.
    """
    _require_torch()
    acts = {}

    def _hook(name):
        def fn(_m, _inp, out):
            a = out.detach()
            acts[name] = a.abs().mean(dim=0).reshape(-1)  # per-unit mean |activation|
        return fn

    handles = []
    for name, sub in module.named_modules():
        if isinstance(sub, (nn.ReLU, nn.SiLU, nn.GELU, nn.Tanh, nn.ELU)):
            handles.append(sub.register_forward_hook(_hook(name)))

    x = torch.as_tensor(np.atleast_2d(inputs), dtype=torch.float32,
                        device=next(module.parameters()).device)
    was_training = module.training
    module.eval()
    try:
        module(x)
    finally:
        module.train(was_training)
        for h in handles:
            h.remove()

    if not acts:
        return 0.0
    total, dormant = 0, 0
    for a in acts.values():
        score = a / (a.mean() + 1e-9)   # normalize per-layer (ReDo score)
        total += score.numel()
        dormant += int((score <= tau).sum().item())
    return dormant / max(1, total)


def redo_reset(module, inputs, optimizer=None, tau=0.0, reinit_scale=1.0):
    """Recycle dormant units in-place (ReDo, arXiv:2302.12902).

    For each Linear layer feeding a tracked activation, units whose normalized
    activation <= `tau` have their *incoming* weights re-initialized (Kaiming)
    and their *outgoing* weights (the next Linear's matching input column) zeroed,
    so a recycled unit re-enters learning without perturbing current outputs.
    Optionally resets the matching Adam optimizer moments.

    Returns the number of units reset. OFF by default at the call sites; safe to
    call periodically. No-op-safe if no dormant units are found.
    """
    _require_torch()
    acts = {}

    def _hook(name):
        def fn(_m, _inp, out):
            acts[name] = out.detach().abs().mean(dim=0).reshape(-1)
        return fn

    # ordered list of (name, linear) and the activations that follow them
    linears = [(n, m) for n, m in module.named_modules() if isinstance(m, nn.Linear)]
    handles = []
    for name, sub in module.named_modules():
        if isinstance(sub, (nn.ReLU, nn.SiLU, nn.GELU, nn.Tanh, nn.ELU)):
            handles.append(sub.register_forward_hook(_hook(name)))

    dev = next(module.parameters()).device
    x = torch.as_tensor(np.atleast_2d(inputs), dtype=torch.float32, device=dev)
    was_training = module.training
    module.eval()
    try:
        with torch.no_grad():
            module(x)
    finally:
        module.train(was_training)
        for h in handles:
            h.remove()

    if not acts:
        return 0

    # Use the per-layer mean activation as the dormancy score for the Linear that
    # produced it. We pair each activation with the most-recent preceding Linear.
    act_vecs = list(acts.values())
    n_reset = 0
    with torch.no_grad():
        for li, (_, lin) in enumerate(linears[:-1]):
            if li >= len(act_vecs):
                break
            a = act_vecs[li]
            if a.numel() != lin.weight.shape[0]:
                continue
            score = a / (a.mean() + 1e-9)
            dead = torch.where(score <= tau)[0]
            if dead.numel() == 0:
                continue
            # re-init incoming weights/bias of dead units
            new_w = torch.empty_like(lin.weight[dead])
            nn.init.kaiming_uniform_(new_w, a=float(np.sqrt(5)))
            lin.weight[dead] = new_w * reinit_scale
            if lin.bias is not None:
                lin.bias[dead] = 0.0
            # zero outgoing weights in the next linear
            nxt = linears[li + 1][1]
            if nxt.weight.shape[1] == lin.weight.shape[0]:
                nxt.weight[:, dead] = 0.0
            # reset optimizer state for the touched params
            if optimizer is not None:
                _reset_adam_state(optimizer, lin.weight)
                if lin.bias is not None:
                    _reset_adam_state(optimizer, lin.bias)
                _reset_adam_state(optimizer, nxt.weight)
            n_reset += int(dead.numel())
    return n_reset


def perturb_reset(module, optimizer=None, fraction=0.1, noise_scale=0.1, rng=None):
    """Shrink-and-perturb soft reset of a random `fraction` of parameters.

    A lightweight primacy-bias mitigation (Nikishin et al., arXiv:2205.07802):
    shrink selected weights toward zero and add small Gaussian noise, nudging the
    network back toward a more plastic regime without a full re-initialization.

    Returns the number of parameter tensors touched. OFF by default.
    """
    _require_torch()
    rng = rng or np.random.default_rng(0)
    touched = 0
    with torch.no_grad():
        for p in module.parameters():
            if p.ndim < 2:  # skip biases / norms
                continue
            mask = torch.as_tensor(
                rng.random(tuple(p.shape)) < fraction, device=p.device)
            if not bool(mask.any()):
                continue
            noise = torch.randn_like(p) * noise_scale
            p[mask] = (1.0 - noise_scale) * p[mask] + noise[mask]
            touched += 1
    if optimizer is not None:
        for p in module.parameters():
            _reset_adam_state(optimizer, p)
    return touched


def _reset_adam_state(optimizer, param):
    """Zero the Adam moment estimates for one parameter (post-reset hygiene)."""
    if not _TORCH_OK:
        return
    state = optimizer.state.get(param, None)
    if not state:
        return
    for key in ("exp_avg", "exp_avg_sq", "max_exp_avg_sq"):
        if key in state and torch.is_tensor(state[key]):
            state[key].zero_()
    if "step" in state:
        state["step"] = state["step"] * 0 if torch.is_tensor(state["step"]) else 0


class PlasticityManager:
    """Schedule periodic plasticity interventions over a set of modules.

    Parameters
    ----------
    modules : list of (nn.Module, optimizer_or_None, probe_inputs_or_None)
        Targets to keep plastic. `probe_inputs` (a batch) is required for the
        ReDo path; the perturb path ignores it.
    reset_every : int
        Step period between interventions (0 disables -> manager is a no-op).
    method : {"redo", "perturb"}
    tau : float            ReDo dormancy threshold.
    fraction, noise_scale  perturb-reset knobs.

    All defaults are inert; the manager only acts when constructed with
    `reset_every > 0`, which the training script does only behind an opt-in flag.
    """

    def __init__(self, modules, reset_every=0, method="redo", tau=0.0,
                 fraction=0.1, noise_scale=0.1, seed=0):
        self.modules = list(modules)
        self.reset_every = int(reset_every)
        self.method = method
        self.tau = float(tau)
        self.fraction = float(fraction)
        self.noise_scale = float(noise_scale)
        self.rng = np.random.default_rng(seed)
        self.n_events = 0
        self.last_reset_units = 0

    @property
    def enabled(self):
        return self.reset_every > 0 and _TORCH_OK

    def maybe_reset(self, step):
        """Call once per training step; runs an intervention on schedule.

        Returns the number of units/tensors reset this step (0 if it was not a
        scheduled step or the manager is disabled).
        """
        if not self.enabled or step <= 0 or (step % self.reset_every) != 0:
            return 0
        total = 0
        for mod, opt, probe in self.modules:
            if self.method == "redo":
                if probe is None:
                    continue
                total += redo_reset(mod, probe, optimizer=opt, tau=self.tau)
            else:
                total += perturb_reset(mod, optimizer=opt, fraction=self.fraction,
                                       noise_scale=self.noise_scale, rng=self.rng)
        self.n_events += 1
        self.last_reset_units = total
        return total
