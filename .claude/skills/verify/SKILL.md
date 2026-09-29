---
name: verify
description: Run the verification gate (lint, types, fast or full tests) and interpret the result. Use before every commit, at the end of every unit of work, and whenever asked "is it green?".
---
# Verification runbook

Delegate to the `test-runner` agent when the output could be long. The main thread only needs
the verdict and the failing cases.

1. `uv run ruff check .` and `uv run ruff format --check .`
2. `uv run mypy` (strict; covers src/ and tests/)
3. Fast tier: `uv run pytest -q -m "not slow"`. At milestones, also run the full suite: `uv run pytest -q`.
4. Interpret the result:
   - **Green:** report "green: N passed, T s".
   - **A golden or regression test fails:** the behavior changed. Do **not** touch
     `tests/golden/`. Decide whether the change is a bug (fix the code) or intended (stop and
     ask the human, who then follows the ADR plus approval procedure in `docs/adr/README.md`).
   - **A fixture-based test fails because of the fixture:** fixtures are immutable. Fix the parser
     or add a new fixture sample.
   - **Flaky or environment failure:** re-run once. If it persists, report it as an environment
     issue with the error.
5. Never loosen a tolerance, skip a test, or add `xfail` to get green. Those are human decisions
   recorded in an ADR.

**Done when:** every step above is green, or the failures are reported with file:line and a
diagnosis.
