# DCRE-028 — Temporal resource complementarity

## Trigger

DCRE-022–027 show that useful capacity depends on spatial resource headroom, communication cost, representation cost, reuse stability, and finite near-workload storage.

DCRE-028 returns to the physical market and adds **time** as another placement dimension.

The question is whether moving flexible work out of an energy-constrained period can simply move scarcity into another physical resource.

## Frozen two-period world

```text
PEAK base tasks    = 70
OFFPEAK base tasks = 20
flexible tasks     = 40
energy/task        = .8

PEAK water/task    = .2
OFFPEAK water/task = .4

PEAK energy ceiling    = 70
PEAK water ceiling     = 30
OFFPEAK energy ceiling = 100
OFFPEAK water ceiling  = 20
```

All values are synthetic.

## ENERGY_SHIFT_GREEDY

Move all flexible work to OFFPEAK:

```text
PEAK tasks=70
energy=56
water=14

OFFPEAK tasks=60
energy=48
water=24 -> fails water ceiling
```

Energy headroom improves while water viability fails.

## WATER_SHIFT_GREEDY

Keep all flexible work in PEAK to avoid OFFPEAK water pressure:

```text
PEAK tasks=110
energy=88 -> fails energy ceiling
```

## EXACT_JOINT_GRID

Enumerate flexible PEAK allocation on the coarse grid `0,10,20,30,40`.

The only jointly viable point is:

```text
flexible PEAK=10
flexible OFFPEAK=30

PEAK tasks=80
energy=64
water=16

OFFPEAK tasks=50
energy=40
water=20
```

## Result

```text
time shifting
!= energy viability
!= multi-resource temporal viability
```

Moving work in time can reduce one peak while creating another resource peak in the destination period.

The control surface must therefore retain both **resource type** and **time**, rather than flattening load shifting into one scalar electricity-price response.

## Boundary

This is a two-period deterministic synthetic world. There is no real grid mix, weather, cooling model, electricity tariff, water price, deadline distribution, storage loss, or carbon coefficient.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_TEMPORAL_MULTI_RESOURCE_ALLOCATION
```

## Next falsifier

DCRE-029 should add multiple independent actors. Even when each actor sees the same offpeak headroom correctly, synchronized load shifting can consume the same apparent slack twice and recreate a peak.
