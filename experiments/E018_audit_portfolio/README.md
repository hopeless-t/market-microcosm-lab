# E018 — Risk-weighted audit portfolio scheduler

E017 schedules one certificate over time. E018 asks what happens when many optimized evaluators compete for a limited authoritative-audit budget.

## Small-world oracle

Each audit candidate has:

- audit cost units;
- restoration value, representing model-relative value from restoring certified optimized authority;
- an optional mandatory flag for cases such as generation drift, expiry, or revocation.

The scheduler receives a fixed audit budget and must choose the best feasible subset.

An exhaustive subset enumerator is the oracle.

## Candidate scheduler

bounded-dp solves the same 0/1 audit-budget problem with dynamic programming.

Promotion requires exact agreement with the exhaustive oracle across a deterministic suite of 48 generated 8-certificate portfolios.

## Why not greedy?

A value-per-cost greedy scheduler is intentionally tested against the classic trap:

- A: cost 10, value 60
- B: cost 20, value 100
- C: cost 30, value 120
- budget: 50

Greedy selects A+B for value 160.

The exact optimum is B+C for value 220.

This prevents a plausible but locally attractive audit policy from being promoted without an exact countercheck.

## Fail-closed mandatory case

A separate portfolio makes mandatory authoritative audits cost more than the available budget.

All schedulers must report the portfolio infeasible and fail closed rather than silently choosing a partial mandatory set.

## Promotion

bounded-dp is promoted only if it:

1. matches the exhaustive oracle on every generated portfolio;
2. reduces search work by at least 50%;
3. coexists with a demonstrated greedy counterexample;
4. fails closed when mandatory audit cost exceeds budget.
