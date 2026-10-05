# ODD addendum — E045 predicate-scoped active sensing

## Purpose

Complete the E043–E044 control loop.

E043 says observability authority is predicate-scoped.

E044 says a boundary-straddling uncertainty set must ABSTAIN.

E045 asks what the system should observe next.

The answer should not default to "collect everything."

## Reference decision

```text
predicate: current MRR >= 2
prior uncertainty: [1.5, 2.5]
prior result: ABSTAIN
```

## Candidate observations

The reference search assigns synthetic information-cost weights.

Cheap local refinements of only one existing input cost 1 but leave the decision interval straddling the threshold.

An exact current-MRR query costs 5 and resolves the predicate.

A predicate-native ledger check — evidence directly sufficient to establish whether current MRR is at least 2 — costs 2 and also resolves the predicate.

Exact search therefore chooses the predicate-native observation.

## Principle

The observation objective is:

```text
minimize declared evidence cost
subject to
all compatible states agree on the requested predicate
```

not:

```text
maximize recovered state detail
```

This continues the minimal-checkpoint principle:

- collect no new evidence when the predicate is already certified;
- ABSTAIN when it is not;
- request the cheapest authorized observation that resolves the specific predicate;
- collect full latent state only when the decision actually requires it.

## Promotion rule

`request-cheapest-predicate-sufficient-observation-v1`

## Limitation

The candidate costs are synthetic policy weights. Real collection cost must include latency, privacy, operator burden, access authority, and measurement error.
