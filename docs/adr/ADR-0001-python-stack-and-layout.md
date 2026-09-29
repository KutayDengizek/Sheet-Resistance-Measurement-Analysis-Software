# ADR-0001: Python stack and repository layout
Status: Accepted
Date: 2026-09-29

## Context
The tool reads small CSV exports (four files per sample) and computes a handful of statistics.
It must be easy to run on lab PCs (Windows) and easy for agents to verify mechanically.

## Decision
- Python ≥ 3.11, managed with **uv** (`uv sync`, `uv run …`), package `sheetres` in a `src/` layout.
- Dev tooling: **pytest** (fast tier = `-m "not slow"`), **ruff** (lint + format, including
  BLE/S110/S112 against swallowed errors and PLR2004 against magic numbers), **mypy --strict**.
- **Stdlib-first:** `csv`, `statistics`, `pathlib`, `dataclasses`. No runtime dependencies until an
  ADR justifies one. numpy and pandas are not needed at n = 4.
- Architecture: `parser` (I/O, validation) → `stats` (pure) → `cli`/report (presentation).

## Alternatives considered
- pandas for CSV parsing — heavy dependency. Its type inference could silently coerce the
  summary lines.
- MATLAB/LabVIEW — can't be mechanically linted or tested in the agent loop.

## Consequences
Hooks can run ruff/mypy/pytest on every write and commit. Adding plotting, a GUI or Excel
export later requires its own ADR.
