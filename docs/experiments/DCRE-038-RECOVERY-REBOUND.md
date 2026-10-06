# DCRE-038 — Recovery speed can trade service loss for a second resource peak

## Trigger

DCRE-033–037 build a resilience chain around correlated shocks and reserve capacity. The next question is what happens **after** a shock has occurred.

A natural objective is to restore capacity as fast as possible.

DCRE-038 attacks the assumption that fastest recovery is automatically best by giving restoration itself a scarce-resource footprint and allowing restored capacity to unlock rebound demand in the same epoch.

## Frozen shock world

```text
pre-shock baseline demand = 100
post-shock capacity       = 60
rebound demand per restored capacity unit = .5
recovery resource per restored capacity unit = 1.5
```

All values are synthetic.

## AGGRESSIVE

Restore all 40 missing capacity units in one step.

```text
epoch 0: capacity 60, demand 100, shortfall 40
epoch 1: +40 capacity -> capacity100
         rebound demand = 100 + .5*40 = 120
         shortfall = 20
         recovery resource = 60
epoch 2: no rebuild, demand100, shortfall0
```

Totals:

```text
service shortfall integral = 60
peak recovery resource     = 60
total recovery resource    = 60
```

The system restores nominal capacity immediately but creates a second-wave service shortfall while the rebound demand arrives.

## DAMPED

Restore 20 units in each of two epochs.

```text
epoch 0: shortfall40
epoch 1: capacity80, demand110, shortfall30, recovery resource30
epoch 2: capacity100, demand110, shortfall10, recovery resource30
epoch 3: calm demand100, shortfall0
```

Totals:

```text
service shortfall integral = 80
peak recovery resource     = 30
total recovery resource    = 60
```

Damping lowers the recovery-resource peak but prolongs service loss.

## Exact synthetic knee

For an illustrative scalarization:

```text
loss = total service shortfall + lambda * peak recovery resource
```

AGGRESSIVE and DAMPED are equal when:

```text
60 + 60 lambda = 80 + 30 lambda
lambda = 20 / 30 = 2/3
```

So on this frozen surface:

```text
lambda < 2/3 -> AGGRESSIVE preferred
lambda > 2/3 -> DAMPED preferred
```

## Result

```text
fastest recovery
!= minimum service loss plus minimum recovery-resource peak
```

Recovery is itself a resource-allocation problem. A policy can restore capacity faster and reduce cumulative service shortfall while creating a much larger emergency resource peak and a transient rebound wave.

The useful object is therefore a recovery Pareto surface, not one scalar "time to restore" metric.

## Boundary

The rebound coefficient, resource multiplier, and scalar weight are synthetic. There is no real construction supply chain, grid restoration, cloud workload, capital cost, repair crew, material scarcity, or demand estimate here.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_RECOVERY_SPEED_RESOURCE_TRADEOFF
```

## Next falsifier

DCRE-039 should remove the fixed rebound coefficient. If rebound depends on accumulated backlog, delayed demand, or user adaptation, the fastest nominal-capacity restoration can trigger a larger delayed wave than the one-step linear model predicts. The next experiment should separate **restored capacity** from **released backlog** rather than adding another governance control.
