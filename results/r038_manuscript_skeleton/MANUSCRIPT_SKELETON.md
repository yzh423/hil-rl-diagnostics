# R038 Manuscript Skeleton

Date: 2026-07-02

Purpose: create the first claim-tethered manuscript skeleton for the current
diagnostic-protocol paper route.

## Created Draft

The manuscript entry point is:

- `paper/main.tex`

The skeleton uses prose sections rather than outline bullets:

- Introduction
- Related Work
- Diagnostic Protocol and Experimental Setup
- Results
- Discussion
- Conclusion

## Evidence Boundaries

The draft imports the current preferred paper assets:

- `paper/figures/fig1_protocol_hero_r029.pdf`
- `paper/figures/TABLE_protocol_checklist.tex`
- `paper/figures/TABLE_registry_costmatched_results_r036.tex`
- `paper/figures/TABLE_registry_trigger_repairs_r036.tex`

These are compile-local snapshots copied from the project-level `figures/`
directory so Tectonic can compile the paper in untrusted mode.

The numerical claims in the Results section are routed through R036
registry-generated tables instead of copied from raw CSVs.

## Citation Boundaries

The draft uses a local `paper/references.bib` containing only keys supported by
R027/R037 source-bank work. It does not merge staged candidates into
`proposal/references.bib`.

The final citation audit is still deferred. It should be run only after this
skeleton has been revised into the actual draft with stable `\cite{...}`
contexts.

The local citation check found that all 15 `\cite{...}` keys used by the
skeleton are present in `paper/references.bib`. The local BibTeX validator
reported:

```text
Total entries: 15
Valid entries: 15
Errors: 0
Duplicates: 0
Warnings: 12
```

The warnings are recommended-field gaps for proceedings/arXiv entries and are
carried forward for the final citation audit rather than filled from memory.

## Compile Status

The skeleton was checked with the LaTeX compile skill, but the current machine
does not have a complete local LaTeX toolchain:

- TeX Live / latexmk / pdflatex were not detected.
- Bundled Tectonic is present, but sandboxed mode reports access-denied cache
  writes.
- A non-sandboxed cached Tectonic probe reached format generation and then
  failed because cached resource `loadhyph-cu.tex` is missing.

No `paper/main.pdf` was generated in this pass. The current draft keeps
`paper/references.bib` for later citation audit, and uses
`paper/sections/99_references.tex` to avoid BibTeX once a usable LaTeX runtime
is available.

## Next Candidate

R039 should revise the skeleton into a stronger first draft section by section,
starting with Introduction and Diagnostic Protocol. Do not broaden claims beyond
the evidence registry, and do not add uncited literature that has not first
entered the R027/R037 support bank.
