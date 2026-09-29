# ADR-0002: Statistical definitions for the six reported quantities
Status: Accepted
Date: 2026-09-29 (decided by the user the same day)

## Context
Each sample has n = 4 measurement files, k = 1..4. The summary row of each file already holds the
per-file mean and standard deviation of sheet resistance (Ω/sq), resistivity (Ω·m) and conductivity
(S/m). The instrument computes resistivity and conductivity itself, using its own thickness.
The tool reports the mean and SD of each of the three quantities over the four files.

## Decision
For each quantity X in {sheet resistance, resistivity, conductivity}, with X_k = the per-file
"Mean …" value from file k:
- **Mean** = (1/n) · Σ X_k
- **SD** = **population** standard deviation of the four X_k: √( (1/n) · Σ (X_k − mean)² ), i.e. ddof = 0
  (Excel `STDEV.P`). This is not the standard error of the mean.
- The per-file "Standard Deviation" columns are **not used** in the result.
- Resistivity and conductivity are **taken from the files**, not recomputed. No thickness input.
- Results are reported in the **same units as the files**: Ohm/square, Ohm.m, S/m.

## Alternatives considered
- Sample SD (ddof = 1) — rejected by the user.
- Standard error SD/√n — rejected.
- Pooling within-file SDs — rejected: only the scatter between the four measurements counts.
- Recomputing ρ = Rs·t and σ = 1/ρ from a thickness — unnecessary, since the instrument already
  provides both, and it would introduce a second, possibly inconsistent thickness.
- Converting to Ω·cm and S/cm — rejected. Keeping the file units avoids a conversion step.

## Consequences
`stats` uses `statistics.pstdev`, via a named constant. Mean conductivity is therefore the mean
of the per-file conductivities, which is *not* 1/(mean resistivity). That is intended. Changing
any of this requires a superseding ADR plus golden regeneration with approval.
