"""FORESIGHT-HIL: Foresighted, budget-aware human-in-the-loop RL prototype.

Dependency-light (numpy-only) reference implementation of the core ideas:
  - ensemble dynamics model with epistemic uncertainty (PETS-style, learned online)
  - foresighted Value-of-Information (VoI) intervention trigger
  - budgeted query allocation across N parallel environments
  - configurable imperfect scripted "human" oracle

MuJoCo / Isaac Lab backends plug in by implementing the same env step API
(see envs/toy_reach.py for the contract).
"""

from .envs.toy_reach import VectorReachEnv
from .models.ensemble_dynamics import EnsembleDynamics
from .oracle.scripted_human import ScriptedHuman
from .gating.voi_gate import VoIGate
from .allocation.budget import allocate_topk

__all__ = [
    "VectorReachEnv",
    "EnsembleDynamics",
    "ScriptedHuman",
    "VoIGate",
    "allocate_topk",
]
