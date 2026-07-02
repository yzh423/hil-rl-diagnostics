# R040 Manuscript Polish

Date: 2026-07-02

## Purpose

R040 strengthens the current-route manuscript prose while preserving the
scientific boundary established by R021-R039. The pass focuses on making the
paper read less like a skeleton and more like a journal-style diagnostic
protocol manuscript.

## Edited Files

| File | Change |
|---|---|
| `paper/main.tex` | Rewrote the abstract to remove skeleton language and foreground the protocol contribution. |
| `paper/sections/01_introduction.tex` | Expanded the introduction into a clearer problem-gap-protocol-contribution arc. |
| `paper/sections/03_protocol_setup.tex` | Expanded the diagnostic protocol and experimental setup with cost matching, repeated checkpoint evaluation, trace diagnostics, case-study scope, and evidence-control language. |
| `paper/sections/06_conclusion.tex` | Rewrote the conclusion around the supported reporting standard. |

## Boundaries Preserved

- No new experimental result was added.
- No raw result file was edited.
- No new citation key or BibTeX entry was added.
- No positive LV-VoI superiority claim was introduced.
- The real-human and real-robot limitations remain explicit.

## Next Writing Target

The next prose target should be `paper/sections/04_results.tex` and
`paper/sections/05_discussion.tex`, with the same constraint: every number must
trace to the evidence registry, and every citation context should be ready for
the later final citation audit.
