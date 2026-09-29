# Component: gui (`src/sheetres/gui.py`)
Status: **implemented** 2026-09-29 per [[../adr/ADR-0004-desktop-gui]]

**Start.** Double-click `Sheet Resistance App.bat`, or run `uv run sheetres-gui [folder ...]`.
Folders given as arguments are loaded at start.

**Pure, tested parts.**
- `analyze(folder) -> SampleResult`: exactly one of `summary` or `error` is set. `folder` is
  resolved to an absolute path. `short_error` is the first line of the error without the long
  folder prefix.
- `find_sample_folders(parent)`: returns `[parent]` if it is itself a sample (it holds CSVs, or is
  a nested export). Otherwise it returns all its subfolders, sorted, non-samples included.
- `results_to_tsv(results, decimal)`: the clipboard export (full precision; empty numbers and "Error: …"
  for failed rows). The GUI passes `system_decimal_separator()` (Windows regional setting).
- `SampleResult.identity`: the normcased resolved sample folder. `X` and `X/X` count as the same sample.

**`App` (Tk).** A Treeview maps item id → `SampleResult`. Re-adding a sample (compared by `identity`)
replaces the row instead of duplicating it. `report_callback_exception`
shows an error dialog.

**Quirks.** Tk's `askdirectory` selects one folder per dialog. For many samples, use "Add all
samples in folder…". The screenshot scripts used for visual checks live outside the repo; the
window title is `Sheet Resistance Analysis`.

**Distribution.** Colleagues need the folder and `uv` (the launcher runs `uv sync`; the first run is
online). A standalone PyInstaller exe is proposed, not decided (PROGRESS 6b).

Related: [[cli]], [[stats]], [[parser]]
