"""Scripted-oracle "human" for the robosuite Lift task (a SIMULATED human).

HONESTY NOTE: this is NOT a real human. It is a privileged-state heuristic
controller (it reads the exact cube/end-effector pose, which a real operator
would only get visually) used as a stand-in teleoperator. Simulation lets us
*control and sweep* its imperfection — which is exactly the robustness
contribution of FORESIGHT-HIL.

It reuses the SAME imperfect-human knobs as the 2D toy `ScriptedHuman`
(via `apply_imperfections`): action noise, reaction delay, skill, intervention
bias, dropout. The clean controller runs a 4-phase pick-and-lift state machine:

    align  -> move above the cube (gripper open)
    descend-> lower onto the cube (gripper open)
    close  -> close the gripper
    lift   -> raise the grasped cube

For non-Lift tasks it falls back to a generic "reach toward object" controller.
"""

from __future__ import annotations

import numpy as np

from .scripted_human import apply_imperfections


class ScriptedLiftOracle:
    def __init__(
        self,
        action_dim: int = 7,
        noise_std: float = 0.0,
        delay: int = 0,
        bias=0.0,
        skill: float = 1.0,
        p_dropout: float = 0.0,
        pos_gain: float = 20.0,
        seed: int = 0,
        task: str = "Lift",
    ):
        self.adim = int(action_dim)
        self.noise_std = float(noise_std)
        self.delay = int(delay)
        self.bias = bias
        self.skill = float(skill)
        self.p_dropout = float(p_dropout)
        self.pos_gain = float(pos_gain)
        self.task = task
        self.rng = np.random.default_rng(seed)
        self.reset()

    def reset(self):
        self._phase = "align"
        self._close_counter = 0
        self._open_counter = 0
        self._hist = []

    # ---- clean privileged controller ----
    def _clean_action(self, priv):
        a = np.zeros(self.adim, dtype=np.float64)
        if self.task.lower() == "stack" and "cubeA_pos" in priv and "cubeB_pos" in priv:
            return self._stack_action(priv)

        eef = priv.get("eef_pos", np.zeros(3))
        cube = priv.get("cube_pos", None)
        if cube is None:
            # generic reach: drive eef toward object using gripper_to_cube vector
            g2c = priv.get("gripper_to_cube", np.zeros(3))
            a[: min(3, g2c.size)] = np.clip(self.pos_gain * g2c[:3], -1, 1)
            return a

        above = cube + np.array([0.0, 0.0, 0.10])
        grasp = cube + np.array([0.0, 0.0, 0.005])
        d_xy = float(np.linalg.norm(cube[:2] - eef[:2]))
        dz_to_above = abs(eef[2] - above[2])
        dz_to_cube = eef[2] - cube[2]

        # ---- phase transitions ----
        if self._phase == "align" and d_xy < 0.02 and dz_to_above < 0.03:
            self._phase = "descend"
        elif self._phase == "descend" and dz_to_cube < 0.015:
            self._phase = "close"
        elif self._phase == "close":
            self._close_counter += 1
            if self._close_counter > 5:
                self._phase = "lift"

        if self._phase == "align":
            target, grip = above, -1.0
        elif self._phase == "descend":
            target, grip = grasp, -1.0
        elif self._phase == "close":
            target, grip = grasp, 1.0
        else:  # lift
            target, grip = cube + np.array([0.0, 0.0, 0.30]), 1.0

        a[:3] = np.clip(self.pos_gain * (target - eef), -1.0, 1.0)
        # orientation deltas (a[3:6]) left at 0 -> keep current wrist pose
        if self.adim >= 7:
            a[6] = grip
        return a

    def _stack_action(self, priv):
        """Pick cube A, move it over cube B, release, then retreat."""
        a = np.zeros(self.adim, dtype=np.float64)
        eef = np.asarray(priv.get("eef_pos", np.zeros(3)), dtype=np.float64)
        cube_a = np.asarray(priv["cubeA_pos"], dtype=np.float64)
        cube_b = np.asarray(priv["cubeB_pos"], dtype=np.float64)

        above_a = cube_a + np.array([0.0, 0.0, 0.10])
        grasp_a = cube_a + np.array([0.0, 0.0, 0.005])
        carry_above_b = cube_b + np.array([0.0, 0.0, 0.16])
        place_on_b = cube_b + np.array([0.0, 0.0, 0.055])
        retreat = cube_b + np.array([0.0, 0.0, 0.18])

        d_xy_a = float(np.linalg.norm(cube_a[:2] - eef[:2]))
        d_xy_b = float(np.linalg.norm(cube_b[:2] - eef[:2]))
        dz_above_a = abs(eef[2] - above_a[2])
        dz_grasp_a = abs(eef[2] - grasp_a[2])
        dz_place = abs(eef[2] - place_on_b[2])

        if self._phase == "align" and d_xy_a < 0.025 and dz_above_a < 0.035:
            self._phase = "descend"
        elif self._phase == "descend" and d_xy_a < 0.025 and dz_grasp_a < 0.025:
            self._phase = "close"
        elif self._phase == "close":
            self._close_counter += 1
            if self._close_counter > 8:
                self._phase = "lift"
        elif self._phase == "lift" and (
            cube_a[2] > cube_b[2] + 0.065 or abs(eef[2] - above_a[2]) < 0.035
        ):
            self._phase = "move"
        elif self._phase == "move" and d_xy_b < 0.035:
            self._phase = "place"
        elif self._phase == "place" and d_xy_b < 0.035 and dz_place < 0.035:
            self._phase = "open"
        elif self._phase == "open":
            self._open_counter += 1
            if self._open_counter > 8:
                self._phase = "retreat"

        if self._phase == "align":
            target, grip = above_a, -1.0
        elif self._phase == "descend":
            target, grip = grasp_a, -1.0
        elif self._phase == "close":
            target, grip = grasp_a, 1.0
        elif self._phase == "lift":
            target, grip = above_a, 1.0
        elif self._phase == "move":
            target, grip = carry_above_b, 1.0
        elif self._phase == "place":
            target, grip = place_on_b, 1.0
        elif self._phase == "open":
            target, grip = place_on_b, -1.0
        else:
            target, grip = retreat, -1.0

        a[:3] = np.clip(self.pos_gain * (target - eef), -1.0, 1.0)
        if self.adim >= 7:
            a[6] = grip
        return a

    def act(self, priv):
        """priv: privileged_state() dict. Returns a single (adim,) action."""
        self._hist.append(priv)
        priv_used = self._hist[-1 - self.delay] if len(self._hist) > self.delay else priv
        a = self._clean_action(priv_used)
        a = apply_imperfections(
            self.rng, a[None, :], skill=self.skill, noise_std=self.noise_std,
            bias=self.bias, p_dropout=self.p_dropout,
        )[0]
        return a
