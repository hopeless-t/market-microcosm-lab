# DCRE-014 — Resource substitution: energy versus water

## Trigger

DCRE-013 gives the provider a resource price and an endogenous capacity choice. A single price can still represent only the scarcity encoded in that price.

DCRE-014 adds a second physical resource and asks whether optimizing one resource merely displaces pressure into another.

## Frozen technologies

At synthetic throughput 120:

```text
DRY
  energy/task = 1.00
  water/task  = 0.05

WET
  energy/task = 0.70
  water/task  = 0.50

HYBRID
  energy/task = 0.82
  water/task  = 0.20
```

Synthetic viability ceilings:

```text
energy <= 100
water  <= 30
```

No coefficient represents a real cooling system.

## ENERGY_ONLY

Minimize energy intensity:

```text
selected = WET
energy = 84  -> viable
water  = 60  -> violates water ceiling
```

The energy objective succeeds locally while shifting ecological pressure into water.

## WATER_ONLY

Minimize water intensity:

```text
selected = DRY
water  = 6   -> viable
energy = 120 -> violates energy ceiling
```

The reverse single-resource objective produces the mirror failure.

## JOINT_VIABILITY

Require both resource ceilings before ranking the remaining candidates:

```text
selected = HYBRID
energy = 98.4
water  = 24
```

HYBRID is the only jointly viable technology in the frozen world.

## Result

```text
single-resource efficiency
!= multi-resource viability
```

A policy can report success on the priced or measured resource while exporting pressure to an unpriced or weakly constrained resource. This is the physical-resource analogue of earlier proxy failures in verification and allocation.

The experiment does not promote HYBRID or a particular pricing formula. It only constructs a world where optimizing energy alone or water alone is insufficient.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_TWO_RESOURCE_SUBSTITUTION_COUNTEREXAMPLE
```

## Next physical falsifier

DCRE-015 should endogenize provider entry and exit under joint resource prices. The next question is whether a viability-preserving price vector also preserves enough provider surplus and service availability to keep the ecosystem alive.
