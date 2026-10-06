# DCRE-015 — Provider entry/exit under joint resource prices

## Trigger

DCRE-014 shows that joint energy/water viability can require a compromise technology rather than optimizing either resource alone.

DCRE-015 asks the next ecological question: **what happens to provider participation when those scarcities are priced?**

A price vector can preserve physical resource ceilings while shrinking provider supply below the service floor.

## Frozen providers

```text
SCALE
  capacity=70, energy/task=.75, water/task=.15, fixed cost=15

LOCAL
  capacity=35, energy/task=.90, water/task=.08, fixed cost=20

WET
  capacity=60, energy/task=.65, water/task=.50, fixed cost=10
```

Synthetic viability constraints:

```text
service capacity >= 100
energy <= 100
water <= 25
```

Providers remain active only when modeled profit is non-negative.

## LOW_RESOURCE_PRICE

```text
energy price=.10
water price=.10
```

All three providers remain:

```text
capacity = 165  -> service viable
energy   = 123  -> fails ceiling
water    = 43.3 -> fails ceiling
```

Cheap resources preserve supply while allowing ecological overshoot.

## JOINT_SCARCITY_PRICE

```text
energy price=.40
water price=1.20
```

Only SCALE remains profitable:

```text
capacity = 70   -> service fails
energy   = 52.5 -> viable
water    = 10.5 -> viable
```

Physical viability is restored by pricing enough providers out of the market that service viability collapses.

## JOINT_PRICE_PLUS_LOCAL_SERVICE_CREDIT

A synthetic targeted credit of 3 is added to LOCAL under the same resource prices.

```text
active = SCALE + LOCAL
capacity = 105 -> service viable
energy   = 84  -> viable
water    = 13.3 -> viable
public credit cost = 3
```

This arm is a constructive existence proof only: in the frozen world, a targeted service-side transfer can preserve both resource and service constraints.

## Result

```text
resource-price viability
!= provider viability
!= service viability
```

Prices that correctly expose physical scarcity can still destroy the supply structure needed for the ecosystem to function. Conversely, low prices can preserve provider surplus while externalizing resource collapse.

The service credit is not promoted as policy. DCRE-011 already showed that protected categories and allocation labels can be Goodharted. The result only establishes that provider entry/exit must sit inside the viability model rather than outside it.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_PROVIDER_ENTRY_EXIT_COUNTEREXAMPLE
```

No number estimates real provider economics, subsidies, electricity/water prices, or market concentration.

## Next physical falsifier

DCRE-016 should add construction lag and time-varying demand. A market that is viable in static equilibrium may still oscillate or collapse when capacity arrives after the demand/resource signal that triggered it.
