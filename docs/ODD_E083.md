# ODD addendum — E083 coverage-aware censored evaluation

## Purpose

E081 shows that informative KPI withdrawal can bias benchmark membership.

E083 applies the same attack to model evaluation.

## Finite reference

Ten forecast cases are evaluated.

Eight stable cases retain numeric labels and are predicted correctly.

Two cases later undergo informative KPI withdrawal. Their numeric labels are unavailable.

A complete-case scorer reports:

`accuracy = 100%`

but silently scores only 8/10 cases.

The coverage-aware scorer reports:

- observed-label accuracy: 100%;
- numeric label coverage: 80%;
- informative withdrawal cases: 2;
- authority: `PARTIAL_EVALUATION_ONLY`.

The two censored cases are neither counted as correct nor counted as errors, because their hidden numeric labels are not identified.

## Consequence

Observed-label accuracy is not full-evaluation authority when the observation process is state-dependent.

Promotion:

`informatively-censored-evaluation-must-report-coverage-and-partial-authority-v1`

## Limitation

E083 demonstrates evaluation authority and coverage semantics; it does not solve statistical correction for the hidden outcomes.
