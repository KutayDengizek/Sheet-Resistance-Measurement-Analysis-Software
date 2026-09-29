# Input format: sample folders and instrument CSVs

**Status: partially known.** Update this note once the example folder arrives (PROGRESS.md NEXT STEP).

## Known (from the user, 2026-09-29)
- One sample = one folder named after the sample, e.g. `260918_E4` (looks like a `YYMMDD` date + sample id).
- It contains 4 measurement CSVs: `260918_E4_1` … `260918_E4_4`. The suffix is the measurement number.
- In each CSV, the **last two lines** hold the summary: the second-to-last line has the variable
  names, the last line has their values. Example names: `Mean Sheet Resistance (Ohm/square)`,
  `Standard Deviation`, and more.

## To confirm with the example (fill in)
- [ ] File extension and exact file names; are there any other files in the folder?
- [ ] Delimiter (`,` vs `;`), decimal separator, encoding/BOM, trailing blank lines
- [ ] Full list of summary variable names, exactly as written, with their units
- [ ] Does the CSV contain thickness, resistivity or conductivity already?
- [ ] What precedes the summary lines (per-point raw data?), and could it help validate the summary?

## Contract the parser enforces (draft)
Exactly 4 files with k = 1..4. The file prefix equals the folder name. The summary lines are the last
two **non-empty** lines, with equal field counts. The required variables are present and numeric
and greater than 0. Any violation raises an error that names the file.

Related: [[../components/parser]], [[sheet-resistance]]
