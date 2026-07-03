# R058 PDF Visual QA

Date: 2026-07-03

## PDF Under Review

| Artifact | Status |
|---|---|
| `paper/build/main.pdf` | Local build output, ignored by Git. |
| `results/r058_submission_packaging_readiness/main_compiled_r058.pdf` | Archived R058 QA copy. |
| `results/r058_submission_packaging_readiness/pdf_visual_qa/main_after_layout_page-*.png` | Final rendered page images used for visual inspection. |

The final PDF has 14 letter-size pages and was produced by bundled Tectonic
0.16.9 with the project-local cache:

```powershell
$env:TECTONIC_CACHE_DIR='C:\Users\14228\Desktop\RLpaper\.tectonic-cache-dir'
$env:TECTONIC_UNTRUSTED_MODE='1'
C:\Users\14228\.codex\plugins\cache\openai-bundled\latex\0.2.4\bin\tectonic.exe -X compile --only-cached --outdir C:\Users\14228\Desktop\RLpaper\paper\build --outfmt pdf --print --reruns 2 --untrusted main.tex
```

The TeX cache was populated earlier through the same command without
`--only-cached`, after approval for Tectonic to download the default bundle and
missing font/map resources.

## Fixes Applied Before Final QA

- Added `paper/figures/` compile-local snapshots for the table and PDF figure
  assets included by `paper/main.tex`.
- Added `.tectonic-cache-dir/`, `paper/build/`, and the temporary smoke-build
  directory to `.gitignore`.
- Switched `hyperref` to `hidelinks` so citation/reference boxes are not shown
  in the submission PDF.
- Set the two large Results figures to page floats and added a float clear
  before Discussion so Fig. 1 and Fig. 2 are both present and readable.
- Added a clear page before the reference list so appendix floats finish before
  `References`.
- Replaced long `\texttt{...}` file paths in the reproducibility inventory
  table with `\path{...}` so paths can wrap inside table cells.

## Visual Inspection

| Page(s) | Check | Result |
|---|---|---|
| 1 | Title, abstract, Note to Practitioners, start of Introduction | Pass. Text is readable and not clipped. |
| 4-5 | Protocol gate matrix and checklist tables | Pass with mild dense table wrapping. No overlap or clipping. |
| 6 | Fig. 1 methodology protocol | Pass. Figure and caption are visible. |
| 7 | Registry-generated main and repair tables | Pass. Tables fit within margins. |
| 8 | Fig. 2 attention-allocation diagnostics | Pass. All panels and caption are visible. |
| 10-12 | Appendix reproducibility inventory and compute/accounting table | Pass. Tables are separated from references and no longer overlap. |
| 13-14 | References | Pass. References begin after appendix material and are readable. |

## Remaining Warnings

The compile still emits underfull/overfull box warnings in dense tables,
especially the protocol checklist, failure taxonomy, and reproducibility
inventory. Visual inspection shows these warnings are layout-density warnings,
not fatal clipping or overlap in the current rendered PDF.

Tectonic also reports a Windows fontconfig warning:

```text
Fontconfig error: Cannot load default config file: No such file: (null)
```

The warning does not prevent the final PDF from rendering correctly after the
Tectonic bundle cache is populated.

## Verdict

PDF compilation and first visual QA are complete for the current draft. The
current PDF is suitable for manuscript iteration, with the caveat that final
venue formatting will still require venue template integration and another
visual QA pass.
