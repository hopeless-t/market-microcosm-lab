# ODD addendum — E086 governance action after KPI withdrawal

## Purpose

E085 observes that an Allied deterioration-linked KPI withdrawal was followed 260 days later by a real corporate exit decision in the same business lineage.

E086 prevents hindsight from turning that chronology into an unsound deterministic policy.

## Action semantics

`KPI_WITHDRAWN + DUE_TO_DETERIORATION`

→ `ESCALATE_REVIEW`

`KPI_WITHDRAWN + DUE_TO_METRIC_REDESIGN`

→ `KERNEL_CHANGE_ONLY`

`KPI_WITHDRAWN + unknown reason`

→ `ABSTAIN_REASON_UNKNOWN`

`SUBSIDIARY_DISSOLUTION_AND_LIQUIDATION_DECISION`

→ `EXIT_CONFIRMED`

A withdrawal event alone never emits `EXIT_CONFIRMED`.

## Consequence

The reporting event can increase governance attention without receiving authority it did not earn.

E085 remains a longitudinal retention validation, not a deterministic liquidation predictor.

Promotion:

`deterioration-linked-kpi-withdrawal-triggers-review-not-deterministic-exit-v1`
