from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"

SUMMARY_HEADER = (
    "Mean Sheet Resistance (Ohm/square),Standard Deviation,Mean Resistivity (Ohm.m),"
    "Standard Deviation,Mean Conductivity (S/m),Standard Deviation"
)
RAW_HEADER = (
    "Current (A),Voltage (V),Sheet Resistance (Ohm/square),Resistivity (Ohm.m),Conductivity (S/m)"
)


@pytest.fixture
def u1_folder() -> Path:
    return FIXTURES / "260902_U1"


def write_measurement(
    folder: Path,
    name: str,
    summary: str = "400.0,0.1,2.8e-06,1e-09,357142.8,50.0",
    header: str = SUMMARY_HEADER,
) -> Path:
    """Write a minimal instrument-style CSV (raw block, blank line, summary) with CRLF endings."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    lines = [RAW_HEADER, "0.001,0.1,450.8,3.1e-06,322580.6", "", header, summary]
    path.write_bytes(("\r\n".join(lines) + "\r\n").encode("utf-8"))
    return path


def make_sample(root: Path, sample: str = "260101_T1", count: int = 4) -> Path:
    folder = root / sample
    for k in range(1, count + 1):
        write_measurement(folder, f"{sample}_{k}.csv")
    return folder
