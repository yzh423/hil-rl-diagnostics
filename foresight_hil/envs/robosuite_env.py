"""Gymnasium-compatible wrapper around a robosuite manipulation task.

This is the "real simulated robot" backend for FORESIGHT-HIL. It mirrors the
contract documented in `toy_reach.py` (reset / step / privileged accessors) but
runs a MuJoCo Panda arm via robosuite instead of a 2D point mass.

Default task: `Lift` (single Panda, OSC_POSE controller, proprioception + object
state, NO images to stay laptop-fast). The flattened observation is

    obs = concat(robot0_proprio-state, object-state)   # 60-D for Lift

and the action is the 7-D OSC_POSE command ([dx,dy,dz, droll,dpitch,dyaw, grip]).

`privileged_state()` returns the ground-truth eef / object pose used by the
scripted-oracle "human" (this is privileged info a real operator would get
visually, and that simulation lets us read exactly).

A lightweight fallback to a built-in Gymnasium MuJoCo task (`Reacher-v4`) is
provided so the pipeline still runs if robosuite fails to import/build.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np

try:
    import gymnasium as gym
    from gymnasium import spaces
except Exception as e:  # pragma: no cover
    raise ImportError("gymnasium is required for the robosuite backend") from e


DEFAULT_OBS_KEYS = ["robot0_proprio-state", "object-state"]


def _ensure_numba_cache_dir():
    """Keep robosuite/numba cache writes inside this project.

    On some Windows installs, numba tries to probe cache writability under
    Anaconda's site-packages, and that filesystem operation can hang for minutes.
    Pointing NUMBA_CACHE_DIR at a local project directory avoids that import-time
    stall while preserving numba caching.
    """
    if os.environ.get("NUMBA_CACHE_DIR"):
        return os.environ["NUMBA_CACHE_DIR"]
    cache_dir = Path(__file__).resolve().parents[2] / ".numba_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ["NUMBA_CACHE_DIR"] = str(cache_dir)
    return os.environ["NUMBA_CACHE_DIR"]


class RobosuiteGymEnv(gym.Env):
    """Single-environment gymnasium wrapper over a robosuite task."""

    metadata = {"render_modes": []}

    def __init__(
        self,
        task: str = "Lift",
        robot: str = "Panda",
        obs_keys=None,
        horizon: int = 200,
        control_freq: int = 20,
        reward_shaping: bool = True,
        terminate_on_success: bool = False,
        seed: int = 0,
        quiet: bool = True,
    ):
        super().__init__()
        _ensure_numba_cache_dir()
        import robosuite as suite
        from robosuite.controllers import load_composite_controller_config

        # robosuite's "BASIC" composite controller config defines controllers for
        # body parts (torso/head/base/legs/left) that a single-arm Panda does not
        # have, so robosuite logs a "Skipping ..." WARNING for each missing part on
        # EVERY env reset. That floods stdout during demo collection / training.
        # The warnings are benign (robosuite simply drops configs for absent parts),
        # so we raise the robosuite logger level to silence them. Set quiet=False to
        # restore the default verbosity.
        if quiet:
            import logging as _logging
            _logging.getLogger("robosuite_logs").setLevel(_logging.ERROR)

        self.task = task
        self.obs_keys = list(obs_keys) if obs_keys is not None else list(DEFAULT_OBS_KEYS)
        self.horizon = horizon
        self.terminate_on_success = bool(terminate_on_success)
        self._seed = seed

        controller_cfg = load_composite_controller_config(controller="BASIC", robot=robot)
        self._env = suite.make(
            env_name=task,
            robots=robot,
            controller_configs=controller_cfg,
            has_renderer=False,
            has_offscreen_renderer=False,
            use_camera_obs=False,
            use_object_obs=True,
            reward_shaping=reward_shaping,
            horizon=horizon,
            control_freq=control_freq,
            ignore_done=False,
        )

        obs_dict = self._env.reset()
        self._last_obs_dict = obs_dict
        self._obs_slices = {}
        flat, slices = self._flatten(obs_dict, return_slices=True)
        self._obs_slices = slices
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=flat.shape, dtype=np.float32
        )
        low, high = self._env.action_spec
        self.action_space = spaces.Box(
            low=low.astype(np.float32), high=high.astype(np.float32), dtype=np.float32
        )
        self._t = 0

    # ---- obs flattening ----
    def _flatten(self, obs_dict, return_slices=False):
        parts, slices, i = [], {}, 0
        for k in self.obs_keys:
            v = np.asarray(obs_dict[k], dtype=np.float32).ravel()
            slices[k] = slice(i, i + v.size)
            i += v.size
            parts.append(v)
        flat = np.concatenate(parts).astype(np.float32)
        if return_slices:
            return flat, slices
        return flat

    @property
    def obs_slices(self):
        return dict(self._obs_slices)

    def gripper_to_cube_slice(self):
        """Index slice (within the flattened obs) of the gripper->cube vector,
        used by the VoI risk function for the Lift task. Returns None if absent."""
        if "object-state" not in self._obs_slices:
            return None
        # For Lift, object-state = [cube_pos(3), cube_quat(4), gripper_to_cube(3)]
        if self.task == "Lift":
            base = self._obs_slices["object-state"].start
            return slice(base + 7, base + 10)
        return None

    # ---- gymnasium API ----
    def reset(self, *, seed=None, options=None):
        if seed is not None:
            self._seed = seed
        obs_dict = self._env.reset()
        self._last_obs_dict = obs_dict
        self._t = 0
        return self._flatten(obs_dict), {}

    def step(self, action):
        action = np.clip(np.asarray(action, dtype=np.float64),
                         self.action_space.low, self.action_space.high)
        obs_dict, reward, done, info = self._env.step(action)
        self._last_obs_dict = obs_dict
        self._t += 1
        success = bool(self._env._check_success())
        # With dense shaping, terminating on success removes the per-step reward
        # stream and makes "grasp-and-hover" out-score "lift-and-complete", so by
        # default we let the episode run to the horizon (success stays a *metric*,
        # not a terminal). Set terminate_on_success=True for a sparse-reward setup.
        if self.terminate_on_success:
            terminated = success
            truncated = bool(done and not success)
        else:
            terminated = False
            truncated = bool(done)  # robosuite `done` is horizon-based
        info = dict(info)
        info["is_success"] = success
        return self._flatten(obs_dict), float(reward), terminated, truncated, info

    def privileged_state(self):
        """Ground-truth pose info for the scripted oracle (the 'human's eyes')."""
        o = self._last_obs_dict
        out = {
            "task": self.task,
            "eef_pos": np.asarray(o.get("robot0_eef_pos", np.zeros(3)), dtype=np.float64),
            "gripper_qpos": np.asarray(o.get("robot0_gripper_qpos", np.zeros(2)), dtype=np.float64),
        }
        if "cube_pos" in o:
            out["cube_pos"] = np.asarray(o["cube_pos"], dtype=np.float64)
        if "gripper_to_cube_pos" in o:
            out["gripper_to_cube"] = np.asarray(o["gripper_to_cube_pos"], dtype=np.float64)
        if "cubeA_pos" in o:
            out["cubeA_pos"] = np.asarray(o["cubeA_pos"], dtype=np.float64)
        if "cubeB_pos" in o:
            out["cubeB_pos"] = np.asarray(o["cubeB_pos"], dtype=np.float64)
        if "gripper_to_cubeA" in o:
            out["gripper_to_cubeA"] = np.asarray(o["gripper_to_cubeA"], dtype=np.float64)
        if "gripper_to_cubeB" in o:
            out["gripper_to_cubeB"] = np.asarray(o["gripper_to_cubeB"], dtype=np.float64)
        return out

    def close(self):
        try:
            self._env.close()
        except Exception:
            pass


class ReacherFallbackEnv(gym.Env):
    """Fallback: built-in Gymnasium MuJoCo `Reacher-v4` exposed with the same
    privileged accessors so the rest of the pipeline runs unchanged if robosuite
    is unavailable. Honest note: this is a 2-DoF toy reacher, NOT a manipulation
    task; used only to keep the deliverable runnable."""

    metadata = {"render_modes": []}

    def __init__(self, task="Reacher", horizon=50, seed=0, **kwargs):
        super().__init__()
        self._env = gym.make("Reacher-v4")
        self.observation_space = self._env.observation_space
        self.action_space = self._env.action_space
        self.task = "Reacher"
        self.horizon = horizon
        self._last_obs = None

    def reset(self, *, seed=None, options=None):
        obs, info = self._env.reset(seed=seed)
        self._last_obs = obs
        return obs.astype(np.float32), info

    def step(self, action):
        obs, reward, terminated, truncated, info = self._env.step(action)
        self._last_obs = obs
        # Reacher has no success flag; define "success" as fingertip close to target
        dist = float(np.linalg.norm(obs[-3:-1])) if obs.shape[0] >= 3 else 1.0
        info = dict(info)
        info["is_success"] = bool(dist < 0.02)
        return obs.astype(np.float32), float(reward), bool(terminated), bool(truncated), info

    def gripper_to_cube_slice(self):
        # Reacher obs[-3:-1] is the fingertip->target vector (2-D)
        n = self.observation_space.shape[0]
        return slice(n - 3, n - 1)

    def privileged_state(self):
        o = self._last_obs
        vec = np.asarray(o[-3:-1], dtype=np.float64) if o is not None else np.zeros(2)
        return {"gripper_to_cube": vec, "eef_pos": np.zeros(3)}

    def close(self):
        self._env.close()


def make_env(task: str = "Lift", seed: int = 0, horizon: int = 200, **kwargs):
    """Factory that returns a robosuite-backed env, falling back to Reacher-v4.

    Returns (env, backend_str) where backend_str is "robosuite" or
    "reacher_fallback" so callers can log/honestly report which was used.
    """
    if task.lower() in ("reacher", "fallback"):
        return ReacherFallbackEnv(task=task, seed=seed, horizon=min(horizon, 50)), "reacher_fallback"
    try:
        env = RobosuiteGymEnv(task=task, seed=seed, horizon=horizon, **kwargs)
        return env, "robosuite"
    except Exception as e:  # pragma: no cover - exercised only on install failure
        print(f"[make_env] robosuite backend failed ({type(e).__name__}: {e}); "
              f"falling back to Gymnasium Reacher-v4.")
        return ReacherFallbackEnv(task="Reacher", seed=seed, horizon=min(horizon, 50)), "reacher_fallback"
