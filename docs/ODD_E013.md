# ODD addendum — E013 one-dimensional pressure decomposition

E013 reuses the E010 entities and transition schedule.

## Purpose

Decompose the E011 composite stress signal into separate structural interventions so that the laboratory can identify which parameter family is sufficient to trigger each model-internal collapse mode.

## Experimental factors

Three independent axes are swept while all other E010 parameters remain at baseline:

1. subscription price multiplier;
2. platform operating-cost multiplier;
3. baseline user churn rate.

Each axis is deterministic conditional on axis level, mechanism, and seed bank.

## Evidence separation

- decomposition scan seeds: 13000–13019;
- failure-biopsy seeds: 14000–14039;
- horizon: 60 periods.

These seed banks do not overlap E010–E012 discovery/promotion/meta banks.

## Knee

The preliminary axis knee is the first tested level where observed full-horizon survival falls below 90%.

A missing knee means only that no threshold was observed inside the declared scan range.

## Failure biopsy

At each detected axis knee, or at the strongest tested point if no knee exists, the experiment stores the first failing trajectory and explicit viability-failure reasons.

## Limitation

One-factor-at-a-time sweeps reveal sufficiency and sensitivity inside the declared simulator, but do not measure interaction effects. Follow-up experiments should reintroduce two-dimensional interactions around localized knees.
