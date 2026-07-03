# Figure Asset Index

Last updated: 2026-07-03

This file consolidates paper figure and table assets across R026, R029, R036,
R053, and R054.

## Preferred Current Assets

| Asset | Source | Status | Use |
|---|---|---|---|
| `fig1_protocol_hero_r029.pdf` | R029 | Preferred Fig. 1 candidate | Protocol-centered hero figure: gates, cost-matched reversal, and trace diagnosis. |
| `fig1_protocol_hero_r029.png` | R029 | Preview | Raster preview for quick inspection. |
| `fig_attention_allocation_diagnostics_r054.pdf` | R054 | Preferred diagnostic composite candidate | Multi-panel attention-allocation diagnostics: cost-matched reversal, repair stop gate, timing raster, budget fraction, geometry, and score/`p_fail`. |
| `fig_attention_allocation_diagnostics_r054.png` | R054 | Preview | Raster preview for visual inspection and README use. |
| `fig_attention_allocation_diagnostics_r054_grayscale.png` | R054 | Grayscale QA preview | Color-robustness check for the R054 diagnostic composite. |
| `TABLE_protocol_checklist.tex` | R029 | Paper-ready draft | Diagnostic protocol checklist table. |
| `fig2_cost_matched_frontier.pdf` | R026 | Paper-ready draft | Success-cost frontier for cost-matched Lift evidence. |
| `fig3_trigger_repairs.pdf` | R026 | Paper-ready draft | R022/R024 repair comparison against random_b350. |
| `fig4_intervention_timing.pdf` | R026 | Paper-ready draft | Intervention timing distribution. |
| `fig5_score_over_time.pdf` | R026 | Paper-ready draft | R024 score-over-time diagnostic. |
| `TABLE_main_costmatched_results.tex` | R026 | Paper-ready draft | Main cost-matched results table. |
| `TABLE_negative_findings.tex` | R026 | Paper-ready draft | Negative trigger-repair findings table. |
| `TABLE_trace_diagnostics.tex` | R026 | Paper-ready draft | Compact trace diagnostic table. |
| `TABLE_registry_costmatched_results_r036.tex` | R036 | Preferred registry-generated table | Main cost-matched result table generated directly from audited registry rows. |
| `TABLE_registry_trigger_repairs_r036.tex` | R036 | Preferred registry-generated table | Trigger-repair result table generated directly from audited registry rows. |
| `TABLE_stack_boundary_appendix_r053.tex` | R053 | Appendix-ready registry-generated table | Stack boundary evidence table; use only as negative robotics breadth evidence. |
| `latex_includes_r036.tex` | R036 | Include snippets | LaTeX `\input{}` snippets for R036 tables. |
| `latex_includes_r054.tex` | R054 | Include snippet | Optional LaTeX figure snippet for the R054 diagnostic composite. |

## Older Or Secondary Assets

| Asset | Status | Note |
|---|---|---|
| `fig1_hero_diagnostic_summary.pdf` | Secondary | Earlier R026 hero candidate; keep for comparison but prefer R029 for the diagnostic-protocol framing. |
| `latex_includes.tex` | R026 include snippets | Includes R026 figures/tables. |
| `latex_includes_r029.tex` | R029 include snippets | Includes the protocol hero and checklist table. |
| `qa_rendered/` | QA previews | Rendered PNG previews and contact sheet for visual inspection. |

## Regeneration

| Script | Regenerates |
|---|---|
| `gen_r026_paper_figures.py` | R026 figures, R026 tables, R026 include snippets. |
| `gen_r029_protocol_assets.py` | R029 protocol hero, checklist table, and R029 include snippets. |
| `gen_r054_attention_allocation_diagnostics.py` | R054 attention-allocation diagnostic composite, PNG/grayscale previews, and trace profile CSV. |
| `foresight_hil/evaluation/attention_diagnostics.py` | R055-tested trace-row collection and profile generation used by the R054 figure script. |
| `scripts/generate_claim_tables.py` | R036 registry-generated Markdown and LaTeX claim tables. |
| `scripts/generate_stack_boundary_appendix.py` | R053 Stack boundary appendix Markdown and LaTeX table. |
| `paper_plot_style.py` | Shared plotting style used by figure scripts. |

Before using a figure in the manuscript, verify that its source result is also
listed in `results/EXPERIMENT_EVIDENCE_REGISTRY.csv`.
