# ODD addendum — E081 disclosure-selection bias

## Purpose

E079 shows that deterioration can change whether a KPI is disclosed at all.

E081 attacks the next pipeline stage: benchmark construction.

If a benchmark keeps only rows with numeric KPI values, deterioration-linked withdrawals can disappear from the benchmark population.

## Finite reference

Ten records are constructed:

- eight healthy records continue KPI disclosure;
- two deterioration records withdraw the KPI and retain no numeric hidden value.

The true deterioration-event rate is 20%.

A complete-case benchmark selects only the eight disclosed rows and observes a deterioration-event rate of 0%.

The event-aware benchmark keeps all ten records, retains the two withdrawal events, and recovers the 20% event rate while still refusing to impute the hidden KPI values.

## Separation

Two populations are distinct:

1. the **empirical event population**, which may include disclosure-withdrawal events;
2. the **numeric KPI estimator sample**, which can use only admitted numeric observations.

A record does not have to vanish from the empirical population merely because its KPI value is unavailable.

## Promotion rule

`benchmark-selection-must-retain-informative-kpi-withdrawal-events-v1`

## Limitation

The finite 10-record world demonstrates the bias mechanism only. It does not estimate the prevalence or magnitude of this bias across Japanese SaaS companies.
