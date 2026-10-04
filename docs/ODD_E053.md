# ODD addendum — E053 noisy lineage-probe robustness

## Purpose

Attack E052's minimum-cost probe portfolio.

The E052 portfolio `ab, ac, bc` perfectly distinguishes the five reference lineage hypotheses when every probe observation is correct.

E053 asks what happens after one probe error.

## Counterexample

E052 signatures include:

```text
none       = 000
shared-bcd = 001
```

A single flipped `bc` observation turns the true `none` signature into the exact `shared-bcd` signature.

The E052 portfolio has minimum pairwise Hamming distance 1.

No decoder can distinguish those two cases after that error.

## Error-correcting requirement

To correct one arbitrary binary probe error, hypothesis signatures need minimum Hamming distance at least 3.

E053 exactly enumerates every subset of the six pair probes.

In this reference world, only the full six-probe portfolio reaches distance 3:

```text
ab, ac, ad, bc, bd, cd
probe count = 6
total declared cost = 12
minimum Hamming distance = 3
```

## Exhaustive decode

There are five hypotheses.

For each hypothesis, E053 tests:

- the no-error signature;
- each of six possible single-bit flips.

That creates 35 exhaustive decode cases.

Nearest-signature decoding identifies the correct hypothesis in all 35.

## Consequence

There are now two different optimization targets:

```text
minimum-cost noiseless identification
!=
minimum-cost one-error-correcting identification
```

Robustness authority requires an explicit signature-distance certificate.

## Promotion rule

`lineage-probe-error-tolerance-requires-distance-three-signatures-v1`

## Limitation

Real probe noise can be correlated, asymmetric, or continuous. Hamming distance is the exact finite reference mechanism, not a universal noise model.
