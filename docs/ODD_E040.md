# ODD addendum — E040 rolling KPI current-state non-identifiability

## Purpose

Push E039 beyond lag.

A rolling metric can be delayed, but a harder problem is that one reported rolling value may not uniquely determine the current latent state at all.

## Exact finite ambiguity proof

Use a six-month trailing window with integer monthly MRR in the range 0 through 10.

Restrict the latent paths to monotone non-increasing sequences, which is already favorable to the interpretation of a declining service.

Require average MRR = 5:

```text
sum(six monthly MRR values) = 30
reported ARR = 5 × 12 = 60
```

Exact enumeration yields **338 distinct monotone paths** with the same reported ARR.

The current, sixth-month MRR can be any integer from **0 through 5**.

Examples include paths ending at zero and paths ending at five, all producing the identical ARR value 60.

Therefore:

```text
reported rolling ARR
does not uniquely identify
current MRR
```

even after imposing a monotone-decline structural assumption.

## Consequence

An early-warning system has three honest choices:

1. observe additional path/boundary state;
2. maintain a set or probability distribution over compatible latent states;
3. add stronger structural assumptions and expose them explicitly.

Silently treating trailing ARR as current MRR is not admissible.

## Promotion rule

`rolling-kpi-current-state-nonidentifiable-without-path-state-v1`

## Limitation

The integer lattice is a finite proof witness. Real MRR is continuous and may be non-monotone, which generally increases rather than removes the ambiguity.
