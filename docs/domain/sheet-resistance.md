# Sheet resistance, resistivity, conductivity

| Quantity | Symbol | Unit (as in the files, and as reported) | Relation (instrument side) |
|---|---|---|---|
| Sheet resistance | Rs | Ohm/square (Ω/sq) | Rs = 4.50797 · V/I |
| Resistivity | ρ | Ohm.m (Ω·m) | ρ = Rs · t, with t = 7 nm assumed by the instrument |
| Conductivity | σ | S/m | σ = 1/ρ |

- The tool does **not** recompute ρ or σ. It averages the values the instrument wrote
  ([[../adr/ADR-0002-statistical-definitions]]).
- Averaging and inverting don't commute: mean(σ_k) ≠ 1/mean(ρ_k). The tool reports mean(σ_k), which is intended.
- The tool's SD is the sample SD (divide by n − 1, [[../adr/ADR-0003-sample-standard-deviation]]). With n = 4 it is
  √(4/3) ≈ 1.155 × the population SD. The instrument's within-file SDs use the population SD.
- For reference: 1 Ω·m = 100 Ω·cm and 1 S/m = 0.01 S/cm. No conversion happens in the tool.

Related: [[../components/stats]]
