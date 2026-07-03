"""Intervention trace schema and row construction."""

from __future__ import annotations

import numpy as np


INTERVENTION_TRACE_FIELDS = [
    "env_step", "episode", "episode_step", "task", "strategy", "seed",
    "human_steps", "budget_used_frac", "engagements", "candidate", "score",
    "p_fail", "eef_z", "cube_z", "gripper_to_cube_norm",
    "gripper_to_cube_xy", "cubeA_z", "cubeB_z", "gripper_to_cubeA_norm",
    "gripper_to_cubeB_norm", "stack_cubeA_lifted",
]

CANDIDATE_TRACE_FIELDS = [
    "env_step", "episode", "episode_step", "task", "strategy", "seed",
    "human_steps", "budget_used_frac", "engagements", "gate_evaluated",
    "intervened", "accepted", "candidate", "score", "p_fail",
    "score_floor_blocked", "rejection_reason", "eef_z", "cube_z",
    "gripper_to_cube_norm", "gripper_to_cube_xy", "cubeA_z", "cubeB_z",
    "gripper_to_cubeA_norm", "gripper_to_cubeB_norm", "stack_cubeA_lifted",
]


def _trace_float(value):
    if value is None:
        return "nan"
    value = float(value)
    if not np.isfinite(value):
        return "nan"
    return f"{value:.6f}"


def _trace_vec(priv, key):
    if key not in priv:
        return None
    return np.asarray(priv[key], dtype=np.float64).reshape(-1)


def _trace_geometry_fields(priv):
    priv = dict(priv or {})
    eef = _trace_vec(priv, "eef_pos")
    cube = _trace_vec(priv, "cube_pos")
    g2c = _trace_vec(priv, "gripper_to_cube")
    cube_a = _trace_vec(priv, "cubeA_pos")
    cube_b = _trace_vec(priv, "cubeB_pos")
    g2c_a = _trace_vec(priv, "gripper_to_cubeA")
    g2c_b = _trace_vec(priv, "gripper_to_cubeB")
    cube_a_lifted = ""
    if cube_a is not None and cube_b is not None and cube_a.size >= 3 and cube_b.size >= 3:
        cube_a_lifted = int(bool(cube_a[2] > cube_b[2] + 0.055))

    def z(vec):
        return vec[2] if vec is not None and vec.size >= 3 else None

    def norm(vec):
        return np.linalg.norm(vec) if vec is not None and vec.size else None

    def norm_xy(vec):
        return np.linalg.norm(vec[:2]) if vec is not None and vec.size >= 2 else None

    return {
        "eef_z": _trace_float(z(eef)),
        "cube_z": _trace_float(z(cube)),
        "gripper_to_cube_norm": _trace_float(norm(g2c)),
        "gripper_to_cube_xy": _trace_float(norm_xy(g2c)),
        "cubeA_z": _trace_float(z(cube_a)),
        "cubeB_z": _trace_float(z(cube_b)),
        "gripper_to_cubeA_norm": _trace_float(norm(g2c_a)),
        "gripper_to_cubeB_norm": _trace_float(norm(g2c_b)),
        "stack_cubeA_lifted": cube_a_lifted,
    }


def _trace_context_fields(step, ep_idx, ep_len, args, controller, priv):
    priv = dict(priv or {})
    return {
        "env_step": int(step),
        "episode": int(ep_idx),
        "episode_step": int(ep_len),
        "task": str(priv.get("task", getattr(args, "task", ""))),
        "strategy": str(getattr(args, "strategy", "")),
        "seed": int(getattr(args, "seed", 0)),
        "human_steps": int(getattr(controller, "spent", 0)),
        "budget_used_frac": f"{getattr(controller, 'spent', 0) / max(1, getattr(args, 'budget', 1)):.4f}",
        "engagements": int(getattr(controller, "engagements", 0)),
    }


def intervention_trace_row(step, ep_idx, ep_len, args, controller, priv):
    """Build a CSV row for an intervention start.

    The row is intentionally based on privileged simulator geometry because
    trace diagnostics are offline analysis outputs, not online policy features.
    """
    row = {
        **_trace_context_fields(step, ep_idx, ep_len, args, controller, priv),
        "candidate": int(bool(getattr(controller, "last_candidate", False))),
        "score": _trace_float(getattr(controller, "last_score", float("nan"))),
        "p_fail": _trace_float(getattr(controller, "last_p_fail", float("nan"))),
    }
    row.update(_trace_geometry_fields(priv))
    return row


def candidate_trace_row(step, ep_idx, ep_len, args, controller, priv):
    """Build a CSV row for a gate-evaluated candidate state.

    Unlike intervention traces, candidate traces include rejected states. They
    are for offline trigger-design audits and should not be treated as online
    success evidence.
    """
    row = {
        **_trace_context_fields(step, ep_idx, ep_len, args, controller, priv),
        "gate_evaluated": int(bool(getattr(controller, "last_gate_evaluated", False))),
        "intervened": int(bool(getattr(controller, "last_intervened", False))),
        "accepted": int(bool(getattr(controller, "last_started", False))),
        "candidate": int(bool(getattr(controller, "last_candidate", False))),
        "score": _trace_float(getattr(controller, "last_score", float("nan"))),
        "p_fail": _trace_float(getattr(controller, "last_p_fail", float("nan"))),
        "score_floor_blocked": int(bool(getattr(controller, "last_score_floor_blocked", False))),
        "rejection_reason": str(getattr(controller, "last_rejection_reason", "")),
    }
    row.update(_trace_geometry_fields(priv))
    return row
