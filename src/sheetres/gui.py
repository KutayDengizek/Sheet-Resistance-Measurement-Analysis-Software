"""Desktop app: pick sample folders, see mean and SD of Rs, rho and sigma per sample (ADR-0004).

Run with `uv run sheetres-gui [folder ...]` or double-click `Sheet Resistance App.bat`.
"""

from __future__ import annotations

import locale
import os
import sys
import tkinter as tk
import traceback
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from types import TracebackType

from sheetres.parser import InputFormatError, load_sample, resolve_sample_folder
from sheetres.report import QUANTITIES, SD_NOTE, display, value
from sheetres.stats import SampleSummary, summarize

TITLE = "Sheet Resistance Analysis"
ERROR_COLOR = "#b00020"
PAD = 6


@dataclass(frozen=True)
class SampleResult:
    """Outcome for one folder: exactly one of `summary` / `error` is set."""

    folder: Path
    summary: SampleSummary | None
    error: str | None

    @property
    def name(self) -> str:
        return self.summary.sample if self.summary else self.folder.name

    @property
    def short_error(self) -> str:
        """The error with the long folder prefix removed, e.g. '260101_X9_2.csv:4: summary ...'."""
        if self.error is None:
            return ""
        text = self.error.splitlines()[0]
        bases = {resolve_sample_folder_or_self(self.folder), self.folder}
        for base in sorted(bases, key=lambda b: len(str(b)), reverse=True):  # longest first
            text = text.replace(str(base) + os.sep, "").replace(str(base), base.name)
        return text

    @property
    def identity(self) -> str:
        """Same sample folder -> same identity (so re-adding replaces the row)."""
        return os.path.normcase(str(resolve_sample_folder_or_self(self.folder)))


def resolve_sample_folder_or_self(folder: Path) -> Path:
    try:
        return resolve_sample_folder(folder)
    except InputFormatError:
        return folder.resolve()


def analyze(folder: Path) -> SampleResult:
    folder = folder.resolve()
    try:
        return SampleResult(folder, summarize(load_sample(folder)), None)
    except InputFormatError as exc:
        return SampleResult(folder, None, str(exc))


def find_sample_folders(parent: Path) -> list[Path]:
    """Every subfolder of `parent` (each becomes a result row, errors included). If `parent`
    is itself a sample folder (holds CSVs, or is a nested export) or has no subfolders, return
    just `parent`, so that choosing a folder always yields at least one visible row."""
    try:
        if resolve_sample_folder(parent) != parent.resolve() or any(
            p.suffix.lower() == ".csv" for p in parent.iterdir()
        ):
            return [parent]
        subfolders = sorted(p for p in parent.iterdir() if p.is_dir())
    except (InputFormatError, OSError):
        return [parent]  # analyze() turns it into an error row naming the folder
    return subfolders or [parent]


def system_decimal_separator() -> str:
    """Decimal separator of the user's regional settings (',' in e.g. German Excel)."""
    try:
        locale.setlocale(locale.LC_NUMERIC, "")
        sep = str(locale.localeconv()["decimal_point"])
    except locale.Error:
        return "."
    finally:
        locale.setlocale(locale.LC_NUMERIC, "C")
    return sep or "."


def _tsv_cell(text: str) -> str:
    return " ".join(text.replace("\t", " ").splitlines())


def results_to_tsv(results: Iterable[SampleResult], decimal: str = ".") -> str:
    """Tab-separated table with full-precision numbers, for pasting into Excel. `decimal` must
    match Excel's regional setting, or numbers paste as text / wrong values."""
    header = ["Sample", *(f"{q.short} ({q.unit})" for q in QUANTITIES), "Folder", "Status"]
    lines = ["\t".join(header)]
    for r in results:
        if r.summary is not None:
            nums = [repr(value(r.summary, q)).replace(".", decimal) for q in QUANTITIES]
            status = "OK"
        else:
            nums = [""] * len(QUANTITIES)
            status = f"Error: {r.error}"
        lines.append("\t".join(_tsv_cell(c) for c in [r.name, *nums, str(r.folder), status]))
    return "\n".join(lines) + "\n"


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.results: dict[str, SampleResult] = {}  # tree item id -> result
        root.title(TITLE)
        root.geometry("1400x560")
        root.minsize(800, 380)
        root.report_callback_exception = self._show_unexpected_error

        bar = ttk.Frame(root, padding=PAD)
        bar.pack(fill="x")
        buttons = [
            ("Add sample folder...", self.ask_sample_folder),
            ("Add all samples in folder...", self.ask_parent_folder),
            ("Remove selected", self.remove_selected),
            ("Clear", self.clear),
            ("Copy results (for Excel)", self.copy_results),
        ]
        for text, cmd in buttons:
            ttk.Button(bar, text=text, command=cmd).pack(side="left", padx=(0, PAD))

        columns = ["sample", *(q.attr for q in QUANTITIES), "status"]
        frame = ttk.Frame(root, padding=(PAD, 0))
        frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("sample", text="Sample")
        self.tree.column("sample", width=110, anchor="w", stretch=False)
        for q in QUANTITIES:
            self.tree.heading(q.attr, text=f"{q.short} ({q.unit})")
            self.tree.column(q.attr, width=150, anchor="e", stretch=False)
        self.tree.heading("status", text="Status")
        self.tree.column("status", width=260, anchor="w", stretch=True)
        self.tree.tag_configure("error", foreground=ERROR_COLOR)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", lambda _e: self._show_details())

        ttk.Label(root, text="Details", padding=(PAD, PAD, PAD, 0)).pack(anchor="w")
        self.details = tk.Text(
            root, height=9, wrap="word", relief="flat", padx=PAD, pady=PAD, font=("Consolas", 10)
        )
        self.details.pack(fill="x", padx=PAD)
        self.details.tag_configure("error", foreground=ERROR_COLOR)
        self.status = ttk.Label(root, text=f"Add a sample folder to begin.   {SD_NOTE}.")
        self.status.pack(fill="x", padx=PAD, pady=PAD)
        self._set_details("Select a row to see full-precision values, or the full error message.")

    # --- actions -------------------------------------------------------------------------------

    def ask_sample_folder(self) -> None:
        folder = filedialog.askdirectory(title="Choose a sample folder (e.g. 260902_U1)")
        if folder:
            self.add_folders([Path(folder)])

    def ask_parent_folder(self) -> None:
        folder = filedialog.askdirectory(title="Choose a folder that contains sample folders")
        if folder:
            self.add_folders(find_sample_folders(Path(folder)))

    def add_folders(self, folders: Sequence[Path]) -> None:
        for folder in folders:
            result = analyze(folder)
            existing = [i for i, r in self.results.items() if r.identity == result.identity]
            for item in existing:  # re-adding a folder refreshes its row instead of duplicating
                self.tree.delete(item)
                del self.results[item]
            item = self.tree.insert(
                "", "end", values=self._row_values(result), tags=self._tags(result)
            )
            self.results[item] = result
        self._update_status()

    def remove_selected(self) -> None:
        for item in self.tree.selection():
            self.tree.delete(item)
            del self.results[item]
        self._update_status()
        self._set_details("")

    def clear(self) -> None:
        self.tree.delete(*self.tree.get_children())
        self.results.clear()
        self._update_status()
        self._set_details("")

    def copy_results(self) -> None:
        ordered = [self.results[i] for i in self.tree.get_children()]
        if not ordered:
            messagebox.showinfo(TITLE, "There are no results to copy yet.")
            return
        decimal = system_decimal_separator()
        self.root.clipboard_clear()
        self.root.clipboard_append(results_to_tsv(ordered, decimal=decimal))
        self.status.configure(
            text=f"Copied {len(ordered)} row(s) with '{decimal}' as decimal separator "
            "(your Windows setting). Paste into Excel with Ctrl+V."
        )

    # --- helpers -------------------------------------------------------------------------------

    @staticmethod
    def _row_values(r: SampleResult) -> list[str]:
        if r.summary is None:
            return [r.name, *([""] * len(QUANTITIES)), f"Error: {r.short_error}"]
        return [r.name, *(display(value(r.summary, q)) for q in QUANTITIES), "OK"]

    @staticmethod
    def _tags(r: SampleResult) -> tuple[str, ...]:
        return ("error",) if r.summary is None else ()

    def _show_details(self) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        r = self.results[sel[0]]
        if r.summary is None:
            self._set_details(f"{r.name}   {r.folder}\n\nError: {r.error}", error=True)
            return
        s = r.summary
        width = max(len(q.label) for q in QUANTITIES)
        lines = [f"{s.sample}   {r.folder}   (n = {s.n} measurement files)", ""]
        lines += [f"{q.label:<{width}}  {value(s, q)!r} {q.unit}" for q in QUANTITIES]
        self._set_details("\n".join(lines))

    def _set_details(self, text: str, error: bool = False) -> None:
        self.details.configure(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", text, ("error",) if error else ())
        self.details.configure(state="disabled")

    def _update_status(self) -> None:
        n_ok = sum(r.summary is not None for r in self.results.values())
        n_err = len(self.results) - n_ok
        errors = f", {n_err} with errors (red)" if n_err else ""
        self.status.configure(text=f"{n_ok} sample(s) analyzed{errors}.   {SD_NOTE}.")

    def _show_unexpected_error(
        self, exc: type[BaseException], val: BaseException, tb: TracebackType | None
    ) -> None:
        """A bug must never fail silently, even when started without a console (pythonw)."""
        detail = "".join(traceback.format_exception(exc, val, tb))
        print(detail, file=sys.stderr)
        messagebox.showerror(TITLE, f"Unexpected error (please report):\n\n{detail[-1500:]}")


def main(argv: Sequence[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else list(argv)
    root = tk.Tk()
    app = App(root)
    if args:  # scheduled, so errors go through the dialog hook instead of a silent exit
        root.after(0, app.add_folders, [Path(a) for a in args])
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
