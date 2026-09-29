# ADR-0002: Statistical definitions for the six reported quantities
Status: Proposed
Date: 2026-09-29

## Context
For each sample we have n = 4 measurements, k = 1..4. Each file reports a mean sheet resistance
Rs_k (Ω/sq) and its own within-measurement standard deviation. The tool must report the mean and
SD of Rs, ρ and σ. Several reasonable definitions give different numbers, so the human must
choose them. Agents must not improvise.

## Open questions (human to answer)
- **Q1 — What does "standard deviation of mean X" mean?**
  (a) sample SD of the four per-file means, ddof = 1 *(proposed)*;
  (b) population SD, ddof = 0;
  (c) standard error of the mean = sample SD / √4.
- **Q2 — Do the per-file SDs from the CSVs enter the result?**
  (a) no, only the scatter of the four means *(proposed)*;
  (b) pooled SD combining within-file and between-file variance.
- **Q3 — How are ρ and σ derived?**
  (a) per measurement: ρ_k = Rs_k·t and σ_k = 1/ρ_k, then mean and SD over k *(proposed; the
  "mean conductivity" then really is the mean of the conductivities)*;
  (b) from the aggregate: ρ̄ = R̄s·t, σ = 1/ρ̄, SDs via first-order error propagation.
- **Q4 — Where does the film thickness t come from, and in what unit?** It may be in the CSV, a CLI
  argument, or a per-sample config file. Is there an uncertainty on t that should propagate?

## Decision
*Pending the human's answers.* The proposed defaults are Q1(a), Q2(a), Q3(a). Q4 is open.

## Consequences
Once Accepted, `stats` implements exactly this and the golden outputs are generated from it. Any
later change requires a superseding ADR plus a golden regeneration with approval.
