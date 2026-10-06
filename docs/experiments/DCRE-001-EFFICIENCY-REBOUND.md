# DCRE-001 — Exact efficiency-rebound knee

## Question

When per-task resource cost falls, under what demand-elasticity and capacity-response conditions does total resource use actually fall, remain unchanged, or increase?

This experiment uses a deterministic synthetic small world. It does not estimate any real data center.

## World

Baseline demand and capacity are both 100 synthetic task units. An efficiency ratio `e` in `(0, 1]` is the resource cost per served task relative to baseline.

Demand responds to cheaper tasks as:

```text
D(e, eta) = 100 * (1 / e)^eta
```

where `eta` is demand elasticity.

Capacity responds to induced demand with `k` in `[0, 1]`:

```text
C = 100 * (1 + k * (D / 100 - 1))
served = min(D, C)
resource = e * served
```

The exact grid is:

```text
e   = 1.0, 0.8, 0.6, 0.4
eta = 0.0, 0.5, 1.0, 1.5, 2.0
k   = 0.0, 0.5, 1.0
```

for 60 cells.

## Exact elasticity knee

When capacity fully follows demand (`k = 1`):

```text
resource = e * 100 * (1/e)^eta
         = 100 * e^(1-eta)
```

Therefore, for any genuine efficiency improvement (`e < 1`):

- `eta < 1` => `CONSERVATION`: total resource use falls;
- `eta = 1` => `FULL_REBOUND`: induced demand exactly consumes the efficiency gain;
- `eta > 1` => `BACKFIRE`: total resource use rises above baseline.

The model therefore does not treat unit efficiency as sufficient evidence for system-level conservation.

## Verification capacity

A second resource is finite verification capacity, fixed at 120 task units.

The open arm can serve work beyond that verification ceiling. Its verified output is:

```text
verified_open = min(served_open, 120)
```

The `VERIFIED_GATE` arm refuses to materialize work beyond what can be independently verified:

```text
served_gate = min(served_open, 120)
```

The gate is deliberately narrow. It does not claim that all unverified work has zero value. It asks a stricter question: how much resource is spent on work that cannot increase independently checked output in this model?

## Frozen grid result

The 60-cell exact grid produces:

```text
CONSERVATION  = 33 cells
FULL_REBOUND  = 18 cells
BACKFIRE      = 9 cells
verification-starved = 19 cells
```

Across the complete grid:

```text
aggregate open resource        ~= 5326.2470
aggregate verified-gate resource ~= 4460.7956
aggregate verified output       ~= 6444.6319 in both arms
resource reduction at equal verified output ~= 16.2488%
```

This aggregate is only a checksum over the frozen synthetic grid, not a policy recommendation or real-world savings estimate.

## Failure biopsy

The interesting state is not merely `BACKFIRE`.

A cell can be:

1. resource-conserving and verification-safe;
2. resource-conserving but verification-starved;
3. full-rebound;
4. backfire with useful verified growth;
5. backfire where extra resource buys no extra verified output because verification is saturated.

DCRE-001 establishes only the first boundary and a verification-saturation detector. Later experiments should split useful vs speculative demand, heterogeneous quality, queue latency, provider solvency, dynamic resource price, water intensity, and multi-actor distributional effects.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = DETERMINISTIC_SYNTHETIC_SMALL_WORLD
```

No empirical coefficient is inferred here. The exact result is useful because it provides a falsifiable reference surface for later richer models.
