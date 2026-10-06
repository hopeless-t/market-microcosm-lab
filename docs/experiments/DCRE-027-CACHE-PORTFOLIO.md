# DCRE-027 — Finite near-cache portfolio: hotness is not resident value

## Trigger

DCRE-025–026 show that prepared compact representations are attractive only inside a joint reuse × stability region.

DCRE-027 adds one more scarce physical resource: **near-workload storage**.

The question is no longer whether one prepared object is worth keeping. It is which subset should remain resident when several objects compete for a finite cache budget.

## Reuse existing machinery

This experiment intentionally does **not** implement a new knapsack solver.

It projects cache candidates onto the already-qualified E018 portfolio scheduler:

```text
cache storage units        -> E018 audit_cost_units
expected network relief    -> E018 restoration_value
```

E018 already provides an exhaustive small-world oracle and a bounded-DP scheduler that is tested against greedy allocation traps.

## Frozen candidates

Storage budget:

```text
10 units
```

Candidates:

```text
HOT_BIG
  storage = 8
  requests = 10
  network relief / valid hit = 1
  invalidation probability = .40
  expected relief = 6

WARM_A
  storage = 5
  requests = 7
  relief / valid hit = 2
  invalidation = 0
  expected relief = 14

WARM_B
  storage = 5
  requests = 6
  relief / valid hit = 2
  invalidation = 0
  expected relief = 12
```

All values are synthetic.

## Frequency greedy

A request-count ranking chooses `HOT_BIG` first.

```text
selected = HOT_BIG
storage = 8 / 10
expected network relief = 6
```

The remaining two units cannot hold either WARM object.

## E018 exact / bounded-DP projection

The exact portfolio and E018 bounded DP both choose:

```text
WARM_A + WARM_B
storage = 10 / 10
expected network relief = 26
```

## Result

```text
request frequency
!= valid reuse
!= resident value
```

A hot object can be a poor resident when it is large, unstable, or saves little network resource per valid reuse.

This closes the locality/cache mini-chain with a stronger rule: **near-workload residency is a finite portfolio problem, not an LFU popularity ranking problem.**

The important meta-result is also architectural: the lab reused E018's already-qualified portfolio mechanism instead of creating another scheduler.

## Boundary

Expected relief is synthetic and assumes homogeneous invalidation probability and network value. There is no measured cache hit-rate, SSD cost, DRAM cost, egress price, latency benefit, or real workload trace.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_CACHE_PORTFOLIO_COUNTEREXAMPLE
```

## Chapter handoff

Do not recursively expand cache governance here.

DCRE-028 returns foreground attention to **physical time-varying resource ecology**: shift flexible workload across temporal energy/water headroom and test when load shifting helps versus when deadlines, rebound, or synchronized response create a new peak.
