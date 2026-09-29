# Input format: sample folders and instrument CSVs

**Status: confirmed** against fixture `tests/fixtures/260902_U1/` (2026-09-29).

## Folder
- One sample = one folder named after the sample, `YYMMDD_<id>` (e.g. `260902_U1`), holding exactly
  4 files `<sample>_1.csv` … `<sample>_4.csv`. The suffix is the measurement number.
- **Nested exports occur:** `data/260902_U1/260902_U1/*.csv`, where the outer folder also held a
  `CLAUDE.md` describing the data. The CLI accepts the outer folder when it contains no CSVs and
  has a subfolder with the same name (user decision, 2026-09-29).
- Non-CSV files in the sample folder are ignored. Any extra `*.csv` is an error.

## File layout (all four files are identical in structure)
1. Header: `Current (A),Voltage (V),Sheet Resistance (Ohm/square),Resistivity (Ohm.m),Conductivity (S/m)`
2. 27 raw measurement rows, 5 columns
3. One blank line
4. Summary header, 6 columns: `Mean Sheet Resistance (Ohm/square),Standard Deviation,Mean Resistivity (Ohm.m),Standard Deviation,Mean Conductivity (S/m),Standard Deviation`
5. Summary values, 6 columns

- Delimiter `,`, decimal point `.`, no BOM, CRLF line endings, a trailing CRLF after the last row.
- Numbers carry full float precision and may use exponent notation (`3.06e-06`).
- **The name `Standard Deviation` appears three times.** Columns must be addressed by position
  (1, 3, 5), never by name through a dict.
- Units are SI: resistivity is in **Ω·m** and conductivity in **S/m**, not Ω·cm or S/cm.

## Instrument-side relationships (observed in the data; not used by the tool)
- Rs = 4.50797 · V/I. The correction factor is ≈ 4.508, not π/ln2 ≈ 4.532.
- ρ = Rs · 7e-9 m, so the instrument assumes a 7 nm film. σ = 1/ρ.

## Contract the parser enforces
Exactly 4 files with k = 1..4, and the file prefix equals the folder name. The last two non-empty
lines are the summary. The header must match the 6 expected names exactly, in order. The values are
6 finite numbers, and the three means are > 0. Any violation raises `InputFormatError` (or a
subclass), with the file path and line number in the message.

Related: [[../components/parser]], [[sheet-resistance]]
