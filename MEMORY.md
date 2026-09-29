# MEMORY — long-term project lessons

Distilled, dated knowledge that was expensive to learn. Budget: < 200 lines. When it grows, move
older entries into vault notes and leave a link. When two entries conflict, the newer one wins.

## Key decisions
- 2026-09-29 — Python ≥ 3.11, uv, src layout, pytest/ruff/mypy --strict, stdlib-first (no runtime
  deps yet) → [ADR-0001](docs/adr/ADR-0001-python-stack-and-layout.md)
- 2026-09-29 — **Accepted (user):** mean plus **population SD (ddof = 0)** of the four per-file means.
  Within-file SDs are ignored. ρ and σ come from the files (no thickness). Units stay as in the
  files → [ADR-0002](docs/adr/ADR-0002-statistical-definitions.md)
- 2026-09-29 — The CLI accepts a nested export `X/X/*.csv` given as `X` (user decision).

## Known pitfalls
- 2026-09-29 — **Mean of conductivities ≠ 1/(mean resistivity).** Averaging and inverting don't
  commute. The tool reports mean(σ_k), which is intended (ADR-0002). Don't "fix" it.
- 2026-09-29 — **The summary header repeats `Standard Deviation` three times.** A dict/DictReader
  keeps only the last one. Always address summary columns by position (`parser.COL_*`).
- 2026-09-29 — The instrument uses **SI units**: resistivity in Ohm.m, conductivity in S/m. Don't
  assume Ω·cm (a factor of 100).
- 2026-09-29 — The files have CRLF endings, a blank line before the summary, and a trailing CRLF.
  The parser takes the last two *non-empty* lines. `.gitattributes` has `tests/fixtures/** -text`
  so git never rewrites the fixture bytes.
- 2026-09-29 — Sample exports may contain a `CLAUDE.md` written for the data folder. Never copy it
  into the repo (it would be loaded as agent instructions). Its facts are in
  [docs/domain/input-format.md](docs/domain/input-format.md).
- 2026-09-29 — The bash hook's path guard is a text heuristic: any command whose text mentions
  `tests/fixtures`, `tests/golden` or `.claude/approvals` next to `>`, `rm`, `sed -i`, etc. is blocked,
  even a heredoc that only writes docs. Use the Write/Edit tools for such files.
- 2026-09-29 — ruff also formats the Python code blocks inside Markdown notes.

## Domain invariants
- One sample = one folder `YYMMDD_<id>` containing exactly 4 files `YYMMDD_<id>_<k>.csv`, k = 1..4.
  The folder name and file prefix must match.
- The mean Rs, ρ and σ are all > 0. A non-positive or non-finite value is a data error, not something to clip.
- The instrument's own relations (informational only): Rs = 4.50797·V/I, ρ = Rs·7 nm, σ = 1/ρ.

## Do not
- Do not edit expected values in `tests/golden/` or fixture CSVs to make a test pass.
- Do not silently drop a measurement file that fails to parse, not even when the other three are fine.
- Do not change the estimator (ddof, SD vs SEM) or the units without a superseding ADR.
- Do not add runtime dependencies (numpy/pandas/GUI toolkits) without an ADR.
