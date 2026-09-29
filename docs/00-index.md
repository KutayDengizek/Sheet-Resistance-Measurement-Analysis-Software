# Index (Map of Content)

The hub note. Start here and follow only the links your task needs.

## Domain
- [[domain/sheet-resistance]]: physics, formulas, units (Rs, ρ, σ) and how the three relate.
- [[domain/input-format]]: sample folder and file naming, CSV layout, and what is still unconfirmed.

## Components (one note = one unit of delegable work)
- [[components/parser]]: sample folder → four validated per-measurement records. *(Phase 1)*
- [[components/stats]]: pure aggregation to the six reported quantities. *(Phase 2)*
- [[components/cli]]: `sheetres <folder>` presentation and exit codes. *(Phase 4)*
- [[components/gui]]: Tkinter desktop app: pick folders, results table, copy to Excel. *(Phase 5a)*

## Decisions
- [[adr/README]]: when an ADR is required, the template, and the golden-data approval procedure.
- [[adr/ADR-0001-python-stack-and-layout]]: **Accepted.** Python/uv/pytest/ruff/mypy, stdlib-first.
- [[adr/ADR-0002-statistical-definitions]]: **Accepted.** Mean of per-file means; ρ and σ from the files; units as in the files.
- [[adr/ADR-0003-sample-standard-deviation]]: **Accepted.** Every SD divides by n − 1 (supersedes ADR-0002's SD).
- [[adr/ADR-0004-desktop-gui]]: **Accepted.** Tkinter GUI, no new dependency; clipboard export for Excel.

## Sessions
- `sessions/`: append-only journal, one note per session (`YYYY-MM-DD-NN.md`). Latest: [[sessions/2026-09-29-03]].
