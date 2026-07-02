"""Experiment bookkeeping helpers shared by training scripts and tests."""

from __future__ import annotations

import csv
import os
import re

import numpy as np


SUMMARY_RESULT_FIELDS = {
    "bc_final_mse", "final_success_rate", "best_success_rate",
    "final_policy_source", "raw_final_success_rate",
    "raw_final_eval_successes", "raw_final_success_ci_low",
    "raw_final_success_ci_high", "restored_best_success_rate",
    "restored_best_eval_successes", "restored_best_success_ci_low",
    "restored_best_success_ci_high", "best_eval_step",
    "best_human_steps", "best_budget_used_frac", "best_engagements",
    "best_checkpoint_path", "human_steps", "budget_used_frac", "engagements",
    "final_eval_successes", "final_eval_episodes", "final_success_ci_low",
    "final_success_ci_high", "wall_time_s",
}


def sanitize_run_label(label):
    """Filesystem-friendly label for distinguishing experiment configurations."""
    label = str(label or "").strip()
    label = label.replace(".", "p")
    label = re.sub(r"[^A-Za-z0-9_+=.-]+", "_", label)
    return label.strip("_")


def config_run_label(args):
    """Compact label for hyperparameters that materially change the run."""
    late_reg_coef = getattr(args, "bc_actor_reg_late_coef", None)
    if late_reg_coef is None:
        late_reg_coef = args.bc_actor_reg_coef
    fields = [
        ("steps", args.total_steps),
        ("demo", args.n_demos),
        ("ls", args.learning_starts),
        ("bs", args.batch_size),
        ("gs", args.gradient_steps),
        ("bc", args.bc_pretrain_steps),
        ("reg", args.bc_actor_reg_coef),
        ("regs", getattr(args, "bc_actor_reg_schedule", "constant")),
        ("lreg", late_reg_coef),
        ("vref", getattr(args, "voi_reference_policy", "none")),
        ("vlv", getattr(args, "voi_learning_value_scale", 0.0)),
        ("vlvmin", getattr(args, "voi_learning_value_min_disagreement", 0.0)),
        ("vsfloorstep", getattr(args, "voi_score_floor_after_step", 0)),
        ("vsfloor", getattr(args, "voi_score_floor_after_value", 0.0)),
        ("vphase", getattr(args, "voi_phase_guard", "none")),
        ("idemomode", getattr(args, "intervention_demo_mode", "all")),
        ("restorebest", int(bool(getattr(args, "restore_best_model_at_end", False)))),
        ("pace", args.pace),
    ]
    return sanitize_run_label("_".join(f"{k}{v}" for k, v in fields))


def build_run_tag(args):
    run_tag = f"{args.task}_{args.strategy}_b{args.budget}_seed{args.seed}"
    label = sanitize_run_label(args.run_label)
    if args.auto_run_label and not label:
        label = config_run_label(args)
    if label:
        run_tag = f"{run_tag}_{label}"
    return run_tag, label


def write_summary_row(summary_csv, header, row):
    """Replace an existing matching config row, otherwise append.

    A direct rerun overwrites the per-run CSV. If the summary only appended, the
    plotter would later treat repeated runs as extra seeds. We identify a run by
    all non-result fields in the summary schema and keep one row per config.
    """
    row_dict = {
        h: "" if i >= len(row) or row[i] is None else str(row[i])
        for i, h in enumerate(header)
    }
    key_fields = [h for h in header if h not in SUMMARY_RESULT_FIELDS]
    old_rows = []
    if os.path.exists(summary_csv):
        with open(summary_csv, newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames == header:
                for old in reader:
                    if any((old.get(k, "") or "") != row_dict.get(k, "")
                           for k in key_fields):
                        old_rows.append(old)

    with open(summary_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for old in old_rows:
            w.writerow(old)
        w.writerow(row_dict)


def maybe_save_best_checkpoint(model, checkpoint_path, step, success_rate,
                               best_success, best_step, enabled=True):
    """Track the best evaluation and optionally persist the policy checkpoint."""
    success_rate = float(success_rate)
    improved = best_step is None or success_rate > float(best_success)
    if not improved:
        return best_success, best_step, False

    best_success = success_rate
    best_step = int(step)
    if not enabled or not checkpoint_path:
        return best_success, best_step, False

    checkpoint_path = str(checkpoint_path)
    checkpoint_dir = os.path.dirname(checkpoint_path)
    if checkpoint_dir:
        os.makedirs(checkpoint_dir, exist_ok=True)
    model.save(checkpoint_path)
    return best_success, best_step, True


def best_eval_cost_metadata(previous_best_step, new_best_step, current_step,
                            human_steps, budget_used_frac, engagements,
                            current=None):
    """Return cost metadata for the eval that produced the current best policy."""
    current = dict(current or {"human_steps": "", "budget_used_frac": "",
                               "engagements": ""})
    if new_best_step == previous_best_step or new_best_step != int(current_step):
        return current
    return {
        "human_steps": int(human_steps),
        "budget_used_frac": f"{float(budget_used_frac):.4f}",
        "engagements": int(engagements),
    }


def choose_reported_final_eval(raw_final_eval, restored_best_eval=None):
    """Choose which policy evaluation should populate final_* summary fields."""
    if restored_best_eval is None:
        return raw_final_eval, "last_policy"
    return restored_best_eval, "best_checkpoint"


def effective_bc_actor_reg_coef(step, total_steps, base_coef, schedule="constant",
                                late_coef=None, late_start_frac=0.5):
    """BC anchor strength for anti-collapse actor regularization."""
    base_coef = float(base_coef)
    late_coef = base_coef if late_coef is None else float(late_coef)
    if schedule == "constant":
        return base_coef
    if schedule != "linear_late":
        raise ValueError(f"unknown bc actor reg schedule: {schedule}")

    start_frac = float(np.clip(late_start_frac, 0.0, 1.0))
    total_steps = max(1, int(total_steps))
    start_step = start_frac * total_steps
    if step <= start_step:
        return base_coef
    denom = max(1e-6, total_steps - start_step)
    alpha = float(np.clip((step - start_step) / denom, 0.0, 1.0))
    return (1.0 - alpha) * base_coef + alpha * late_coef


def should_add_intervention_demo(intervened, controller, mode="all"):
    """Whether an intervention transition should enter the demo/BC replay.

    `all` preserves the original HIL-SERL-style behavior. `starts` keeps only
    the first transition of each takeover latch, and `none` treats online human
    control as assistance data for the RL buffer without strengthening the BC
    anchor on the whole takeover trajectory.
    """
    mode = str(mode)
    if mode == "all":
        return bool(intervened)
    if mode == "starts":
        return bool(intervened and getattr(controller, "last_started", False))
    if mode == "none":
        return False
    raise ValueError(f"unknown intervention demo replay mode: {mode}")
