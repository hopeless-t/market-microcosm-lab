# Root of Trust

This file defines the minimum constitution for one evaluation generation.

## R1 — Conservation
All money/resource creation and destruction must be explicit external source/sink events. Internal transfers conserve the ledger.

## R2 — Causality
State at time t+1 may depend only on allowed state/history, current action, declared stochastic input, and declared exogenous input.

## R3 — Oracle isolation
Deployable policy code may not consume oracle-only state or future information.

## R4 — Reproducibility
Every scored run has an immutable manifest containing code revision, model/policy/verifier versions, scenario, parameters and seed.

## R5 — Independent promotion
The candidate generator cannot directly mark itself promoted. Promotion is produced by a verifier from persisted evidence.

## R6 — Held-out isolation
Promotion scenarios/seeds are not available to candidate optimization.

## R7 — Constitutional versioning
Changing R1-R6 or the hard viability constraints creates a new evaluation generation. Incumbent and challengers are re-evaluated under the new generation.

These rules are intentionally small. The meta-loop may improve almost everything else.
