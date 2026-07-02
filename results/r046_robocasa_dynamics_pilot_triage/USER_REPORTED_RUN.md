# R046 User-Reported RoboCasa Dynamics Benchmark

Date reported: 2026-07-02

## VOID Status

The user clarified that this benchmark output belonged to another project. It
is retained only as a correction trace and must not be used for the current
FORESIGHT-HIL manuscript.

## Status

This run was reported by the user from a WSL shell outside the current RLpaper
workspace. It is not part of this project.

## Reported Command

```bash
cd ~/robocasa/cube_morphtamp_x_v2
conda activate robocasa
export PYTHONPATH=src:tools

python -m morphtamp_x_v2.cli dynamics-benchmark \
  --objects cube sphere cylinder plate mug_proxy bowl_proxy capsule tall_box flat_box ring \
  --tasks tabletop_easy over_barrier narrow_slot shelf_pick shelf_place folded_transfer far_corner around_wall under_bridge \
  --panda-xml ~/robocasa/mujoco_menagerie/franka_emika_panda/scene.xml \
  --auto-fit-panda \
  --position-tolerance 0.05 \
  --full-candidate-limit 3 \
  --settle-steps 80 \
  --frame-substeps 8 \
  --dynamics-gate panda_practical_8mm \
  --output-dir results/dynamics_calibration_full \
  --output results/dynamics_calibration_full/summary.json
```

## Reported Output

```text
dynamics-benchmark: success=5/90 output=results/dynamics_calibration_full/summary.json
```

## Immediate Interpretation

The reported success rate is too low to support a positive robotics-breadth
claim. The useful next step is not to expand the benchmark. It is to split the
failure by object, task, and gate condition so we can see whether the failures
come from candidate generation, overly strict dynamics acceptance, object
geometry/contact parameters, Panda fit, or task-specific infeasibility.
