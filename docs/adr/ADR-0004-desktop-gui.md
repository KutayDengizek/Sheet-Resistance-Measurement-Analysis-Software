# ADR-0004: Desktop GUI with Tkinter
Status: Accepted
Date: 2026-09-29 (the user asked for "a visual app that I can select folders from my pc and show
results". The agent chose the toolkit and layout; the user may revise either.)

## Context
Lab users should be able to pick sample folders with the mouse and read the results, without a
terminal. ADR-0001 requires an ADR for a GUI and prefers the standard library.

## Decision
- **Toolkit: Tkinter/ttk** (Python stdlib). No new runtime dependency. Entry point `sheetres-gui`
  (`[project.gui-scripts]`, so no console window), plus the double-click launcher
  `Sheet Resistance App.bat` at the repo root.
- **Layout:** a toolbar (Add sample folder… · Add all samples in folder… · Remove selected · Clear ·
  Copy results), a results table with one row per sample and the 6 quantities at 6 significant
  digits, a details pane with full-precision values or the full error message, and a status line
  stating the SD definition.
- **No silent failures in the GUI:** every chosen folder produces a row. Folders that fail to load
  are red rows with the error, never skipped. "Add all samples in folder…" lists *every* subfolder,
  so non-samples show up as error rows. Unexpected exceptions in callbacks open an error dialog,
  because stderr is invisible under the GUI exe. Folders passed on the command line are loaded via
  `root.after`, so they go through the same hook. Choosing an empty folder still yields an error row.
- **Export:** "Copy results (for Excel)" puts a tab-separated table on the clipboard, with full
  `repr` precision and the units in the header cells. Columns: Sample, the 6 quantities, Folder, Status.
  The **decimal separator follows the Windows regional setting** (`,` for German number format), so
  Excel parses the numbers correctly. Tabs and newlines inside error text are flattened.
- The GUI computes nothing itself. It calls `parser.load_sample` → `stats.summarize`, and takes its
  labels and units from `report.QUANTITIES`, the same as the CLI.

## Alternatives considered
- PySide6/Qt: nicer widgets, but a ~100 MB dependency and licensing questions. Unnecessary for a
  table and some buttons.
- A web UI (Streamlit etc.): needs a server and a browser, and brings heavy dependencies.
- Saving to .xlsx directly: needs openpyxl (a dependency). Clipboard TSV pastes into Excel with no
  dependency. Revisit if file export is wanted.

## Consequences
Presentation logic lives in `gui.py`. Its non-Tk parts (`analyze`, `find_sample_folders`,
`results_to_tsv`) are unit-tested; the window itself gets a smoke test that is skipped when no
display is available. Adding plots or file export later requires its own ADR.
