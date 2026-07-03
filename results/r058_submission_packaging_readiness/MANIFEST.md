# R058 Submission Packaging Readiness Pass

Date: 2026-07-03

## Purpose

R058 records the first execution pass for submission packaging readiness after
R057. It focuses on local PDF compilation, PDF visual QA readiness, public Git
source-state tracking, and whether an institutional source archive should be
prepared before submission.

This package does not add a new experiment, change raw evidence, change
manuscript numerical claims, add citation keys, or change the protected
negative LV-VoI result boundary.

## Inputs Reviewed

| Artifact | Role |
|---|---|
| `paper/main.tex` | Current manuscript entry point for PDF compilation. |
| `paper/sections/` | Current manuscript section sources. |
| `figures/` | Current figure and registry-generated table assets. |
| `results/r047_evidence_provenance_package/` | Evidence/source/hash provenance layer. |
| `results/r048_version_command_provenance/` | Historical source-snapshot repair and command-provenance boundary. |
| `results/r049_provenance_validation/` | Executable provenance validation gate. |
| Current Git repository | Source-state tracking for post-R048 project work. |

## Outputs

| Artifact | Purpose |
|---|---|
| `results/r058_submission_packaging_readiness/LATEX_RUNTIME_DIAGNOSTIC.md` | Records the local LaTeX/Tectonic diagnosis, cache fix, and compile command. |
| `results/r058_submission_packaging_readiness/PDF_VISUAL_QA.md` | Records the compiled PDF, rendered page images, visual inspection, and remaining warnings. |
| `results/r058_submission_packaging_readiness/SUBMISSION_PACKAGING_REVIEW.md` | Records packaging, visual-QA, source-archive, and evidence-boundary status. |
| `results/r058_submission_packaging_readiness/SOURCE_ARCHIVE_DECISION.md` | Decides how public Git and a future institutional archive should be used together. |
| `results/r058_submission_packaging_readiness/SUBMISSION_CHECKLIST.md` | Tracks the remaining submission-readiness gates. |
| `results/r058_submission_packaging_readiness/main_compiled_r058.pdf` | Archived compiled PDF for this pass. |
| `results/r058_submission_packaging_readiness/pdf_visual_qa/main_after_layout_page-*.png` | Final rendered page images for QA. |
| `results/EXPERIMENT_EVIDENCE_REGISTRY.csv` | Registers R058 as a project-packaging artifact row. |

## Current Verdict

The repository source state is ready to be tracked through the public GitHub
repository, while R047/R048 remain the evidence and historical source-snapshot
provenance records. Local PDF compilation and first visual QA are now complete
through bundled Tectonic 0.16.9 after redirecting `TECTONIC_CACHE_DIR` to a
project-local cache and adding compile-local `paper/figures/` snapshots.

The resulting PDF is archived at
`results/r058_submission_packaging_readiness/main_compiled_r058.pdf`. Remaining
warnings are dense-table underfull/overfull box warnings, not hard compile
failures.

## Claim Boundary

R058 is a submission-readiness and packaging artifact. It supports future
release hygiene and reviewer packaging, but it should not be used as empirical
evidence for LV-VoI, random baselines, Stack transfer, real-human validation,
or real-robot validation.
