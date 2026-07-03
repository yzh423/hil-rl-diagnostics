# R054 Visual QA

Date: 2026-07-03

## Verdict

PASS for use as an optimized paper-figure candidate.

The figure removes two presentation risks in earlier assets: a dual-y trace
panel and proportion-only timing bars that could make small trace counts look
more certain than they are. The new R054 figure uses separate panels for each
diagnostic quantity and includes raw event starts or distribution displays
where appropriate.

## Checks

| Check | Status | Note |
|---|---|---|
| No dual y axes | PASS | Geometry and starts are now separated. |
| No unsupported mean bars | PASS | Budget uses box-plus-strip; geometry uses median/IQR markers. |
| Raw event visibility | PASS | Timing panel shows every intervention start as a raster mark. |
| Colorblind / grayscale robustness | PASS | A grayscale preview is generated; key panels also use position, shape, or direct labels. |
| Text clipping | PASS | PNG preview shows no clipped axis labels, panel labels, or annotations. |
| Legend overlap | PASS | Legends sit in empty plot regions and do not cover key data. |
| Claim scope | PASS | The figure supports a diagnostic protocol interpretation and does not claim LV-VoI superiority. |

## Known Limits

- The figure is a dense double-column diagnostic candidate. It should be used
  where a full evidence summary is appropriate, not as a tiny single-column
  inset.
- Panels a and b show relative success/cost positions rather than pairwise
  confidence intervals. The registered R036 tables remain the canonical source
  for Wilson intervals.
- Panel e summarizes gripper-cube geometry with median/IQR instead of plotting
  every geometry point to keep the panel readable.

## Files Checked

| File | Role |
|---|---|
| `figures/fig_attention_allocation_diagnostics_r054.png` | Color preview. |
| `figures/fig_attention_allocation_diagnostics_r054_grayscale.png` | Grayscale preview. |
| `results/r054_attention_allocation_figure_optimization/attention_allocation_trace_profile.csv` | Derived data profile. |
