# Component: parser (`src/sheetres/parser.py`)
Status: **implemented** 2026-09-29, tested against fixture `260902_U1`

**Purpose.** Turn a sample folder into 4 validated `Measurement` records. It is the only component
that touches the filesystem on the input side.

**Interface.**
- `resolve_sample_folder(folder) -> Path`: returns `folder`, or `folder/folder.name` when `folder`
  has no CSVs and contains a same-named subfolder (a nested export).
- `load_sample(folder, expected_count=4) -> list[Measurement]`, sorted by index.
- `Measurement`: `sample, index, path, rs_ohm_sq, rs_sd_ohm_sq, rho_ohm_m, rho_sd_ohm_m,
  sigma_s_per_m, sigma_sd_s_per_m`. The `*_sd_*` fields are the within-file SDs; they are kept for
  information but unused by stats.

**Errors** (all subclass `InputFormatError(ValueError)`, messages give `path:line`):
`WrongFileCount` (missing, extra or duplicate k), `NameMismatch` (a CSV not named `<sample>_<k>.csv`),
`MissingSummary` (fewer than 2 non-empty lines, or ≠ 6 values), `UnexpectedHeader` (any change in
the 6 summary names), `NonNumericValue` (unparsable, NaN/inf, or a mean ≤ 0).

**Invariants.** Never skip a file. Never coerce a value. Columns are addressed by position
(`COL_*`) because `Standard Deviation` repeats. Non-CSV files in the folder are ignored.

See [[../domain/input-format]].
