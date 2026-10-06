# DCRE-025 — Reuse-count knee for prepared compact representations

## Trigger

DCRE-024 finds a compact representation that is jointly viable across network, encode-compute, and semantic-fidelity constraints.

But compact/canonical representations often have a fixed preparation cost. If the object is used once, preparing it may be irrational even when each later transfer is cheaper.

DCRE-025 adds reuse and asks when the fixed preparation cost amortizes.

## Frozen synthetic cost surface

All values are abstract resource-cost units. Network and compute are combined only through an explicit synthetic `1:1` weight for this experiment.

### RAW_PER_USE

```text
preparation compute = 0
network per use      = 25
compute per use      = 0

cost(N) = 25N
```

### PREPARED_COMPACT_REUSE

```text
preparation compute = 30
network per use      = 10
compute per use      = 2

cost(N) = 30 + 12N
```

## Exact crossover

Set the two synthetic composite costs equal:

```text
25N = 30 + 12N
13N = 30
N = 30 / 13 ~= 2.3077
```

Therefore the first integer reuse count at which prepared compact wins is:

```text
N = 3
```

Frozen examples:

```text
uses=1: RAW 25 < PREPARED 42
uses=2: RAW 50 < PREPARED 54
uses=3: RAW 75 > PREPARED 66
uses=8: RAW 200 > PREPARED 126
```

## Result

```text
per-transfer efficiency
!= lifecycle efficiency
```

A representation with a fixed preparation cost can be worse for one-off work and better for repeated work. Whether canonicalization, precomputation, caching, or projection is worthwhile depends on expected reuse, not just the marginal transfer cost.

This gives a market interpretation to reuse-aware materialization: **prepare durable structure only when its expected service life can repay the fixed cost**.

## Boundary

The `1:1` network/compute exchange rate is a synthetic scalarization chosen only to construct a crossover. Real systems require measured resource prices or a non-scalar viability surface.

The experiment also assumes the prepared representation remains valid across uses. Staleness/invalidation can destroy amortization and is intentionally excluded here.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_REUSE_AMORTIZATION_KNEE
```

## Next falsifier

DCRE-026 should add invalidation risk. If the underlying meaning changes often, a prepared representation may need to be rebuilt before its reuse count reaches the amortization knee. The next question is the stability/reuse region in which preparation remains economically viable.
