# ODD addendum — E039 rolling KPI observation lag

## Purpose

Separate latent business state from the measurement kernel used to observe it.

Informetis defines ARR as twelve times the average MRR over the six months immediately preceding quarter end.

That means ARR is not an instantaneous state variable.

## Event context

The company reports that a major rental-business service ended in March 2026.

A June quarter-end ARR therefore uses a six-month window containing January through June.

Even if an affected customer-level MRR became zero immediately after March, the June trailing window would still contain three pre-end months.

## Exact impulse response

E039 uses a simple structural reference:

```text
pre-shock MRR = 10
post-shock MRR = 0
window = 6 months
```

The instantaneous underlying recurring-revenue equivalent falls:

```text
120 → 0
```

But the trailing reported ARR responds gradually:

```text
month 0: 120
month 1: 100
month 2:  80
month 3:  60
month 4:  40
month 5:  20
month 6:   0
```

Three months after a complete end, half of the legacy signal remains in the metric.

## Consequence for early warning

Warning lead time cannot be evaluated from publication timestamps alone.

The evidence plane must distinguish:

```text
latent business state
→ measurement window
→ metric value
→ publication cadence
→ warning observation
```

A smoothed KPI can produce apparent delayed deterioration or apparent delayed recovery even when the underlying state changed abruptly.

## Promotion rule

`rolling-window-metric-lag-must-be-modeled-v1`

## Limitation

The 10→0 MRR impulse is synthetic. It describes the exact response of the published metric definition, not Informetis's customer-level MRR or aggregate company ARR.
