# E013 — Pressure decomposition

E011 intentionally used a composite stress axis:

- subscription price / revenue falls;
- platform operating cost rises;
- baseline user churn rises.

That located the first viability knees, but it did not tell us which component caused each collapse.

E013 performs one-factor-at-a-time interventions.

## Axes

### Subscription price multiplier

Only subscription price changes. Platform operating cost and churn remain at their neutral defaults.

### Platform cost multiplier

Only platform operating cost changes.

### Baseline churn rate

Only baseline churn changes.

Each axis uses the same level count and approximately the same step sizes that contributed to E011.

## Outputs

For every mechanism × axis × level:

- survival rate and Wilson lower confidence bound;
- ecosystem health;
- user utility and diversity;
- active developer/publisher counts;
- platform cash;
- survival duration;
- entry/exit counts.

The preliminary knee remains the first level with observed survival below 90%.

## Failure biopsy

For every mechanism and axis, E013 searches a distinct seed bank at the detected knee. If no knee occurs in the scan range, biopsy is attempted at the strongest tested level.

This reveals whether a single pressure axis is sufficient to reproduce the composite E011 failure mode.

## Interpretation

This is an explicit intervention inside the synthetic world. It identifies model-internal causal sensitivity, not a real-world causal effect.
