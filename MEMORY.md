# MEMORY — long-term project lessons

Distilled, dated knowledge that was expensive to learn. Budget: < 200 lines. When it grows, move
older entries into vault notes and leave a link. When two entries conflict, the newer one wins.

## Key decisions
- 2026-09-29 — Python ≥ 3.11, uv, src layout, pytest/ruff/mypy --strict, stdlib-first (no runtime
  deps yet) → [ADR-0001](docs/adr/ADR-0001-python-stack-and-layout.md)
- 2026-09-29 — Statistical definitions are **Proposed, not yet decided**. Open questions are listed
  in [ADR-0002](docs/adr/ADR-0002-statistical-definitions.md). The human decides them.

## Known pitfalls
- 2026-09-29 — **Mean of conductivities ≠ 1/(mean resistivity).** Averaging and inverting don't
  commute (Jensen), so the two give different numbers. Use the method ADR-0002 fixes, and never
  mix the two approaches between code paths.
- 2026-09-29 — **"Standard deviation of the mean" is ambiguous.** It can mean the SD of the four
  per-file means or the standard error (SD/√n). Numpy's default `std` is population (ddof=0) and
  `statistics.stdev` is sample (ddof=1). Always pass or state the ddof explicitly.
- 2026-09-29 — Instrument CSVs keep the summary in the **last two lines** (header row, value row).
  Trailing blank lines, BOMs, `;` delimiters or a decimal comma would shift or break that. Parse
  defensively and fail loudly (see [docs/domain/input-format.md](docs/domain/input-format.md)).
- 2026-09-29 — Hooks load at session start. Edits to `.claude/hooks/*` or `.claude/settings.json`
  take effect in the next session (some versions reload live, but don't rely on it).

## Domain invariants
- One sample = one folder `YYMMDD_<id>` containing exactly 4 files `YYMMDD_<id>_<k>.csv`, k = 1..4.
  The folder name and file prefix must match.
- Rs > 0, t > 0. A non-positive value is a data error, not something to clip.
- ρ = Rs · t (thickness in cm → Ω·cm); σ = 1/ρ (S/cm).

## Do not
- Do not edit expected values in `tests/golden/` or fixture CSVs to make a test pass.
- Do not silently drop a measurement file that fails to parse, not even when the other three are fine.
- Do not pick an estimator (ddof, SD vs SEM, error propagation) that ADR-0002 hasn't settled.
  Ask the human.
- Do not add runtime dependencies (numpy/pandas/GUI toolkits) without an ADR.
