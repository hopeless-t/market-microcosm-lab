# DCRE-022 — Spatial resource complementarity

## Trigger

DCRE-014 introduces energy/water substitution inside one synthetic site. Real ecological pressure is also spatial: different regions can have different resource headroom.

DCRE-022 asks whether workload placement can exploit complementary regional constraints instead of optimizing a single resource or concentrating all work in one apparently rich region.

## Frozen regions

```text
GRID_RICH
  energy ceiling = 100
  water ceiling  = 20

WATER_RICH
  energy ceiling = 50
  water ceiling  = 100
```

Workload:

```text
total tasks       = 100
energy/task       = .8
water/task        = .3
allocation grid   = 0,25,50,75,100 tasks in GRID_RICH
```

All coefficients are synthetic.

## ENERGY_HEADROOM_GREEDY

Put all work in the region with larger energy headroom:

```text
GRID_RICH tasks=100
energy=80  -> viable
water=30   -> violates ceiling 20
```

## WATER_HEADROOM_GREEDY

Put all work in the region with larger water headroom:

```text
WATER_RICH tasks=100
water=30  -> viable
energy=80 -> violates ceiling 50
```

## EXACT_JOINT_GRID

Enumerate the frozen allocation grid and require both regional resource constraints.

```text
GRID_RICH  tasks=50 -> energy40, water15
WATER_RICH tasks=50 -> energy40, water15
```

The 50/50 allocation is jointly viable on this coarse grid.

## Result

```text
aggregate resource headroom
!= spatial viability
```

A region can look attractive under one resource while being locally fragile under another. Spatial diversification can use complementary headroom, but it also introduces network, latency, transmission, and coordination costs that are absent here.

DCRE-022 therefore does not promote geographic spreading. It only establishes that resource constraints must retain location rather than being collapsed into one global scalar budget.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_SPATIAL_RESOURCE_ALLOCATION
```

## Next physical falsifier

DCRE-023 should add inter-region transfer/network cost and locality requirements. A spatially resource-viable allocation may become service- or network-infeasible once moving work and data between regions has a price.
