"""Presentation metadata shared by the CLI and the GUI: which quantities are shown, with units."""

from __future__ import annotations

from dataclasses import dataclass

from sheetres.stats import SampleSummary

SD_NOTE = "SD = sample standard deviation (divide by n-1) over the measurement files"


@dataclass(frozen=True)
class Quantity:
    label: str
    short: str  # column heading
    attr: str  # SampleSummary field
    unit: str  # exactly as the instrument writes it (ADR-0002)


QUANTITIES = (
    Quantity("Mean sheet resistance", "Mean Rs", "rs_mean_ohm_sq", "Ohm/square"),
    Quantity("Std. dev. of mean sheet resistance", "SD Rs", "rs_sd_ohm_sq", "Ohm/square"),
    Quantity("Mean resistivity", "Mean rho", "rho_mean_ohm_m", "Ohm.m"),
    Quantity("Std. dev. of mean resistivity", "SD rho", "rho_sd_ohm_m", "Ohm.m"),
    Quantity("Mean conductivity", "Mean sigma", "sigma_mean_s_per_m", "S/m"),
    Quantity("Std. dev. of mean conductivity", "SD sigma", "sigma_sd_s_per_m", "S/m"),
)


def value(summary: SampleSummary, q: Quantity) -> float:
    v = getattr(summary, q.attr)
    if not isinstance(v, float):
        raise TypeError(f"SampleSummary.{q.attr} is {type(v).__name__}, expected float")
    return v


def display(v: float) -> str:
    """Human-readable value (6 significant digits). Exports use full precision instead."""
    return f"{v:.6g}"
