# R054 Attention-Allocation Figure Optimization Manifest

Date: 2026-07-03

## Purpose

R054 adds a scipilot-guided data-figure optimization pass for the current
human-attention allocation paper spine. It does not add a new experiment or
change any historical result. The goal is to make the existing R021/R023/R024
evidence easier to inspect without overstating LV-VoI performance.

## Inputs

| Source | Role |
|---|---|
| `results/r021_random_costmatch/r021_costmatch_aggregate.csv` | Cost-matched Lift success and best-step human cost. |
| `results/r023_real_trace_seed0_2/trace_Lift_random_b350_seed*.csv` | Random b350 intervention-start traces. |
| `results/r023_real_trace_seed0_2/trace_Lift_voi_b600_seed*.csv` | Original LV-VoI scale3 intervention-start traces. |
| `results/r024_score_floor_seed0_2/r024_score_floor_aggregate.csv` | Same-seed score-floor/min-disagree repair outcomes. |
| `results/r024_score_floor_seed0_2/trace_Lift_voi_b600_seed*.csv` | Score-floor intervention-start traces. |

## Outputs

| Artifact | Purpose |
|---|---|
| `foresight_hil/evaluation/attention_diagnostics.py` | Reusable trace-row collection and profile-building helpers used by the figure script. |
| `tests/test_attention_diagnostics.py` | Unit tests for trace profile generation and source collection. |
| `figures/gen_r054_attention_allocation_diagnostics.py` | Reproducible generation script. |
| `figures/fig_attention_allocation_diagnostics_r054.pdf` | Vector publication figure. |
| `figures/fig_attention_allocation_diagnostics_r054.png` | Raster preview for visual QA. |
| `figures/fig_attention_allocation_diagnostics_r054_grayscale.png` | Grayscale preview for color-robustness inspection. |
| `figures/latex_includes_r054.tex` | Optional LaTeX include snippet. |
| `results/r054_attention_allocation_figure_optimization/attention_allocation_trace_profile.csv` | Derived trace profile used for inspection. |
| `results/r054_attention_allocation_figure_optimization/DATA_PROFILE.md` | Human-readable data profiling and chart-choice notes. |
| `results/r054_attention_allocation_figure_optimization/VISUAL_QA.md` | Visual QA checklist and remaining limits. |

## Chart Decisions

- Replace the earlier dual-axis trace summary with separate panels for timing,
  budget fraction, geometry, and score calibration.
- Use relative-delta scatter panels for the two decision gates: R021 vs LV-VoI
  and R024 repairs vs same-seed random b350.
- Use an intervention-start raster instead of proportion-only timing bars so
  the reader sees the event counts and distribution directly.
- Use box-plus-strip displays for budget fraction and median/IQR markers for
  gripper-cube geometry instead of mean bars.
- Use score-vs-`p_fail` scatter for LV-VoI variants to expose clipping and
  threshold stress without claiming calibration has been solved.

## Claim Boundary

R054 supports figure presentation and data inspection only. It should not be
used to claim a new method result, a positive LV-VoI conclusion, real-human
validation, or real-robot validation. The protected evidence boundary remains
R021/R022/R023/R024 as registered in `results/EXPERIMENT_EVIDENCE_REGISTRY.csv`.

## Regeneration

```powershell
python figures\gen_r054_attention_allocation_diagnostics.py
```
