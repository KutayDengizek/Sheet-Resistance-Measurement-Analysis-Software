# Component: stats (`src/sheetres/stats.py`)
Status: **blocked** on [[../adr/ADR-0002-statistical-definitions]] (Proposed)

**Purpose.** Pure functions (no I/O) that turn `list[Measurement]` plus thickness into a
`SampleSummary` with the six quantities: mean and SD of Rs (Ω/sq), ρ (Ω·cm) and σ (S/cm).

**Proposed interface.** `summarize(measurements, thickness_cm: float) -> SampleSummary`

**Invariants.** Implement the estimators exactly as the Accepted ADR-0002 says. Pass `ddof`
explicitly. Tests use values computed by hand, not values copied from the implementation.

Related: [[../domain/sheet-resistance]], [[parser]], [[cli]]
