"""Training-side utilities for FORESIGHT-HIL (optional, default-off).

Currently exposes T1 plasticity-preservation tools (ReDo / shrink-and-perturb
resets) used to counter primacy bias under intervention-induced distribution
shift. Imports are dependency-light; torch is guarded inside `plasticity`.
"""

from .plasticity import (
    PlasticityManager,
    dormant_fraction,
    redo_reset,
    perturb_reset,
)

__all__ = [
    "PlasticityManager",
    "dormant_fraction",
    "redo_reset",
    "perturb_reset",
]
