# MEMORY — long-term project lessons

Distilled, dated knowledge that was expensive to learn. Budget: < 200 lines. When it grows, move
older entries into vault notes and leave a link. When two entries conflict, the newer one wins.

## Key decisions
- 2026-09-29 — Python ≥ 3.11, uv, src layout, pytest/ruff/mypy --strict, stdlib-first (no runtime
  deps yet) → [ADR-0001](docs/adr/ADR-0001-python-stack-and-layout.md)
- 2026-09-29 — **Accepted (user):** mean of the four per-file means.
  Within-file SDs are ignored. ρ and σ come from the files (no thickness). Units stay as in the
  files → [ADR-0002](docs/adr/ADR-0002-statistical-definitions.md)
- 2026-09-29 — **User: divide by n − 1 for all SDs** (sample SD, `statistics.stdev`), which supersedes
  ADR-0002's population SD → [ADR-0003](docs/adr/ADR-0003-sample-standard-deviation.md). The
  instrument's within-file SDs divide by **n**, so the tool deliberately differs from them. Don't
  "align" the two.
- 2026-09-29 — Desktop GUI = Tkinter (stdlib), launched by `Sheet Resistance App.bat` → [ADR-0004](docs/adr/ADR-0004-desktop-gui.md)
- 2026-09-29 — The CLI accepts a nested export `X/X/*.csv` given as `X` (user decision).
- 2026-09-29 — Work lives on `main`, and `origin` is github.com/KutayDengizek/Sheet-Resistance-Measurement-Analysis-Software
  (published by the human via GitHub Desktop; `gh` is not installed). `git fetch`/`git push` from the agent shell hung
  for more than 60 s, waiting for credentials. Use `GIT_TERMINAL_PROMPT=0` with a timeout, or ask the human to push in GitHub Desktop.
- 2026-09-29 — The user is in a lab setting; colleagues are likely non-developers. Distribution today:
  `uv` + `Sheet Resistance App.bat`. A PyInstaller `.exe` was offered; it is undecided and needs ADR-0005.
- 2026-09-29 — The user prefers short free-text questions with a stated default over multiple-choice
  prompts for routine next steps; two such prompts were rejected.

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
- 2026-09-29 — **GUI visual check:** launch the app in the background, then take a PowerShell
  `CopyFromScreen` of its window. Find the window through `Get-Process | ? MainWindowTitle -eq 'Sheet Resistance Analysis'`.
  `FindWindow($null, …)` fails from PowerShell, because `$null` becomes "". The shell cannot run
  `"Sheet Resistance App.bat"` through `cmd //c` (the spaces split the path); use `powershell -Command "& '.\Sheet Resistance App.bat'"`.
- 2026-09-29 — Stderr is invisible when the GUI runs as `sheetres-gui.exe`/pythonw. Tk callback errors
  go through `App._show_unexpected_error` (a dialog). Keep that hook.

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
