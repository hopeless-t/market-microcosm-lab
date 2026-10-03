# ODD addendum — E018 audit portfolio scheduling

## Purpose

Allocate a limited authoritative-audit budget across multiple optimized evaluator certificates without allowing a locally appealing priority heuristic to become self-certifying.

## Entities

AuditItem:

- name;
- integer audit cost units;
- integer restoration value;
- mandatory audit flag.

## Objective

Choose a subset within the declared budget that maximizes total restoration value.

Tie-breaking is deterministic:

1. higher restoration value;
2. lower total audit cost;
3. lexicographically smaller selected-name tuple.

Mandatory items must be included. If mandatory cost alone exceeds budget, the portfolio is infeasible and the scheduler fails closed.

## Reference algorithm

The oracle enumerates all subsets.

For eight items this requires 256 subset evaluations per generated portfolio.

## Candidate algorithm

bounded-dp preselects mandatory items and solves the remaining budgeted selection through dynamic programming indexed by consumed budget.

## Evaluation suite

- deterministic RNG seed: 18017;
- 48 generated portfolios;
- 8 certificates per generated portfolio;
- 0–2 mandatory audits per portfolio;
- audit cost units: 1–6;
- restoration values: 10–150.

Separate fixed cases test:

- a value-per-cost greedy trap;
- mandatory audit cost greater than total budget.

## Promotion gate

Promotion requires:

- 100% exact match to the exhaustive oracle on generated portfolios;
- at least 50% reduction in search-work units;
- at least one explicit greedy failure;
- fail-closed behavior for infeasible mandatory portfolios.

## Interpretation

Restoration value is a synthetic scheduler objective, not a real-world monetary or safety valuation. The experiment validates scheduling machinery, not a particular external audit policy.
