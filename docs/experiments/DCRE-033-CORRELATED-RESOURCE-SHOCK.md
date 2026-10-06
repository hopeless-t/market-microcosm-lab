# DCRE-033 — Spatial diversity fails under correlated resource shock

## Trigger

DCRE-022 shows that spatial placement can exploit complementary regional headroom. DCRE-032 shows that behavioral diversity can collapse under a large common shock.

DCRE-033 projects the same question back onto physical infrastructure: **does geographic diversification still protect service when the resource shock is correlated across regions?**

## Frozen market

Two regions each have synthetic service capacity 60 under baseline conditions.

```text
Region A capacity = 60
Region B capacity = 60
total workload    = 100
```

The allocation grid moves work in 10-task increments.

## Baseline

```text
50 / 50
```

is feasible.

## Independent regional shock

Region A falls to 40 while Region B remains at 60:

```text
A=40
B=60
aggregate capacity=100
```

The exact coarse reallocation is:

```text
40 / 60
```

and the full workload remains feasible.

## Common shock

Both regions fall to 40:

```text
A=40
B=40
aggregate capacity=80 < workload100
```

No allocation on the grid can preserve the full workload.

## Result

```text
spatial diversity
!= independent failure domains
```

Geographic distribution protects against local loss only while the relevant resource shock is not common-mode across the distributed sites.

This is the physical-resource projection of the E022/E023 failure-domain lesson: counting regions is not the same as counting independent resource domains.

## Boundary

Capacity is a scalar abstraction. There is no real grid topology, watershed, fuel market, weather field, transmission network, disaster model, or regional demand. Shock correlation is constructed rather than estimated.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_CORRELATED_RESOURCE_SHOCK_COUNTEREXAMPLE
```

## Next direction

DCRE-034 should add reserve capacity or flexible curtailment and ask how much slack is worth holding against a common shock. The key tradeoff is idle-resource cost versus resilience, not merely average utilization.
