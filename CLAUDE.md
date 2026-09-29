# Sheet Resistance Measurement Analysis

Python tool that takes one **sample folder** of four-point-probe exports (e.g. `260918_E4/` containing
`260918_E4_1.csv` … `260918_E4_4.csv`), reads the summary values from the last two lines of each CSV,
and reports mean ± standard deviation of **sheet resistance**, **resistivity** and **conductivity**
over the four measurements. Lab staff use the results to characterize thin films. A silent error
(wrong row read, dropped file, unit slip, wrong estimator) produces a number that looks plausible and
can mislead material or process decisions. Prefer a loud failure to a quiet wrong answer.

**Units:** sheet resistance Rs in Ω/sq; thickness t in the unit recorded in the data (confirm
per [docs/domain/input-format.md](docs/domain/input-format.md)); resistivity ρ = Rs·t in Ω·cm; conductivity σ = 1/ρ in S/cm. Every
quantity in code carries its unit in the name or docstring (`rs_ohm_sq`, `rho_ohm_cm`).

## Session protocol
- **Start:** `/resume` (reads MEMORY.md, PROGRESS.md, latest `docs/sessions/` note, then states the plan).
- **End:** `/handoff` (PROGRESS.md CURRENT TASK/NEXT STEP, MEMORY.md lessons, journal note, commit).
- Context running low? Don't start a new unit of work. Run `/handoff` instead.

## Repository map
```
src/sheetres/        package: parser (CSV → records), stats (pure aggregation), cli/report
tests/               pytest; tests/fixtures/ = raw exports (append-only), tests/golden/ = expected outputs
scripts/             regenerate_golden.py (the only sanctioned writer of tests/golden/)
docs/                knowledge vault (Obsidian) → start at docs/00-index.md; ADRs in docs/adr/
.claude/             commands (/resume, /handoff), skills, agents, hooks, settings.json
```

## Commands
```
uv sync                         # create/refresh .venv (Python ≥ 3.11)
uv run pytest -m "not slow"     # fast tier (what the commit hook runs)
uv run pytest                   # full suite
uv run ruff check . && uv run ruff format --check . && uv run mypy
```

## Hard invariants
1. **Raw exports are immutable.** `tests/fixtures/**` is append-only. *(hook-enforced)*
2. **Golden data is protected.** `tests/golden/**` changes only via `scripts/regenerate_golden.py`
   plus an Accepted ADR plus a human-created `.claude/approvals/golden.approved`. Never edit
   expected values to make a test pass. *(hook-enforced)*
3. **No silent failures.** A missing, extra or malformed file, a missing variable, or a
   non-numeric value raises an error that names the file and line. Never skip data, and never
   default a value to 0/NaN. No bare `except`, no `except: pass`. *(ruff BLE/S110/S112, on write)*
4. **Statistics are defined by ADR, not improvised.** Estimators (ddof, SD vs SEM, how σ/ρ are
   derived) follow [ADR-0002](docs/adr/ADR-0002-statistical-definitions.md). Changing one requires a new ADR.
5. **Explicit units, no magic numbers.** Name every conversion constant. *(ruff PLR2004)*
6. **Every commit is green:** ruff + mypy --strict + fast tests. No `--no-verify`. *(hook-enforced)*
7. **Pure core.** `stats` does no I/O. Parsing, computation and presentation stay separate.
8. **Decisions need ADRs:** a new dependency, any change to the CSV contract, output format,
   estimators, or golden data. Anything that is "on purpose" but looks odd.

## Commits
`type(scope): what and why` (types: feat, fix, refactor, test, docs, chore). Keep each commit
atomic and green. End every commit with the Co-Authored-By trailer.

## Pointers
Vault hub: [docs/00-index.md](docs/00-index.md) · Agent roles: `.claude/agents/` (implementer,
reviewer, test-runner) · Skills: `.claude/skills/` · Plan and status: [PROGRESS.md](PROGRESS.md)
· Lessons: [MEMORY.md](MEMORY.md)
