# Component: cli / report (`src/sheetres/cli.py`)
Status: **implemented** 2026-09-29 (plain-text table)

**Usage.** `uv run sheetres <sample-folder>`, e.g. `uv run sheetres data/260902_U1`. The nested
export folder is accepted too.

**Output.** 7 lines: the sample name with n, then the 6 quantities with units (`Ohm/square`,
`Ohm.m`, `S/m`) at 6 significant digits. Units are ASCII so the Windows console never chokes on Ω.

**Exit codes.** 0 = ok; 2 = input error (`InputFormatError`), with a one-line message on stderr that
names the file. Anything else is a bug and propagates as a traceback.

**Open.** Machine-readable output (CSV/JSON) and a batch mode over many folders both need an ADR.

Related: [[stats]], [[parser]]
