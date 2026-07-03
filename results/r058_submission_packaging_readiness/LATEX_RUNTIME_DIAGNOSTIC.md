# R058 LaTeX Runtime Diagnostic

Date: 2026-07-03

## Goal

Resolve or clearly classify the local PDF compilation gate for the current
manuscript at `paper/main.tex`, then determine whether PDF visual QA can run in
this workspace.

## Commands Attempted

Tool discovery:

```powershell
where.exe pdflatex
where.exe latexmk
where.exe tectonic
```

Result: none of these tools are available on `PATH`.

Bundled LaTeX plugin doctor:

```powershell
python -X utf8 C:\Users\14228\.codex\plugins\cache\openai-bundled\latex\0.2.4\scripts\latex_doctor.py --json
```

Result:

- TeX Live / MacTeX tooling was missing (`latexmk`, `pdflatex`, `kpsewhich`,
  `xelatex`, `lualatex`, and `biber` were unavailable).
- Bundled Tectonic was found at
  `C:\Users\14228\.codex\plugins\cache\openai-bundled\latex\0.2.4\bin\tectonic.exe`.
- Bundled Tectonic version: `Tectonic 0.16.9`.
- The Tectonic smoke test failed with Windows `os error 183`:
  "Cannot create a file when that file already exists."

Manuscript compile through the bundled plugin:

```powershell
python -X utf8 C:\Users\14228\.codex\plugins\cache\openai-bundled\latex\0.2.4\scripts\compile_latex.py C:\Users\14228\Desktop\RLpaper\paper\main.tex --output-directory C:\Users\14228\Desktop\RLpaper\paper\build --json
```

Result: Tectonic was selected as suitable for the project, but failed with the
same `os error 183`. TeX Live fallback was unavailable.

Direct Tectonic variants:

```powershell
C:\Users\14228\.codex\plugins\cache\openai-bundled\latex\0.2.4\bin\tectonic.exe -X compile --outdir C:\Users\14228\Desktop\RLpaper\paper\build_xdg_cache --outfmt pdf --print --untrusted main.tex
C:\Users\14228\.codex\plugins\cache\openai-bundled\latex\0.2.4\bin\tectonic.exe -X compile --outdir C:\Users\14228\Desktop\RLpaper\paper\build_no_untrusted --outfmt pdf --print main.tex
C:\Users\14228\.codex\plugins\cache\openai-bundled\latex\0.2.4\bin\tectonic.exe -X compile --only-cached --outdir C:\Users\14228\Desktop\RLpaper\paper\build_only_cached --outfmt pdf --print main.tex
```

Result: all variants failed before TeX processing with the same `os error 183`.

Minimal source isolation:

```latex
\documentclass{article}
\begin{document}
Smoke test.
\end{document}
```

Compiled with:

```powershell
C:\Users\14228\.codex\plugins\cache\openai-bundled\latex\0.2.4\bin\tectonic.exe -X compile --outdir C:\Users\14228\Desktop\RLpaper\tmp_tectonic_smoke_build --outfmt pdf --print tmp_tectonic_smoke.tex
```

Result: the minimal file failed with the same `os error 183`, confirming that
the observed failure is not specific to the manuscript source or figures.

Managed TeX Live installer:

```powershell
python -X utf8 C:\Users\14228\.codex\plugins\cache\openai-bundled\latex\0.2.4\scripts\install_texlive.py --install-managed-full
```

Result: the installer did not install TeX Live on this machine because the
managed full install path is supported by the plugin on macOS/Linux only.

## Diagnosis

The initial local PDF compile gate was caused by the Windows Tectonic cache
location. Tectonic failed with `os error 183` until `TECTONIC_CACHE_DIR` was
redirected to a project-local directory:

```powershell
$env:TECTONIC_CACHE_DIR='C:\Users\14228\Desktop\RLpaper\.tectonic-cache-dir'
```

After that change, Tectonic could initialize and process the manuscript. The
first network-enabled compile populated the default bundle cache and missing
font/map resources. Subsequent builds can run with `--only-cached`.

The remaining source-side issue was that `paper/main.tex` includes assets using
`figures/...` relative paths while compilation runs from `paper/`. This was
fixed by adding compile-local snapshots under `paper/figures/`, consistent with
`paper/README.md`.

## Working Compile Command

```powershell
$env:TECTONIC_CACHE_DIR='C:\Users\14228\Desktop\RLpaper\.tectonic-cache-dir'
$env:TECTONIC_UNTRUSTED_MODE='1'
C:\Users\14228\.codex\plugins\cache\openai-bundled\latex\0.2.4\bin\tectonic.exe -X compile --only-cached --outdir C:\Users\14228\Desktop\RLpaper\paper\build --outfmt pdf --print --reruns 2 --untrusted main.tex
```

Output:

- `paper/build/main.pdf`
- archived QA copy:
  `results/r058_submission_packaging_readiness/main_compiled_r058.pdf`

## Remaining Caveats

- TeX Live/MiKTeX tools remain unavailable on `PATH`.
- The local Tectonic cache is intentionally ignored by Git.
- The compile emits layout-density warnings in several dense tables.
- Final venue template integration should rerun compile and visual QA.
