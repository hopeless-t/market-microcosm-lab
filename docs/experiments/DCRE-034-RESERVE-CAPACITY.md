# DCRE-034 — Reserve capacity is a priced resilience option

## Trigger

DCRE-033 shows that spatial diversification cannot preserve a 100-unit workload when a correlated shock reduces aggregate regional capacity below 100.

A natural correction is to hold reserve capacity.

DCRE-034 attacks two extreme intuitions:

```text
idle reserve is always waste
reserve should always be maximized
```

by pricing reserve against shock risk.

## Frozen world

```text
shock size = 20 capacity units
reserve grid = 0,10,20,30
holding cost = .1 per reserve unit
shortfall penalty = 1 per unserved unit
```

Expected cost is:

```text
holding_cost
+ shock_probability * residual_shortfall * shortfall_penalty
```

## Low-risk world

```text
p = .05
```

Exact grid result:

```text
reserve = 0
expected cost = 1
```

At this probability, holding one unit of reserve costs more than its expected avoided shortfall.

## High-risk world

```text
p = .20
```

Exact grid result:

```text
reserve = 20
holding cost = 2
residual shortfall = 0
expected cost = 2
```

## Marginal knee

A marginal reserve unit is attractive when:

```text
p * shortfall_penalty > holding_cost
```

so the frozen probability knee is:

```text
p = .1 / 1 = .10
```

## Result

```text
high utilization
!= resilience
reserve capacity
!= unconditional waste
```

Idle capacity has option value when the expected avoided shock loss exceeds its holding cost.

But reserve is not free resilience: below the risk/consequence knee it becomes pure carrying cost in this model.

## Boundary

Shock probability is known and stationary, reserve activation is perfect, and there is no construction lag, provider incentive, financing cost, correlated reserve failure, or demand growth. All values are synthetic.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_RESERVE_OPTION_KNEE
```

## Next falsifier

DCRE-035 should endogenize who pays to hold reserve. A socially valuable reserve can disappear in a competitive market if providers earn revenue only when capacity is actively used. The next question is reserve procurement versus free-riding, not more reserve arithmetic.
