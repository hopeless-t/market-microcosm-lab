# ODD addendum — E084 censored performance intervals

## Purpose

E083 reports 100% observed-label accuracy with only 80% numeric-label coverage and therefore refuses full-evaluation authority.

E084 asks what can still be certified without inventing the two hidden labels.

## Exact finite-population bound

Eight of ten cases have numeric labels and all eight are correct.

Two labels are censored.

Worst case: both censored predictions are wrong.

`accuracy = 8 / 10 = 0.80`

Best case: both are correct.

`accuracy = 10 / 10 = 1.00`

Therefore the full-population accuracy is exactly bounded by:

`[0.80, 1.00]`

No censored label is imputed.

## Decision-scoped authority

For a required accuracy of 75%, the lower bound already exceeds the threshold, so E084 returns `CERTIFIED_PASS`.

For a required accuracy of 90%, the interval straddles the threshold, so E084 returns `ABSTAIN_CENSORED_LABELS`.

The same partial evidence can therefore certify a coarse performance predicate while remaining insufficient for a finer one.

Promotion:

`censored-evaluation-uses-full-population-performance-intervals-v1`
