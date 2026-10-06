# DCRE-012 — Capacity race after unit-efficiency gains

## Chapter return

DCRE-001–011 follow the information/allocation chain far enough to expose rebound, verification scarcity, exploration, correlated evidence, audit value, waiting congestion, price exclusion, and protected-label Goodhart.

DCRE-012 deliberately returns foreground attention to the original physical-resource question: **what happens when efficiency savings are reinvested into capacity?**

## Frozen world

```text
baseline demand       = 100 tasks
baseline capacity     = 100 tasks
efficiency ratio e    = 0.60
demand elasticity eta = 1.50
resource ceiling      = 100 synthetic resource units
verification capacity = 120 tasks
```

Induced demand is:

```text
D = 100 * (1/0.6)^1.5
  ~= 215.166 tasks
```

## Arm A — no reinvestment

Capacity stays at 100 tasks.

```text
served = 100
resource = .6 * 100 = 60
verified = 100
```

The unit-efficiency gain appears as a 40-unit resource saving.

## Arm B — reinvest savings up to the old resource ceiling

If capacity expands until the old resource ceiling is filled:

```text
capacity = 100 / .6
         ~= 166.667 tasks
resource = .6 * 166.667
         = 100
verified = min(166.667, 120)
         = 120
```

The original resource saving is fully reabsorbed: total resource use returns to baseline even though each task is cheaper.

## Arm C — verification-aware capacity

If physical capacity expansion stops at the independently verifiable throughput ceiling:

```text
capacity = 120
resource = .6 * 120 = 72
verified = 120
```

Compared with resource-ceiling reinvestment:

```text
same verified output = 120
resource 100 -> 72
28% less synthetic resource
```

## Result

This creates a concrete capacity-race failure mode:

```text
unit efficiency improves
 -> apparent resource headroom
 -> capacity reinvestment
 -> induced demand absorbs capacity
 -> old resource ceiling fills again
```

A fixed resource ceiling prevents backfire above the ceiling but does not preserve efficiency savings. It can merely convert conservation into full rebound.

The verification-aware arm shows a second problem: expanding physical capacity beyond another scarce production factor can consume resource without increasing independently checked output.

## Boundary

The world is deliberately tiny. There is no provider profit model, capital cost, electricity price, water coupling, construction lag, depreciation, regional grid constraint, or competition among providers yet.

The 28% number is a frozen synthetic comparison, not a real-world savings estimate.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_CAPACITY_REINVESTMENT_COUNTEREXAMPLE
```

## Next physical falsifier

DCRE-013 should endogenize provider investment and resource price. The key question is whether dynamic pricing suppresses the capacity race, shifts it to a different resource, or prices essential demand out of the market.
