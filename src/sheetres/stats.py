"""Pure aggregation of per-file means into the six reported quantities (no I/O).

Estimators are fixed by docs/adr/ADR-0002-statistical-definitions.md: arithmetic mean and
population standard deviation (ddof = 0) of the per-file means; within-file SDs are not used.
"""

from __future__ import annotations

import statistics
from collections.abc import Sequence
from dataclasses import dataclass

from sheetres.parser import Measurement

# ADR-0002: population SD (divide by n), i.e. Excel STDEV.P. Changing this requires a new ADR.
standard_deviation = statistics.pstdev


@dataclass(frozen=True)
class SampleSummary:
    sample: str
    n: int
    rs_mean_ohm_sq: float
    rs_sd_ohm_sq: float
    rho_mean_ohm_m: float
    rho_sd_ohm_m: float
    sigma_mean_s_per_m: float
    sigma_sd_s_per_m: float


def summarize(measurements: Sequence[Measurement]) -> SampleSummary:
    if not measurements:
        raise ValueError("summarize: no measurements given")
    samples = {m.sample for m in measurements}
    if len(samples) != 1:
        raise ValueError(f"summarize: measurements from more than one sample: {sorted(samples)}")
    rs = [m.rs_ohm_sq for m in measurements]
    rho = [m.rho_ohm_m for m in measurements]
    sigma = [m.sigma_s_per_m for m in measurements]
    return SampleSummary(
        sample=samples.pop(),
        n=len(measurements),
        rs_mean_ohm_sq=statistics.fmean(rs),
        rs_sd_ohm_sq=standard_deviation(rs),
        rho_mean_ohm_m=statistics.fmean(rho),
        rho_sd_ohm_m=standard_deviation(rho),
        sigma_mean_s_per_m=statistics.fmean(sigma),
        sigma_sd_s_per_m=standard_deviation(sigma),
    )
