import math
from pathlib import Path

import pytest

from sheetres.parser import load_sample
from sheetres.stats import summarize

# Per-file means copied by hand from the last line of each tests/fixtures/260902_U1 file (k = 1..4).
RS = [437.39957709029943, 435.0582255646393, 433.8324346299779, 433.3297324777792]
RHO = [3.0617970396320962e-06, 3.0454075789524744e-06, 3.036827042409846e-06, 3.033308127344454e-06]
SIGMA = [326605.60239959665, 328363.3178086603, 329291.0695125812, 329673.07934461074]


def mean(xs: list[float]) -> float:
    return (xs[0] + xs[1] + xs[2] + xs[3]) / 4


def population_sd(xs: list[float]) -> float:
    """ADR-0002: sqrt( (1/n) * sum (x_k - mean)^2 ), n = 4."""
    m = mean(xs)
    return math.sqrt(
        ((xs[0] - m) ** 2 + (xs[1] - m) ** 2 + (xs[2] - m) ** 2 + (xs[3] - m) ** 2) / 4
    )


def test_u1_summary_matches_hand_calculation(u1_folder: Path) -> None:
    s = summarize(load_sample(u1_folder))
    assert s.sample == "260902_U1"
    assert s.n == 4
    assert s.rs_mean_ohm_sq == pytest.approx(mean(RS), rel=1e-12)
    assert s.rs_sd_ohm_sq == pytest.approx(population_sd(RS), rel=1e-9)
    assert s.rho_mean_ohm_m == pytest.approx(mean(RHO), rel=1e-12)
    assert s.rho_sd_ohm_m == pytest.approx(population_sd(RHO), rel=1e-9)
    assert s.sigma_mean_s_per_m == pytest.approx(mean(SIGMA), rel=1e-12)
    assert s.sigma_sd_s_per_m == pytest.approx(population_sd(SIGMA), rel=1e-9)


def test_u1_known_magnitudes(u1_folder: Path) -> None:
    """Coarse independent check (worked out on paper) that catches unit or column mix-ups."""
    s = summarize(load_sample(u1_folder))
    assert s.rs_mean_ohm_sq == pytest.approx(434.905, abs=1e-3)
    # deviations 2.4946, 0.1532, -1.0726, -1.5753 -> sum of squares 9.8783
    # population: sqrt(9.8783 / 4) = 1.5715; sample (ddof=1) would be sqrt(9.8783 / 3) = 1.8146
    assert s.rs_sd_ohm_sq == pytest.approx(1.5715, abs=1e-3)


def test_uses_population_not_sample_sd() -> None:
    from sheetres.parser import Measurement

    ms = [
        Measurement("S", k, Path(f"S_{k}.csv"), rs, 0.0, rs * 1e-8, 0.0, 1 / (rs * 1e-8), 0.0)
        for k, rs in enumerate([1.0, 2.0, 3.0, 4.0], start=1)
    ]
    s = summarize(ms)
    # mean 2.5; deviations -1.5 -0.5 0.5 1.5; sum of squares 5; population variance 5/4
    assert s.rs_mean_ohm_sq == 2.5
    assert s.rs_sd_ohm_sq == pytest.approx(math.sqrt(5 / 4))


def test_empty_input_is_an_error() -> None:
    with pytest.raises(ValueError, match="no measurements"):
        summarize([])


def test_mixed_samples_are_an_error(u1_folder: Path) -> None:
    from dataclasses import replace

    ms = load_sample(u1_folder)
    ms[2] = replace(ms[2], sample="OTHER")
    with pytest.raises(ValueError, match="more than one sample"):
        summarize(ms)
