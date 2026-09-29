"""Read one sample folder of instrument CSVs into validated per-measurement records.

Contract: docs/domain/input-format.md. Every deviation raises an InputFormatError subclass whose
message names the file (and line); nothing is skipped or defaulted (CLAUDE.md invariant 3).
"""

from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path

MEASUREMENTS_PER_SAMPLE = 4

# Summary header written by the instrument. The three SD columns share one name, so columns are
# addressed by position only.
SUMMARY_HEADER = (
    "Mean Sheet Resistance (Ohm/square)",
    "Standard Deviation",
    "Mean Resistivity (Ohm.m)",
    "Standard Deviation",
    "Mean Conductivity (S/m)",
    "Standard Deviation",
)
COL_RS, COL_RS_SD, COL_RHO, COL_RHO_SD, COL_SIGMA, COL_SIGMA_SD = range(len(SUMMARY_HEADER))
POSITIVE_COLUMNS = (COL_RS, COL_RHO, COL_SIGMA)


class InputFormatError(ValueError):
    """The input folder or a file in it does not match the documented instrument format."""


class WrongFileCount(InputFormatError):
    pass


class NameMismatch(InputFormatError):
    pass


class MissingSummary(InputFormatError):
    pass


class UnexpectedHeader(InputFormatError):
    pass


class NonNumericValue(InputFormatError):
    pass


@dataclass(frozen=True)
class Measurement:
    """Summary row of one measurement file, in the instrument's units."""

    sample: str
    index: int
    path: Path
    rs_ohm_sq: float
    rs_sd_ohm_sq: float  # within-file SD; informational, not used by stats (ADR-0002)
    rho_ohm_m: float
    rho_sd_ohm_m: float
    sigma_s_per_m: float
    sigma_sd_s_per_m: float


def _csv_entries(folder: Path) -> list[Path]:
    try:
        return sorted(p for p in folder.iterdir() if p.suffix.lower() == ".csv")
    except OSError as exc:
        raise InputFormatError(f"{folder}: folder cannot be read ({exc.strerror})") from exc


def resolve_sample_folder(folder: Path) -> Path:
    """Return the folder holding the CSVs. Accepts a nested export `X/X/*.csv` given as `X`
    (only when `X` itself has no CSVs and `X/X` does)."""
    folder = folder.resolve()
    if not folder.is_dir():
        raise InputFormatError(f"{folder}: sample folder does not exist or is not a directory")
    nested = folder / folder.name
    if not _csv_entries(folder) and nested.is_dir() and _csv_entries(nested):
        return nested
    return folder


def load_sample(folder: Path, expected_count: int = MEASUREMENTS_PER_SAMPLE) -> list[Measurement]:
    """Load and validate all measurement files of one sample, sorted by measurement index."""
    folder = resolve_sample_folder(folder)
    sample = folder.name
    pattern = re.compile(rf"^{re.escape(sample)}_(\d+)\.csv$", re.IGNORECASE)

    by_index: dict[int, Path] = {}
    for path in _csv_entries(folder):
        if not path.is_file():
            raise NameMismatch(f"{path}: expected a measurement file, found a directory")
        m = pattern.match(path.name)
        if m is None:
            raise NameMismatch(
                f"{path}: file name does not match '{sample}_<k>.csv' for sample folder '{sample}'"
            )
        k = int(m.group(1))
        if k in by_index:
            raise WrongFileCount(
                f"{path}: measurement {k} appears more than once (also {by_index[k].name})"
            )
        by_index[k] = path

    expected = set(range(1, expected_count + 1))
    if set(by_index) != expected:
        missing = [f"{sample}_{k}.csv" for k in sorted(expected - set(by_index))]
        extra = [by_index[k].name for k in sorted(set(by_index) - expected)]
        raise WrongFileCount(
            f"{folder}: expected {expected_count} files {sample}_1..{expected_count}.csv; "
            f"missing {missing or 'none'}, unexpected {extra or 'none'}"
        )
    return [_read_measurement(by_index[k], sample, k) for k in sorted(expected)]


def _read_measurement(path: Path, sample: str, index: int) -> Measurement:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise InputFormatError(
            f"{path}: not UTF-8 text ({exc.reason} at byte {exc.start})"
        ) from exc
    except OSError as exc:
        raise InputFormatError(f"{path}: cannot be read ({exc.strerror})") from exc
    lines = [(n, line) for n, line in enumerate(text.splitlines(), start=1) if line.strip()]
    if len(lines) < len(("header", "values")):
        raise MissingSummary(f"{path}: needs a summary header line and a value line at the end")
    (header_no, header_line), (values_no, values_line) = lines[-2], lines[-1]

    header = tuple(cell.strip() for cell in next(csv.reader([header_line])))
    if header != SUMMARY_HEADER:
        raise UnexpectedHeader(
            f"{path}:{header_no}: summary header {list(header)} != expected {list(SUMMARY_HEADER)}"
        )
    cells = [cell.strip() for cell in next(csv.reader([values_line]))]
    if len(cells) != len(SUMMARY_HEADER):
        raise MissingSummary(
            f"{path}:{values_no}: expected {len(SUMMARY_HEADER)} values, found {len(cells)}"
        )
    values = [_to_float(cell, path, values_no, col) for col, cell in enumerate(cells)]
    for col in POSITIVE_COLUMNS:
        if values[col] <= 0:
            raise NonNumericValue(
                f"{path}:{values_no}: '{SUMMARY_HEADER[col]}' must be > 0, got {values[col]!r}"
            )
    return Measurement(
        sample=sample,
        index=index,
        path=path,
        rs_ohm_sq=values[COL_RS],
        rs_sd_ohm_sq=values[COL_RS_SD],
        rho_ohm_m=values[COL_RHO],
        rho_sd_ohm_m=values[COL_RHO_SD],
        sigma_s_per_m=values[COL_SIGMA],
        sigma_sd_s_per_m=values[COL_SIGMA_SD],
    )


def _to_float(cell: str, path: Path, line_no: int, col: int) -> float:
    where = f"{path}:{line_no}: column {col + 1} ('{SUMMARY_HEADER[col]}')"
    try:
        value = float(cell)
    except ValueError:
        raise NonNumericValue(f"{where} is not a number: {cell!r}") from None
    if not math.isfinite(value):
        raise NonNumericValue(f"{where} is not finite: {cell!r}")
    return value
