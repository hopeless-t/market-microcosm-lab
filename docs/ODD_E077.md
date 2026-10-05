# ODD addendum — E077 calibration Pareto frontier

E076 solves one certificate target: robust acquisition cost <= 11.3.

E077 removes that single-target dependency.

Every calibration subset is already available from E076. E077 discards dominated choices and keeps the exact cost-vs-certified-bound Pareto frontier:

```text
calibration cost 0 -> robust bound 12.00 -> no calibration
calibration cost 1 -> robust bound 11.85 -> strategy incidence study
calibration cost 2 -> robust bound 11.20 -> GTM incidence study
```

All other calibration portfolios are dominated in the current reference.

A target compiler then selects the cheapest sufficient frontier point:

```text
target <= 12.0 -> cost 0
target <= 11.9 -> strategy, cost 1
target <= 11.3 -> GTM, cost 2
target <= 11.1 -> UNSAT
```

The last case matters: the system does not invent more certainty than the admitted calibration catalog can buy.

Promotion: `certificate-calibration-uses-pareto-frontier-and-fail-closed-target-compiler-v1`.
