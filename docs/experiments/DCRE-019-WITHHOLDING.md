# DCRE-019 — Strategic withholding of capacity rights

## Trigger

DCRE-018 shows that capacity rights can prevent duplicated construction, but winner-take-all allocation concentrates the right to expand.

DCRE-019 gives the right-holder a scarcity-sensitive market price and asks whether all reserved capacity will actually be deployed.

## Frozen market

```text
baseline capacity = 100
capacity right    = 60
demand            = 160
base task price   = 1.0
scarcity markup   = .03 per unmet task
candidate deploy  = 0,20,40,60
```

Market price rises with unmet demand.

## UNCONSTRAINED_RIGHT_HOLDER

Frozen exact choices:

```text
deploy 60 -> unmet 0  -> price 1.0 -> revenue 60
deploy 40 -> unmet 20 -> price 1.6 -> revenue 64
deploy 20 -> unmet 40 -> price 2.2 -> revenue 44
```

The revenue-maximizing holder deploys only 40 and withholds 20.

The capacity-right mechanism eliminated overbuild in DCRE-018, but concentrated control creates a scarcity-rent incentive that reintroduces service loss.

## USE_OR_LOSE

Add a synthetic penalty `.25` per withheld capacity unit.

The frozen optimum moves back to:

```text
deploy = 60
unmet  = 0
net revenue = 60
```

This is a constructive repair only.

## Result

```text
overbuild prevention
!= deployment incentive
!= service availability
```

A market instrument that constrains investment quantity can still permit strategic non-deployment after rights are allocated.

The use-or-lose penalty is not promoted as policy. Under lower realized demand it can itself create wasteful deployment or strategic gaming; that is deliberately left open.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_CAPACITY_WITHHOLDING_COUNTEREXAMPLE
```

## Next physical falsifier

DCRE-020 should make realized demand uncertain after rights allocation. A rigid use-or-lose obligation may prevent withholding in high demand but force unnecessary activation when demand falls, turning an anti-market-power rule into another rebound source.
