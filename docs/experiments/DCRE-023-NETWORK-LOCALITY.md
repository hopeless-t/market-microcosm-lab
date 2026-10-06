# DCRE-023 — Network/locality cost can erase spatial resource viability

## Trigger

DCRE-022 finds a resource-viable 50/50 split across two regions with complementary energy/water headroom.

That result assumes moving work between regions is free.

DCRE-023 adds a synthetic network/locality budget and asks whether the resource-optimal placement survives once remote execution has a transfer cost.

## Frozen projection from DCRE-022

```text
GRID_RICH  tasks = 50
WATER_RICH tasks = 50
```

Under DCRE-022 this split is jointly viable for regional energy and water.

Assume the workload/data origin is GRID_RICH, so tasks placed in WATER_RICH are remote.

Synthetic network ceiling:

```text
network <= 20
```

## RAW_TRANSFER

Remote transfer cost is `.50` network units per remote task.

For the DCRE-022 50/50 split:

```text
remote tasks = 50
network      = 25
```

The allocation remains energy/water viable but violates the network ceiling.

On the frozen allocation grid `0,25,50,75,100`, **no allocation is jointly viable** under the raw-transfer coefficient: placements that reduce remote traffic eventually violate one of the regional physical-resource ceilings.

## COMPACT_TRANSFER

Reduce remote transfer to `.30` network units per task while leaving the physical workload unchanged.

The same 50/50 split becomes:

```text
remote tasks = 50
network      = 15
```

and passes the synthetic network ceiling together with the DCRE-022 regional energy/water ceilings.

## Result

```text
spatial resource viability
!= network/locality viability
```

Geographic placement can exploit complementary physical headroom only if communication/locality cost fits inside the same viability region.

Conversely, a sufficiently cheaper projection/transfer path can change the *feasible placement set* rather than merely making an already-feasible system cheaper.

This is why communication efficiency belongs inside the market ecology rather than being treated only as an implementation optimization.

## Boundary

The `.50`, `.30`, and `20` values are synthetic. There is no real bandwidth, latency, data-sovereignty, egress-price, carbon, or privacy estimate here.

`COMPACT_TRANSFER` is deliberately abstract: it could represent compression, canonical minimum-sufficient projections, locality-aware caching, less duplicated context, or another mechanism. DCRE-023 does not identify which mechanism is best.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_SPATIAL_NETWORK_FEASIBILITY_COUNTEREXAMPLE
```

## Next physical falsifier

DCRE-024 should endogenize the compact-transfer mechanism itself. Compression/projection may save network resource while adding compute, memory, latency, or reconstruction error. The next question is whether a cheaper transfer path merely moves scarcity back into local computation or semantic loss.
