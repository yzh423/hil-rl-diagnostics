import pathlib
import subprocess
import sys

root = pathlib.Path(r"C:\Users\14228\Desktop\RLpaper")
out = root / "results" / "r024_score_floor_seed0_2"
out.mkdir(parents=True, exist_ok=True)
cmd = [
    sys.executable, "-u", "scripts/run_comparison.py",
    "--task", "Lift",
    "--seeds", "0", "1", "2",
    "--strategies", "voi",
    "--budget", "600",
    "--total_steps", "10000",
    "--n_demos", "20",
    "--learning_starts", "500",
    "--batch_size", "256",
    "--gradient_steps", "1",
    "--bc_pretrain_steps", "5000",
    "--bc_actor_reg_coef", "50.0",
    "--eval_at_start",
    "--eval_every", "2000",
    "--eval_episodes", "20",
    "--takeover_len", "20",
    "--voi_tau", "0.01",
    "--voi_cquery", "0.0",
    "--voi_reference_policy", "demo_nn",
    "--voi_learning_value_scale", "3.0",
    "--voi_learning_value_clip", "1.0",
    "--voi_score_floor_after_step", "4000",
    "--voi_score_floor_after_value", "0.05",
    "--trace_interventions",
    "--restore_best_model_at_end",
    "--out_dir", "results\\r024_score_floor_seed0_2",
]
(out / "driver.cmd.txt").write_text(" ".join(cmd), encoding="utf-8")
stdout = open(out / "driver.stdout.log", "wb", buffering=0)
stderr = open(out / "driver.stderr.log", "wb", buffering=0)
flags = 0
for name in ("DETACHED_PROCESS", "CREATE_NEW_PROCESS_GROUP", "CREATE_NO_WINDOW"):
    flags |= getattr(subprocess, name, 0)
proc = subprocess.Popen(
    cmd,
    cwd=str(root),
    stdin=subprocess.DEVNULL,
    stdout=stdout,
    stderr=stderr,
    creationflags=flags,
    close_fds=False,
)
(out / "driver.pid").write_text(str(proc.pid), encoding="utf-8")
print(proc.pid)
