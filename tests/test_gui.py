import tkinter as tk
from collections.abc import Iterator
from pathlib import Path

import pytest

from conftest import make_sample
from sheetres.gui import App, analyze, find_sample_folders, results_to_tsv


def test_analyze_ok(u1_folder: Path) -> None:
    r = analyze(u1_folder)
    assert r.summary is not None and r.error is None
    assert r.name == "260902_U1"
    assert r.summary.rs_mean_ohm_sq == pytest.approx(434.905, abs=1e-3)


def test_analyze_error_is_reported_not_dropped(tmp_path: Path) -> None:
    folder = make_sample(tmp_path, count=3)
    r = analyze(folder)
    assert r.summary is None
    assert r.error is not None and "260101_T1_4.csv" in r.error
    assert r.name == "260101_T1"


def test_find_sample_folders_lists_every_subfolder(tmp_path: Path) -> None:
    make_sample(tmp_path, "260101_A")
    make_sample(tmp_path, "260101_B")
    (tmp_path / "not_a_sample").mkdir()  # included on purpose: shown as an error row, never hidden
    (tmp_path / "readme.txt").write_text("x", encoding="utf-8")
    names = [p.name for p in find_sample_folders(tmp_path)]
    assert names == ["260101_A", "260101_B", "not_a_sample"]


def test_find_sample_folders_on_a_sample_itself_returns_it(u1_folder: Path) -> None:
    assert find_sample_folders(u1_folder) == [u1_folder]


def test_tsv_has_header_full_precision_and_error_rows(u1_folder: Path, tmp_path: Path) -> None:
    ok = analyze(u1_folder)
    bad = analyze(make_sample(tmp_path, count=3))
    lines = results_to_tsv([ok, bad]).splitlines()
    header = lines[0].split("\t")
    assert header[0] == "Sample" and "Mean Rs (Ohm/square)" in header and header[-1] == "Status"
    row = lines[1].split("\t")
    assert row[0] == "260902_U1"
    assert ok.summary is not None
    assert float(row[1]) == ok.summary.rs_mean_ohm_sq  # full precision, not rounded
    assert row[-1] == "OK"
    bad_row = lines[2].split("\t")
    assert bad_row[0] == "260101_T1" and bad_row[1] == "" and bad_row[-1].startswith("Error:")


@pytest.fixture
def app() -> Iterator[App]:
    try:
        root = tk.Tk()
    except tk.TclError as exc:  # no display available (e.g. headless CI)
        pytest.skip(f"Tk display unavailable: {exc}")
    root.withdraw()
    a = App(root)
    yield a
    root.destroy()


def test_app_adds_rows_and_replaces_duplicates(app: App, u1_folder: Path, tmp_path: Path) -> None:
    app.add_folders([u1_folder])
    app.add_folders([u1_folder])  # same folder again: refreshed, not duplicated
    app.add_folders([make_sample(tmp_path, count=3)])
    rows = app.tree.get_children()
    assert len(rows) == 2
    assert app.tree.item(rows[0])["values"][0] == "260902_U1"
    assert "error" in app.tree.item(rows[1])["tags"]
    app.tree.selection_set(rows[1])
    app.root.update()
    assert "260101_T1_4.csv" in app.details.get("1.0", "end")
    app.clear()
    assert app.tree.get_children() == ()


def test_short_error_drops_the_long_folder_prefix(tmp_path: Path) -> None:
    r = analyze(make_sample(tmp_path, count=3))
    assert str(tmp_path) not in r.short_error
    assert r.short_error.startswith("260101_T1: expected 4 files")


def test_empty_parent_still_yields_a_row(tmp_path: Path) -> None:
    (tmp_path / "only.txt").write_text("x", encoding="utf-8")
    assert find_sample_folders(tmp_path) == [tmp_path]
    assert analyze(tmp_path).error is not None


def test_parent_with_same_named_subfolder_without_csvs_lists_all_subfolders(
    tmp_path: Path,
) -> None:
    parent = tmp_path / "data"
    (parent / "data").mkdir(parents=True)  # e.g. data/data/ holding no CSVs
    make_sample(parent, "260101_A")
    assert [p.name for p in find_sample_folders(parent)] == ["260101_A", "data"]


def test_nested_export_short_error_and_identity_are_stable(tmp_path: Path) -> None:
    outer = tmp_path / "260101_T1"
    inner = make_sample(outer, count=3)  # outer/260101_T1/*.csv, one file missing
    r_outer, r_inner = analyze(outer), analyze(inner)
    assert r_outer.short_error == r_inner.short_error
    assert r_outer.short_error.startswith("260101_T1: expected 4 files")
    assert r_outer.identity == r_inner.identity


def test_tsv_uses_given_decimal_separator(u1_folder: Path) -> None:
    ok = analyze(u1_folder)
    assert ok.summary is not None
    row = results_to_tsv([ok], decimal=",").splitlines()[1].split("\t")
    assert row[1] == repr(ok.summary.rs_mean_ohm_sq).replace(".", ",")
    assert "." not in row[1]


def test_tsv_error_cell_never_breaks_rows_or_columns(tmp_path: Path) -> None:
    from sheetres.gui import SampleResult

    r = SampleResult(tmp_path, None, "line one\tcol\nline two")
    lines = results_to_tsv([r]).splitlines()
    assert len(lines) == 2
    assert len(lines[1].split("\t")) == len(lines[0].split("\t"))


def test_app_installs_error_hook_and_merges_nested_duplicates(app: App, tmp_path: Path) -> None:
    assert app.root.report_callback_exception == app._show_unexpected_error
    outer = tmp_path / "260101_T1"
    inner = make_sample(outer)
    app.add_folders([outer, inner])
    assert len(app.tree.get_children()) == 1


def test_app_remove_selected_and_copy_empty(
    app: App, u1_folder: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    shown: list[str] = []
    monkeypatch.setattr("sheetres.gui.messagebox.showinfo", lambda _t, msg: shown.append(msg))
    app.copy_results()
    assert shown and "no results" in shown[0]
    app.add_folders([u1_folder])
    app.tree.selection_set(app.tree.get_children()[0])
    app.remove_selected()
    assert app.tree.get_children() == ()
