# DCRE-020 — Use-or-lose obligations under demand uncertainty

## Trigger

DCRE-019 shows that concentrated capacity rights can create profitable withholding and that a use-or-lose penalty can restore full deployment in the frozen high-demand world.

DCRE-020 attacks the assumption that full deployment is always socially useful after rights are allocated.

## Frozen uncertainty

```text
baseline capacity = 100
capacity right    = 60
activation resource = .5 per deployed capacity unit

LOW demand  = 100 with probability .5
HIGH demand = 160 with probability .5
```

The demand state is observed before deployment in the flexible arm.

## DEMAND_CONTINGENT_DEPLOYMENT

Deploy only the residual capacity actually needed:

```text
LOW  -> deploy 0
HIGH -> deploy 60

expected served demand      = 130
expected unmet demand       = 0
expected activation resource= 15
expected idle capacity      = 0
```

## RIGID_USE_OR_LOSE

Force the full 60 units to be active in both demand states:

```text
LOW  -> deploy 60, idle 60
HIGH -> deploy 60, idle 0

expected served demand       = 130
expected unmet demand        = 0
expected activation resource = 30
expected idle capacity       = 30
```

The rigid obligation delivers no additional service in the frozen world while doubling expected activation resource.

## Result

```text
anti-withholding rule
!= demand-contingent viability
```

A rule that repairs market power under high demand can become a rebound mechanism when demand falls. The regulator has moved from under-deployment risk to over-activation risk.

The flexible arm is not a free solution: real demand observability can be delayed or manipulated. DCRE-020 only demonstrates that unconditional activation is not generally equivalent to service assurance.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_USE_OR_LOSE_UNCERTAINTY_COUNTEREXAMPLE
```

## Next physical falsifier

DCRE-021 should add delayed/noisy demand measurement so demand-contingent deployment itself can fail. The key question becomes the value and latency of operational telemetry relative to activation cost and service risk.
