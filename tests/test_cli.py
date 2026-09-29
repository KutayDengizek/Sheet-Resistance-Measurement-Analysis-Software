from pathlib import Path

import pytest

from conftest import make_sample
from sheetres.cli import EXIT_INPUT_ERROR, main


def test_prints_six_quantities_with_units(
    u1_folder: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(u1_folder)]) == 0
    out = capsys.readouterr().out
    assert "Sample 260902_U1" in out
    assert "Mean sheet resistance" in out and "434.905 Ohm/square" in out
    assert "Std. dev. of mean sheet resistance" in out
    assert "Ohm.m" in out and "S/m" in out
    assert len(out.strip().splitlines()) == 7


def test_bad_input_exits_nonzero_and_names_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    folder = make_sample(tmp_path, count=3)
    assert main([str(folder)]) == EXIT_INPUT_ERROR
    err = capsys.readouterr().err
    assert "260101_T1_4.csv" in err
