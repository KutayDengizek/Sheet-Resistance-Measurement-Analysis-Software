# Component: stats (`src/sheetres/stats.py`)
Status: **implemented** 2026-09-29 per [[../adr/ADR-0002-statistical-definitions]] (Accepted)

**Purpose.** Pure function (no I/O): `summarize(measurements) -> SampleSummary` with
`rs_mean_ohm_sq, rs_sd_ohm_sq, rho_mean_ohm_m, rho_sd_ohm_m, sigma_mean_s_per_m, sigma_sd_s_per_m`
plus `sample` and `n`.

**Estimators.** `statistics.fmean` and `statistics.pstdev` (population SD, ddof = 0) of the per-file
means. The SD function is the module constant `standard_deviation`. Changing it requires a new ADR.

**Tests.** `tests/test_stats.py` recomputes the expected values with the formula written out,
from values copied by hand from the fixture. It also has a paper-calculated magnitude check,
and a check with values 1..4 that separates ddof 0 from ddof 1.

Related: [[../domain/sheet-resistance]], [[parser]], [[cli]]
