# R056 Methodology Extension

Date: 2026-07-03

## Purpose

R056 strengthens the paper's methodological contribution without adding a new
experiment or changing the protected result boundary. It derives a protocol gate
matrix, a failure-mode taxonomy, a small set of diagnostic metrics, and a
methodology-first Fig. 1 candidate from already registered R021/R023/R024
evidence.

The intended manuscript use is to make the contribution read as an auditable
cost-matched HIL-RL diagnostic protocol for human-attention allocation, rather
than as a failed positive LV-VoI method paper.

## Inputs

| Source | Role |
|---|---|
| `results/r021_random_costmatch/r021_costmatch_aggregate.csv` | Cost-matched Lift success/cost comparison: random b350 versus LV-VoI scale3. |
| `results/r023_real_trace_seed0_2/r023_trace_strategy_diagnostics.csv` | Start-level trace diagnosis for random b350 and LV-VoI scale3. |
| `results/r024_score_floor_seed0_2/r024_score_floor_aggregate.csv` | Same-seed score-floor repair and random b350 comparison. |
| `results/r024_score_floor_seed0_2/r024_trace_strategy_compare.csv` | Score-floor trace follow-up and start-count comparison. |

No historical raw CSV was edited.

## Derived Outputs

| Output | Description |
|---|---|
| `protocol_gate_matrix.csv` | Four protocol gates and their case-study verdicts. |
| `failure_taxonomy.csv` | Failure-mode taxonomy induced by the R021/R023/R024 diagnostic evidence. |
| `derived_attention_metrics.csv` | Small derived metric table used for stop-rule visualization and auditability. |
| `figures/TABLE_protocol_gate_matrix_r056.tex` | Manuscript-ready gate matrix table. |
| `figures/TABLE_failure_taxonomy_r056.tex` | Manuscript-ready failure taxonomy table. |
| `figures/fig1_methodology_protocol_r056.pdf` | Methodology-first Fig. 1 candidate. |
| `figures/fig1_methodology_protocol_r056.png` | PNG preview for visual QA and README use. |
| `figures/fig1_methodology_protocol_r056_grayscale.png` | Grayscale preview for color-robustness checks. |
| `scripts/generate_methodology_extension.py` | Rebuilds R056 CSV and LaTeX table artifacts. |
| `figures/gen_r056_methodology_figure.py` | Rebuilds the R056 methodology figure and grayscale preview. |
| `foresight_hil/evaluation/protocol_diagnostics.py` | Tested helper module for derived protocol diagnostics. |
| `tests/test_protocol_diagnostics.py` | Regression tests for the derived diagnostic helper. |

## Derived Metric Definitions

| Metric | Formula |
|---|---|
| `random_b350_success_margin_vs_lv_voi_pp` | `100 * (random_b350_success - lv_voi_scale3_success)` from R021. |
| `random_b350_human_step_saving_vs_lv_voi` | `lv_voi_scale3_cost - random_b350_cost` from R021. |
| `lv_voi_start_inflation_vs_random` | `lv_voi_trace_starts / random_b350_trace_starts` from R023. |
| `score_floor_start_reduction_vs_lv_voi` | `(lv_voi_trace_starts - score_floor_trace_starts) / lv_voi_trace_starts` from R024 traces. |
| `score_floor_gap_closure_vs_random` | `(lv_voi_trace_starts - score_floor_trace_starts) / (lv_voi_trace_starts - random_trace_starts)` from R024 traces. |
| `score_floor_success_gap_vs_random_pp` | `100 * (score_floor_success - same_seed_random_b350_success)` from R024 aggregate. |

## Visual QA

The R056 methodology figure follows the project figure discipline:

- no dual y axes;
- no mean-only bar chart for small derived samples;
- no pie chart or 3D chart;
- colorblind-friendly palette inherited from `figures/paper_plot_style.py`;
- grayscale preview generated and inspected;
- long gate explanations moved to tables and prose to avoid over-compressed
  figure text.

The first generated draft was rejected because panel b text overlapped and panel
c title/label spacing was too tight. The current version uses a short
gate/evidence/verdict matrix and shorter metric title, and the grayscale preview
remains legible.

## Claim Boundary

R056 is a derived methodology and presentation package. It supports claims such
as:

- the protocol can be stated as explicit cost, repeat-evaluation, trace, and
  repair-stop gates;
- the current Lift case study reaches a reject/diagnose/stop verdict under
  those gates;
- the failure taxonomy is induced by registered R021/R023/R024 evidence.

R056 does not support claims that:

- LV-VoI is superior to cost-matched random;
- the score-floor repair is a positive method result;
- trace diagnostics overturn the R021 success-cost reversal;
- the project has real-human or real-robot validation.

## Verification Record

Executed on 2026-07-03 after R056 code, figure, manuscript, registry, and audit
updates:

| Command | Result |
|---|---|
| `python -m unittest tests.test_protocol_diagnostics` | PASS: 3 tests. |
| `python scripts\generate_methodology_extension.py` | PASS: regenerated 3 R056 CSVs and 2 LaTeX tables. |
| `python figures\gen_r056_methodology_figure.py` | PASS: regenerated PDF, PNG, and grayscale preview. |
| `python figures\gen_r054_attention_allocation_diagnostics.py` | PASS: regenerated R054 profile and figure assets after the `math` import repair. |
| `python scripts\validate_evidence_registry.py` | PASS: 47 rows, 47 sources, 0 issues. |
| `python scripts\audit_registry_numbers.py` | PASS: 94 numeric checks, 0 issues. |
| `python scripts\generate_claim_tables.py` | PASS: regenerated 5 R036 claim-table assets. |
| `python scripts\generate_stack_boundary_appendix.py` | PASS: regenerated 2 R053 Stack appendix assets. |
| `python scripts\validate_provenance_package.py` | PASS: 6 checks, 289 files, 0 issues. |
| `python -m unittest discover -s tests` | PASS: 84 tests. A Gym deprecation warning was printed and is not a current test failure. |
| `python -m json.tool paper\PAPER_CLAIM_AUDIT.json` | PASS: JSON audit file parses. |
| `git diff --check` | PASS: no whitespace errors; Git printed line-ending normalization warnings for previously generated text assets. |

LaTeX PDF compilation was not rerun in this pass because the project dashboard
still records a local LaTeX runtime/cache caveat.
