# DCRE-036 — Nameplate reserve is not usable resilience

## Trigger

DCRE-035 shows that a capacity payment can close the private incentive gap and induce reserve entry.

That does not guarantee the procured reserve is useful.

DCRE-036 attacks a simple procurement rule that buys the cheapest nominal reserve capacity without adjusting for reliability.

## Frozen bids

```text
FLAKY_BIG
  nominal reserve = 20
  holding cost    = .05 / unit
  reliability     = .40
  expected usable = 8

RELIABLE_A
  nominal reserve = 10
  holding cost    = .10 / unit
  reliability     = 1.00
  expected usable = 10

RELIABLE_B
  nominal reserve = 10
  holding cost    = .10 / unit
  reliability     = 1.00
  expected usable = 10
```

Shock world:

```text
shock size = 20
shock probability = .20
shortfall penalty = 1 / unit
```

## NAMEPLATE_CHEAPEST

A nominal target of 20 units buys the lowest holding-cost-per-nameplate bid:

```text
selected = FLAKY_BIG
nominal reserve = 20
expected usable = 8
```

Synthetic system expected cost:

```text
holding cost = 1
expected residual shortfall = .20 * 12 = 2.4
total = 3.4
```

## RELIABILITY_AWARE_EXACT

Enumerate the frozen bid subsets and minimize the same system expected-cost surface.

```text
selected = RELIABLE_A + RELIABLE_B
nominal reserve = 20
expected usable = 20
holding cost = 2
residual shortfall = 0
system expected cost = 2
```

## Result

```text
procured nameplate capacity
!= expected usable reserve
!= resilience
```

A payment mechanism can solve under-procurement and still buy the wrong reserve if it rewards nominal quantity rather than delivered reliability.

The experiment therefore extends the DCRE pattern:

```text
fix one scarcity
-> create a new proxy
-> proxy becomes the next failure surface
```

## Boundary

Reliability is known, stationary, independent, and converted into expected usable units linearly. Real reserve adequacy depends on correlated outages, activation delay, duration, telemetry, geography, fuel, network constraints, and settlement rules.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_RESERVE_QUALITY_COUNTEREXAMPLE
```

## Next direction

Do not recurse into auction design yet. DCRE-037 should return to correlated physical reliability and test whether two individually reliable reserve providers share a hidden failure domain. That can reuse the E022/E023 failure-domain machinery rather than invent another reliability model.
