# Sheet Resistance Measurement Analysis

Takes a sample folder of four-point-probe exports (`260902_U1/` with `260902_U1_1.csv` …
`260902_U1_4.csv`) and reports, over the 4 measurements:

| Quantity | Unit |
|---|---|
| Mean sheet resistance, and its standard deviation | Ohm/square |
| Mean resistivity, and its standard deviation | Ohm.m |
| Mean conductivity, and its standard deviation | S/m |

Only the last two lines of each CSV (the instrument's summary row) are used. Standard deviations
are sample SDs (divide by n − 1).

## Desktop app
Double-click **`Sheet Resistance App.bat`**. Then:
- **Add sample folder…**: pick one sample folder (either the folder with the CSVs, or an outer
  folder of the same name that contains it).
- **Add all samples in folder…**: pick a folder such as `data\`, and every sample inside it is analyzed.
- Click a row to see full-precision values, or the full error message. Rows in red could not be analyzed.
- **Copy results (for Excel)**: then press Ctrl+V in Excel.

## Command line
```powershell
uv run sheetres data\260902_U1
```

## Setup (new computer)
Install [uv](https://docs.astral.sh/uv/). The launcher runs `uv sync` itself; or run `uv sync`
once in this folder. Tests: `uv run pytest`.

Contributor and agent documentation: [CLAUDE.md](CLAUDE.md), with the knowledge vault in [docs/](docs/00-index.md).
