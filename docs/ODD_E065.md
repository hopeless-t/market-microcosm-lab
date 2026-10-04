# ODD addendum — E065 public-warning feature sufficiency

## Purpose

E064 prevents future leakage.

E065 asks the next prospective question: does the public Q3 evidence actually contain the state required by the structural early-warning model?

## Warning feature contract

The E035/E036-style warning vector requires:

- cash collection gap;
- fully-loaded delivery margin;
- market headroom;
- downstream funnel success;
- strategic-exit value gap.

## Public FY2025 Q3 evidence

The public BBD KPI material provides:

- ARR = 1,688 million JPY;
- churn = 2.16%;
- contract count = 3,304;
- ARPA = 511,090 JPY.

Those are valid admitted observations.

They are not direct measurements of any of the five structural warning axes.

## Forbidden shortcut

The evaluator may not silently infer:

```text
ARR -> cash timing
ARPA -> fully-loaded margin
contracts -> market headroom
churn -> downstream customer success
growth -> strategic exit value
```

because those mappings are exactly the proxy collapses attacked by E030–E034.

## Prospective result

Feature coverage:

```text
0 / 5
```

The correct public-data decision is:

`ABSTAIN — INSUFFICIENT_PUBLIC_EVIDENCE`

No imputation is authorized.

## Consequence

A model can be structurally better than the public dataset available to evaluate it.

That is not permission to weaken the feature contract.

It is an evidence-acquisition problem.

## Promotion rule

`structural-warning-must-abstain-when-public-feature-contract-is-incomplete-v1`

## Limitation

E065 concerns the public IR dataset. Internal company systems may contain the missing structural state under a different access and authority scope.
