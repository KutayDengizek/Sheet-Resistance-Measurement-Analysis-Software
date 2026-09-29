# Sheet resistance, resistivity, conductivity

| Quantity | Symbol | Unit (reported) | Relation |
|---|---|---|---|
| Sheet resistance | Rs | Ω/sq | measured (four-point probe; the instrument applies geometric correction) |
| Film thickness | t | cm (confirm the source unit, e.g. nm → ×1e-7) | input, see [[input-format]] |
| Resistivity | ρ | Ω·cm | ρ = Rs · t |
| Conductivity | σ | S/cm | σ = 1/ρ |

- Conversion constants are named in code, e.g. `NM_PER_CM = 1e7`. Never inline them.
- Averaging and inverting don't commute, so the order of operations matters. See the Q3 options
  in [[../adr/ADR-0002-statistical-definitions]].
- With n = 4 the SD estimator matters: ddof = 1 vs 0 changes the SD by a factor √(4/3) ≈ 1.155.

Related: [[../components/stats]]
