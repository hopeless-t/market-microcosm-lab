# ODD addendum — E056 measurement-channel failure domains

## Purpose

Attack E055's independent-channel assumption.

E055 synthesizes a ten-channel distance-five probe code and proves correction of every two arbitrary bit errors.

That certificate is meaningful only if the measurement topology makes the bit-error model plausible.

## Common-mode counterexample

The E055 code contains five channels whose TRUE pattern distinguishes `shared-abc` from `none`:

```text
ab × 1
ac × 2
bc × 2
```

If all five channels share one `shared-collector` failure root, one root fault flips all five bits.

Starting from the true `none` codeword, that one common-mode fault creates the exact `shared-abc` codeword.

Nearest-codeword decoding confidently returns the wrong hypothesis.

The distance-five certificate did not fail mathematically.

Its assumed error unit was wrong.

## Root-diverse repair

The declared bit budget is two arbitrary flipped channels.

Therefore one measurement-root failure must corrupt at most two certified channels.

With ten channels, a simple counting lower bound requires at least:

```text
ceil(10 / 2) = 5 independent measurement roots
```

The repaired reference places at most two channels under each of five roots.

Every one-root failure is then an error pattern of size at most two, already covered by E055's certificate.

Five hypotheses × five possible root faults gives 25 exact cases, all decoded correctly.

## Consequence

```text
repetition count
!=
independent redundancy
```

Robust probe authority requires both:

- code-distance certificate;
- measurement failure-domain certificate.

## Promotion rule

`redundant-probe-channels-must-diversify-measurement-failure-roots-v1`

## Limitation

The reference handles one declared measurement-root fault. Multiple simultaneous roots or hidden shared infrastructure require a stronger threat compile.
