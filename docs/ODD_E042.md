# ODD addendum — E042 reporting-resolution self-attack

## Purpose

Attack E038's apparently impressive 0.34% point-error result.

The Informetis service-component ARR chart used by E038 displays values in integer million JPY.

A model must not claim empirical precision finer than the source representation supports.

## Naive E038 point result

Using displayed values:

```text
Q1 = 266
Q3 = 231

retention = sqrt(231 / 266)
Q4 prediction ≈ 215.27
displayed Q4 = 216
absolute point error ≈ 0.73 million JPY
relative point error ≈ 0.34%
```

But 0.73 million JPY is smaller than one displayed million-JPY unit.

## Rounding-aware interval

Assume conventional nearest-million display rounding:

```text
266 represents approximately [265.5, 266.5)
231 represents approximately [230.5, 231.5)
216 represents approximately [215.5, 216.5)
```

Propagating the Q1/Q3 intervals through the same decay formula gives a prediction interval of approximately:

```text
[214.37, 216.17]
```

This overlaps the Q4 displayed-value interval.

The admissible conclusion is therefore:

```text
decay model is interval-consistent with the rounded holdout
```

not:

```text
decay model has demonstrated 0.34% real-world accuracy
```

## Authority change

E042 explicitly marks the E038 sub-1% precision interpretation:

`REVOKED`

The broader E038 component/event holdout remains useful, but only at a precision supported by the source.

## Promotion rule

`empirical-claim-precision-cannot-exceed-reporting-resolution-v1`

## Consequence

Every empirical scalar now needs another identity field:

```text
value
+ definition
+ time
+ source authority
+ component
+ reporting resolution / quantization
```

Uncertainty introduced by reporting resolution must be propagated through model comparison and holdout evaluation.

## Limitation

The interval assumes ordinary nearest-million rounding of the displayed chart. More precise underlying figures could narrow the uncertainty if they become publicly available.
