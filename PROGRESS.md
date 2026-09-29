# PROGRESS

## CURRENT TASK
The app is feature-complete for one sample type (CLI + Tkinter GUI, sample SD n − 1), on `main`, and
published to GitHub (`origin` = github.com/KutayDengizek/Sheet-Resistance-Measurement-Analysis-Software).
The golden baseline (Phase 3) still waits on the approval marker.

## NEXT STEP
1. **Human (open):**
   a. Confirm the GitHub repo is **private** (it holds real lab CSVs in `tests/fixtures/260902_U1`); the agent
      cannot check visibility. Delete the redundant local branch `setup/agent-infrastructure`.
   b. Golden approval: create `.claude/approvals/golden.approved` containing `ADR-0003`.
   c. Decide whether colleagues get a standalone `.exe` (Phase 6b below).
2. **Pushing:** `git push origin main` from the agent shell can hang waiting for credentials (no terminal
   prompt). Use `GIT_TERMINAL_PROMPT=0` with a timeout; if it fails, ask the human to click *Push origin* in
   GitHub Desktop. WATCH: never force-push, and never change repo visibility.
3. **When the marker exists:** implement `scripts/regenerate_golden.py` (for every `tests/fixtures/*`:
   `summarize(load_sample(...))` → `tests/golden/<sample>.json`, `dataclasses.asdict`, sorted keys, full
   float repr) and `tests/test_golden.py` (parametrized over the fixture folders; it must **fail** when a golden
   file is missing; compare with `rel=1e-12`). Follow skill `regenerate-golden`, including the mutation step
   (`standard_deviation = statistics.stdev` → `pstdev` must make the golden test fail and name the quantity; then
   revert). WATCH: the bash hook blocks any command mentioning `tests/golden` or `regenerate_golden` until the
   marker exists. Gate: fast tier + reviewer. Commit `test(golden): baseline per ADR-0002/ADR-0003`, then ask
   the human to delete the marker.
4. **If an .exe is wanted (6b):** draft ADR-0005 (PyInstaller as a dev-only build tool; one-file, windowed
   `sheetres-gui`), add `pyinstaller` to the dev group, and add `scripts/build_exe.py` → `dist/SheetResistance.exe`
   (`dist/` is already gitignored). Verify by launching the exe with `data/260902_U1` and a screenshot (see the
   MEMORY pitfall on screenshots). WATCH: unsigned exe → SmartScreen warning; document it in README.
5. Deferred reviewer NOTEs (only if the human wants stricter validation): the raw-data block is not
   validated; the within-file SDs are not checked for ≥ 0; `NonNumericValue` is also used for ≤ 0 values;
   GUI tracebacks are not written to a log file.

## Phases
| # | Phase | Status | Acceptance criteria |
|---|-------|--------|---------------------|
| 0 | Agent infrastructure | ✅ done 2026-09-29 | CLAUDE/MEMORY/PROGRESS, vault, commands, skills, agents, hooks verified empirically |
| 1 | Input contract + parser | ✅ done 2026-09-29 | Fixture 260902_U1 committed; typed records; each malformed case raises a named error; tests cover each |
| 2 | Statistics core | ✅ done 2026-09-29 | ADR-0002 + ADR-0003 Accepted; pure `summarize`; sample SD (n − 1); hand-calculated tests |
| 3 | Golden baseline | ⏳ waiting on approval marker | `tests/golden/<sample>.json` produced by the script; mutation planted and caught |
| 4 | CLI / presentation | ✅ done 2026-09-29 | `sheetres <folder>` prints the 6 quantities with units; exit code 2 on bad input |
| 5a | Desktop GUI | ✅ done 2026-09-29 | ADR-0004; pick folders; table + details; red error rows; copy for Excel; screenshot-verified |
| 5b | Optional: file export / plots | ⬜ undecided | needs an ADR |
| 6a | Publish to GitHub | ✅ done 2026-09-29 (via GitHub Desktop) | `main` pushed with full history; visibility to be confirmed by the human |
| 6b | Optional: standalone .exe | ⬜ undecided | ADR-0005; the exe runs on a PC without uv/Python |

## Journal
- 2026-09-29 — [sessions/2026-09-29-01](docs/sessions/2026-09-29-01.md): set up agent infrastructure; guardrails verified.
- 2026-09-29 — [sessions/2026-09-29-02](docs/sessions/2026-09-29-02.md): fixture 260902_U1; ADR-0002/0003 accepted; parser, stats, CLI, GUI implemented and reviewed.
- 2026-09-29 — [sessions/2026-09-29-03](docs/sessions/2026-09-29-03.md): merged into main; published to GitHub by the human; distribution options prepared; handoff.
