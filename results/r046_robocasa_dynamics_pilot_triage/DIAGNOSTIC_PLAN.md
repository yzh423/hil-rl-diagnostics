# R046 RoboCasa Dynamics Benchmark Diagnostic Plan

Date: 2026-07-02

## VOID Status

The user clarified that the reported benchmark belonged to another project.
This diagnostic plan is therefore void for FORESIGHT-HIL and must not guide the
current manuscript or evidence chain.

## Root-Cause Frame

The user-reported benchmark produced `success=5/90` across 10 objects and 9
tasks. That is a feasibility failure, not a paper result. The root cause is not
yet known because the raw `summary.json` has not been inspected. The next
diagnostic step should separate three questions:

1. Are failures concentrated in a few tasks, a few objects, or all combinations?
2. Do candidates fail before dynamics, or do plausible candidates fail the
   `panda_practical_8mm` dynamics gate?
3. Is the bottleneck strictness (`position_tolerance`, candidate limit, settle
   steps, frame substeps) or scene/model configuration (`--auto-fit-panda`,
   Panda XML, object proxies, contacts)?

## First Analysis To Run In The RoboCasa Workspace

Run this in the WSL RoboCasa environment where the raw summary exists:

```bash
cd ~/robocasa/cube_morphtamp_x_v2
conda activate robocasa
export PYTHONPATH=src:tools

python - <<'PY'
import json
from collections import Counter, defaultdict

path = "results/dynamics_calibration_full/summary.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = data.get("rows") or data.get("results") or data.get("benchmarks") or []
print("top-level keys:", sorted(data.keys()))
print("rows:", len(rows))

def get(row, *names):
    for name in names:
        if name in row:
            return row[name]
    return None

by_task = Counter()
ok_task = Counter()
by_obj = Counter()
ok_obj = Counter()
fail_reason = Counter()

for row in rows:
    task = get(row, "task", "task_name")
    obj = get(row, "object", "object_name", "obj")
    ok = bool(get(row, "success", "ok", "passed"))
    reason = get(row, "failure_reason", "reason", "status", "error") or "unknown"
    by_task[task] += 1
    by_obj[obj] += 1
    ok_task[task] += int(ok)
    ok_obj[obj] += int(ok)
    if not ok:
        fail_reason[str(reason)] += 1

print("\nby task")
for task, n in by_task.most_common():
    print(task, ok_task[task], "/", n)

print("\nby object")
for obj, n in by_obj.most_common():
    print(obj, ok_obj[obj], "/", n)

print("\nfailure reasons")
for reason, n in fail_reason.most_common(20):
    print(n, reason)
PY
```

If the script prints `rows: 0`, inspect the top-level keys and adjust the row
path. The goal is a task/object/reason pivot table, not a new benchmark run.

## Minimal Follow-Up Benchmark Slices

Do not rerun the full 90-combination grid until the failure structure is known.
Run small slices that isolate one variable at a time.

### Slice A: Object Sweep On The Easy Task

This checks whether object geometry/contact proxies are already failing before
hard task geometry enters.

```bash
python -m morphtamp_x_v2.cli dynamics-benchmark \
  --objects cube sphere cylinder plate mug_proxy bowl_proxy capsule tall_box flat_box ring \
  --tasks tabletop_easy \
  --panda-xml ~/robocasa/mujoco_menagerie/franka_emika_panda/scene.xml \
  --auto-fit-panda \
  --position-tolerance 0.05 \
  --full-candidate-limit 10 \
  --settle-steps 120 \
  --frame-substeps 8 \
  --dynamics-gate panda_practical_8mm \
  --output-dir results/dynamics_triage_object_easy \
  --output results/dynamics_triage_object_easy/summary.json
```

### Slice B: Task Sweep On One Simple Object

This checks whether task geometry, not object representation, is the dominant
failure source.

```bash
python -m morphtamp_x_v2.cli dynamics-benchmark \
  --objects cube \
  --tasks tabletop_easy over_barrier narrow_slot shelf_pick shelf_place folded_transfer far_corner around_wall under_bridge \
  --panda-xml ~/robocasa/mujoco_menagerie/franka_emika_panda/scene.xml \
  --auto-fit-panda \
  --position-tolerance 0.05 \
  --full-candidate-limit 10 \
  --settle-steps 120 \
  --frame-substeps 8 \
  --dynamics-gate panda_practical_8mm \
  --output-dir results/dynamics_triage_cube_tasks \
  --output results/dynamics_triage_cube_tasks/summary.json
```

### Slice C: Gate-Strictness Check

Repeat Slice A or B while changing only one strictness parameter. Start with
`--full-candidate-limit 20`; if the CLI supports a documented no-gate or relaxed
gate mode in `--help`, compare against that mode in a separate run. Do not
change tolerance, gate, candidate limit, and settle steps all at once.

## Decision Rule

Use RoboCasa as a paper-breadth package only if a small, auditable subset can be
made reproducible and interpretable. A reasonable first gate is:

- at least one easy object/task slice succeeds enough to validate the pipeline;
- failures can be assigned to clear task/object/gate categories;
- the run produces a summary file that can be copied into a new RLpaper result
  directory and audited.

If the low success remains diffuse after the slices, keep the current paper on
Lift plus Stack boundary evidence and describe RoboCasa only as future work.
