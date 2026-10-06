# RPE-005 — Finite prewarm capacity scheduling

## Question

RPE-004 assumes that every trusted wake signal can be acted on. RPE-005 removes that assumption:

> What if several meanings need to be prewarmed at once, but warm-up capacity is finite?

The experiment treats each prewarm candidate as a scheduling job with:

- signal release epoch;
- decision deadline;
- required warm-up duration;
- decision value.

One warm-up slot is available per epoch in these exact small worlds.

## Two counterexample portfolios

### Deadline trap

A salient long job is worth 9 but consumes both early slots. Two smaller urgent jobs plus one later job jointly yield 17.

- value-greedy / arrival-greedy choose the salient long job first and reach only 14;
- density-greedy happens to find 17;
- exact enumeration confirms 17 is optimal.

### Density trap

All jobs share a wide window, but the densest small item crowds out the globally better medium+large pair.

- density-greedy reaches 16;
- value-greedy reaches 22;
- exact enumeration confirms 22 is optimal.

The purpose of using two traps is to defeat the idea that replacing one heuristic with another solves the scheduling problem generically.

## Exact oracle

For each portfolio, every job subset is enumerated. A subset is feasible only if a backtracking scheduler can assign each job its required number of distinct warm-up epochs inside `[release, deadline)` without overlap.

This is intentionally small-world verification, not a scalable production scheduler.

## Core result

```text
value-greedy fails one world
value-density-greedy fails another world
arrival-order fails both
```

Therefore no tested greedy receives general authority from these fixtures.

The exact oracle remains the reference against which future bounded-DP, min-cost-flow, or approximation schedulers should be checked.

## Candidate rule

```text
SCARCE_PREWARM_CAPACITY
REQUIRES
DEADLINE_FEASIBLE_PORTFOLIO_SCHEDULING
AND
GREEDY_COUNTEREXAMPLE_TESTS
```

This is the Research Portfolio Ecology analogue of E018's audit-budget lesson, but with temporal feasibility: value is not enough, cost is not enough, and arrival order is not enough when decision deadlines share a finite warm-up surface.

## Next falsifiers

Useful RPE-006 directions:

- scale from exact enumeration to bounded dynamic programming or flow;
- heterogeneous per-epoch capacity;
- jobs that become stale while waiting;
- mandatory safety/verification meanings;
- correlated signal bursts;
- uncertain job duration;
- cancellation and rescheduling after re-observation.

## Claim ceiling

`EXACT_SMALL_SYNTHETIC_SCHEDULING_WORLDS_ONLY_NO_REAL_WARMUP_THROUGHPUT_CLAIM`
