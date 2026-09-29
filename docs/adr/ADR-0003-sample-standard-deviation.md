# ADR-0003: Sample standard deviation (divide by n − 1)
Status: Accepted
Date: 2026-09-29 (instructed by the user: "divide by n-1 for all standard deviation calculations")

## Context
[[ADR-0002-statistical-definitions]] chose the population SD (divide by n). The user reversed that
choice. For reference, the instrument's own within-file SDs use the population SD (verified from the
raw rows, see [[../domain/input-format]]).

## Decision
Every standard deviation **computed by this tool** is the sample SD:
SD = √( (1/(n−1)) · Σ (X_k − mean)² ), i.e. Excel `STDEV.S` / `statistics.stdev`.
It applies to the SD of mean sheet resistance, mean resistivity and mean conductivity over the
n = 4 files. At least 2 measurements are required; fewer raises an error.

Everything else in ADR-0002 still holds: plain mean; within-file SDs unused; ρ and σ read from the
files; units as in the files.

## Alternatives considered
- Keep the population SD (ADR-0002), which matches the instrument's convention. Rejected by the user.
- Also recompute the within-file SDs with n − 1 from the raw rows. Not needed, because they don't
  enter any reported result. Revisit if they ever do.

## Consequences
Reported SDs grow by a factor of √(4/3) ≈ 1.1547 compared with ADR-0002. For 260902_U1, the Rs SD
goes from 1.5715 to 1.8146 Ohm/square. The tool's SD now deliberately differs from the instrument's
within-file convention. `test_instrument_within_file_sd_is_population` documents that difference.
