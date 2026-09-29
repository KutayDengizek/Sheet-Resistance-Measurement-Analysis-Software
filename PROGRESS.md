# PROGRESS

## CURRENT TASK
Phase 0 (agent infrastructure) is done. **Blocked on the human** for Phase 1: we need an example
sample folder, and the open questions in ADR-0002 need answers.

## NEXT STEP
1. **Human:** put the example folder (e.g. `260918_E4/` with its four CSVs) in the repo root or
   `data/`. Answer ADR-0002 Q1–Q4, including where the film thickness comes from.
2. **Agent:** follow skill `add-fixture-sample` to copy it into `tests/fixtures/260918_E4/`
   (use `cp -n`; fixtures are append-only). Then record the observed CSV layout in
   `docs/domain/input-format.md`: delimiter, encoding, exact names on the second-to-last line,
   units, and whether thickness or resistivity appears in the file.
3. **Agent:** implement `src/sheetres/parser.py` per `docs/components/parser.md` using skill
   `implement-change`. Test first, against the fixture. WATCH: trailing blank lines/BOM
   (MEMORY.md pitfalls). Gate: fast tier green + reviewer pass.
4. Only after ADR-0002 is **Accepted**: implement `stats.py`, then build the golden baseline
   (skill `regenerate-golden`, phase 3).

## Phases
| # | Phase | Status | Acceptance criteria |
|---|-------|--------|---------------------|
| 0 | Agent infrastructure | ✅ done 2026-09-29 | CLAUDE/MEMORY/PROGRESS, vault, commands, skills, agents, hooks verified empirically |
| 1 | Input contract + parser | ⏳ blocked (example data) | Fixture committed; parser returns typed per-file records; every malformed case raises a named error; tests cover each |
| 2 | Statistics core | ⏳ blocked (ADR-0002) | Pure functions; estimators exactly as the ADR says; hand-calculated test values |
| 3 | Golden baseline | ⬜ todo | `tests/golden/<sample>.json` produced by `scripts/regenerate_golden.py`; mutation planted and caught |
| 4 | CLI / presentation | ⬜ todo | `sheetres <folder>` prints the 6 quantities with units; exit code ≠ 0 on bad input |
| 5 | Optional: batch mode / export / GUI | ⬜ undecided | needs an ADR |

### Phase 1 checklist
- [ ] Example folder received and copied to `tests/fixtures/`
- [ ] `docs/domain/input-format.md` updated with the observed layout
- [ ] Parser, plus error types for: wrong file count, name mismatch, missing variable, non-numeric value
- [ ] Tests for each error path

## Journal
- 2026-09-29 — [sessions/2026-09-29-01](docs/sessions/2026-09-29-01.md): set up agent infrastructure; guardrails verified.
