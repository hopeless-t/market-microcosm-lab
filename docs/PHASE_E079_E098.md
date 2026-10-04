# Phase synthesis — E079 to E098

This document is the compact canonical surface for the observation-process / SaaS-exit phase that follows E078.

## North-star contribution

The phase asks a harder version of the original market-viability question:

> What should a market/governance model do when business state changes not only the KPI values, but also what gets reported, what remains observable, which governance checkpoint is active, and whether an exit is a long runoff rather than an instantaneous zero?

The answer is a typed, time-scoped, fail-closed evidence path.

## E079–E088 — endogenous observation process

- **E079 Informative KPI withdrawal** — deterioration-linked KPI withdrawal is retained as an event; hidden values are not imputed.
- **E080 Reporting kernel generations** — reporting-policy change creates a new observation operator; cross-kernel estimators ABSTAIN without a bridge.
- **E081 Disclosure-selection bias** — complete-case filtering can erase deterioration-linked withdrawals from the empirical population.
- **E082 Withdrawal reason typing** — `withdrawn=true` is not a universal failure signal; reason type and source authority are mandatory.
- **E083 Censored evaluation** — 100% observed-label accuracy with 80% label coverage has only partial-evaluation authority.
- **E084 Censored performance intervals** — 8 observed-correct out of 10 total yields an exact full-population accuracy interval [0.80, 1.00]; coarse predicates may pass while finer ones ABSTAIN.
- **E085 Real longitudinal holdout** — Allied's 2024-02-14 withdrawal event precedes a same-lineage 2024-10-31 dissolution/winding-up decision by 260 days; chronology validates event retention, not causality.
- **E086 Governance-action guard** — deterioration-linked withdrawal escalates review; it does not itself authorize exit.
- **E087 Governance checkpoint path** — public sequence is reporting break → explicit exit criteria → confirmed exit.
- **E088 Evidence-time guard** — Q1-effective governance criteria disclosed only on 2024-08-14 are unavailable to a public evaluator before that date.

## E089–E095 — checkpointed exit and post-exit state

- **E089 Predicate-scoped checkpoint authority** — each governance claim uses the minimum indispensable public checkpoint set.
- **E090 Post-exit sign reversal** — Allied revenue falls while operating profit swings from -229m to +16m JPY; revenue scale and operating viability stay separate.
- **E091 Replacement KPI bridge guard** — retrospective backfill authorizes continuity inside the new metric definition, not across a different old construct.
- **E092 Horizon guard** — Q1 operating black does not certify durable profitability when H1 remains loss-making despite major improvement.
- **E093 Jooto traction/viability counterexample** — 2,379 paid contracts and 387m JPY revenue coexist with persistent losses and failure to establish sustainable competitive advantage across five growth axes.
- **E094 Exit runoff state machine** — Jooto exit decision begins a 360-day runoff/migration period; existing-customer and transition obligations remain active.
- **E095 Residual capability value** — standalone growth-business exit does not imply zero value for customer knowledge, technology, adjacent implementations, or employee capability.

## E096–E098 — mechanism taxonomy and recovery control

- **E096 Typed Japanese SaaS negative-evidence taxonomy** — BBD, Allied, and Jooto are distinct mechanism vectors rather than one `FAILED_SAAS` bit.
- **E097 Real recovery negative control** — GVA TECH Q3 ARR↓/churn↑ recovers in Q4, proving one-quarter bad signs are not structural-failure authority.
- **E098 Real-case warning tournament** — a scalar ARR/churn sign rule false-positives on GVA and misses Allied/Jooto; a typed mechanism rule is exact on the four-case semantic regression suite. This is not production predictive accuracy.

## Cross-phase invariants

1. Hidden KPI values are never filled in merely because disclosure stops.
2. Reporting policy is part of the observation model.
3. Effective period, publication time, and metric generation are separate evidence identities.
4. A warning event does not automatically inherit exit authority.
5. Strategic exit has runoff obligations and can preserve residual capability value.
6. Negative-evidence research must include real recovery controls to limit false positives.
7. Exact fit on a hand-typed public-case suite is a semantic regression test, not a production accuracy claim.

## Empirical anchors

This phase is grounded primarily in public materials from:

- BBD Initiative — real portfolio-transition KPI sign reversals;
- Allied Architects — churn/ARR sign conflict, deterioration-linked KPI withdrawal, governance criteria, overseas exit, post-exit operating results, and replacement KPI generation;
- PR TIMES / Jooto — business abolition with nonzero traction, 360-day runoff, and retained capability value;
- GVA TECH — one-quarter ARR/churn deterioration followed by recovery, used as a negative control.

## Validation surface

`python scripts/run_e079_e098_bundle.py`

runs all twenty report payloads and asserts that every promotion gate remains live through the phase integration test.
