# PROGRESS

## CURRENT TASK
Phases 1, 2 and 4 are done: `uv run sheetres <sample-folder>` prints the six quantities for a sample.
Next is Phase 3 (golden baseline), which needs a one-time approval from the human.

## NEXT STEP
1. **Human:** create the file `.claude/approvals/golden.approved` containing the text `ADR-0003`.
   Agents cannot create it (see docs/adr/README.md).
2. **Agent:** implement `scripts/regenerate_golden.py`. For every folder in `tests/fixtures/`, run
   `summarize(load_sample(...))` and write `tests/golden/<sample>.json` (dataclasses.asdict, full float
   repr, sorted keys). Then add `tests/test_golden.py`, parametrized over the fixture folders. It must
   **fail** when a golden file is missing, so it can never pass as "empty == empty", and compare
   with `rel=1e-12`. Follow skill `regenerate-golden`, including the mutation step: change
   `standard_deviation = statistics.stdev` to `pstdev` and confirm the golden test fails with a message
   that names the quantity. Revert, commit `test(golden): baseline per ADR-0002/ADR-0003`, then ask the human to
   delete the marker.
3. Reviewer NOTEs left open (see journal 2026-09-29-02): the raw-data block is not validated; the within-file
   SDs are not checked for ≥ 0; `NonNumericValue` is also used for ≤ 0 values. Pick these up only if the
   human wants stricter validation.
4. Phase 5 options for the human to decide (each needs an ADR): a batch mode over `data/*`, CSV/JSON
   export, a GUI.

## Phases
| # | Phase | Status | Acceptance criteria |
|---|-------|--------|---------------------|
| 0 | Agent infrastructure | ✅ done 2026-09-29 | CLAUDE/MEMORY/PROGRESS, vault, commands, skills, agents, hooks verified empirically |
| 1 | Input contract + parser | ✅ done 2026-09-29 | Fixture 260902_U1 committed; typed records; each malformed case raises a named error; tests cover each |
| 2 | Statistics core | ✅ done 2026-09-29 | ADR-0002 + ADR-0003 Accepted; pure `summarize`; sample SD (n − 1); hand-calculated tests |
| 3 | Golden baseline | ⏳ waiting on approval marker | `tests/golden/<sample>.json` produced by the script; mutation planted and caught |
| 4 | CLI / presentation | ✅ done 2026-09-29 | `sheetres <folder>` prints the 6 quantities with units; exit code 2 on bad input |
| 5 | Optional: batch mode / export / GUI | ⬜ undecided | needs an ADR |

## Journal
- 2026-09-29 — [sessions/2026-09-29-01](docs/sessions/2026-09-29-01.md): set up agent infrastructure; guardrails verified.
- 2026-09-29 — [sessions/2026-09-29-02](docs/sessions/2026-09-29-02.md): fixture 260902_U1; ADR-0002 accepted; parser, stats, CLI implemented and reviewed.
