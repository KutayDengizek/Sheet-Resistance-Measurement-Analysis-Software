from pathlib import Path

import pytest

from conftest import make_sample, write_measurement
from sheetres.parser import (
    InputFormatError,
    MissingSummary,
    NameMismatch,
    NonNumericValue,
    UnexpectedHeader,
    WrongFileCount,
    load_sample,
    resolve_sample_folder,
)


def test_fixture_u1_values_read_by_position(u1_folder: Path) -> None:
    ms = load_sample(u1_folder)
    assert [m.index for m in ms] == [1, 2, 3, 4]
    assert all(m.sample == "260902_U1" for m in ms)
    # Values copied by hand from the last line of tests/fixtures/260902_U1/260902_U1_1.csv
    m1 = ms[0]
    assert m1.rs_ohm_sq == 437.39957709029943
    assert m1.rs_sd_ohm_sq == 0.11282937560880453
    assert m1.rho_ohm_m == 3.0617970396320962e-06
    assert m1.rho_sd_ohm_m == 7.89805629261629e-10
    assert m1.sigma_s_per_m == 326605.60239959665
    assert m1.sigma_sd_s_per_m == 84.26674380073895
    assert ms[3].rs_ohm_sq == 433.3297324777792


def test_accepts_nested_export_folder(tmp_path: Path) -> None:
    inner = make_sample(tmp_path / "260101_T1")
    (tmp_path / "260101_T1" / "CLAUDE.md").write_text("notes", encoding="utf-8")
    assert resolve_sample_folder(tmp_path / "260101_T1") == inner
    assert len(load_sample(tmp_path / "260101_T1")) == 4


def test_missing_folder(tmp_path: Path) -> None:
    with pytest.raises(InputFormatError, match="does not exist"):
        load_sample(tmp_path / "nope")


def test_three_files_is_an_error(tmp_path: Path) -> None:
    folder = make_sample(tmp_path, count=3)
    with pytest.raises(WrongFileCount, match=r"_4\.csv"):
        load_sample(folder)


def test_fifth_file_is_an_error(tmp_path: Path) -> None:
    folder = make_sample(tmp_path, count=5)
    with pytest.raises(WrongFileCount, match=r"_5\.csv"):
        load_sample(folder)


def test_foreign_csv_is_an_error(tmp_path: Path) -> None:
    folder = make_sample(tmp_path)
    write_measurement(folder, "other_1.csv")
    with pytest.raises(NameMismatch, match=r"other_1\.csv"):
        load_sample(folder)


def test_duplicate_index_is_an_error(tmp_path: Path) -> None:
    folder = make_sample(tmp_path)
    write_measurement(folder, "260101_T1_01.csv")
    with pytest.raises(WrongFileCount, match="more than once"):
        load_sample(folder)


def test_non_csv_files_are_ignored(tmp_path: Path) -> None:
    folder = make_sample(tmp_path)
    (folder / "notes.txt").write_text("x", encoding="utf-8")
    assert len(load_sample(folder)) == 4


def test_renamed_summary_column_is_an_error(tmp_path: Path) -> None:
    folder = make_sample(tmp_path)
    bad = "Mean Sheet Resistance (Ohm/sq),Standard Deviation,Mean Resistivity (Ohm.m),"
    bad += "Standard Deviation,Mean Conductivity (S/m),Standard Deviation"
    write_measurement(folder, "260101_T1_2.csv", header=bad)
    with pytest.raises(UnexpectedHeader, match=r"260101_T1_2\.csv:4"):
        load_sample(folder)


def test_non_numeric_value_is_an_error(tmp_path: Path) -> None:
    folder = make_sample(tmp_path)
    write_measurement(folder, "260101_T1_3.csv", summary="400.0,0.1,abc,1e-09,357142.8,50.0")
    with pytest.raises(NonNumericValue, match=r"260101_T1_3\.csv:5.*'abc'"):
        load_sample(folder)


@pytest.mark.parametrize("value", ["nan", "inf", ""])
def test_non_finite_or_empty_value_is_an_error(tmp_path: Path, value: str) -> None:
    folder = make_sample(tmp_path)
    write_measurement(folder, "260101_T1_1.csv", summary=f"{value},0.1,2.8e-06,1e-09,3.5e5,50.0")
    with pytest.raises(NonNumericValue):
        load_sample(folder)


@pytest.mark.parametrize(
    "summary", ["0,0.1,2.8e-06,1e-09,3.5e5,50", "400,0.1,-2.8e-06,1e-9,3.5e5,5"]
)
def test_non_positive_mean_is_an_error(tmp_path: Path, summary: str) -> None:
    folder = make_sample(tmp_path)
    write_measurement(folder, "260101_T1_4.csv", summary=summary)
    with pytest.raises(NonNumericValue, match="must be > 0"):
        load_sample(folder)


def test_wrong_field_count_is_an_error(tmp_path: Path) -> None:
    folder = make_sample(tmp_path)
    write_measurement(folder, "260101_T1_1.csv", summary="400.0,0.1,2.8e-06")
    with pytest.raises(MissingSummary, match="6 values"):
        load_sample(folder)


def test_file_without_summary_is_an_error(tmp_path: Path) -> None:
    folder = make_sample(tmp_path)
    (folder / "260101_T1_2.csv").write_bytes(b"only one line\r\n")
    with pytest.raises(MissingSummary, match=r"260101_T1_2\.csv"):
        load_sample(folder)


def test_non_utf8_file_is_an_error_naming_the_file(tmp_path: Path) -> None:
    folder = make_sample(tmp_path)
    (folder / "260101_T1_3.csv").write_bytes(b"\xff\xfe\x00garbage\r\n")
    with pytest.raises(InputFormatError, match=r"260101_T1_3\.csv: not UTF-8"):
        load_sample(folder)


def test_directory_named_like_csv_is_an_error(tmp_path: Path) -> None:
    folder = make_sample(tmp_path)
    (folder / "extra.csv").mkdir()
    with pytest.raises(NameMismatch, match="found a directory"):
        load_sample(folder)


def test_relative_dot_path_works(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    folder = make_sample(tmp_path)
    monkeypatch.chdir(folder)
    assert [m.sample for m in load_sample(Path("."))] == ["260101_T1"] * 4


def test_uppercase_extension_counts_as_csv_for_nesting(tmp_path: Path) -> None:
    outer = tmp_path / "260101_T1"
    make_sample(outer)  # nested outer/260101_T1/*.csv
    write_measurement(outer, "260101_T1_1.CSV")
    with pytest.raises(WrongFileCount):  # outer has a CSV, so it is NOT treated as nested
        load_sample(outer)


def test_same_named_subfolder_without_csvs_is_not_treated_as_nested(tmp_path: Path) -> None:
    outer = tmp_path / "260101_T1"
    (outer / "260101_T1").mkdir(parents=True)
    assert resolve_sample_folder(outer) == outer.resolve()
