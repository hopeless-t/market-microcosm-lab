# DCRE-039 — Backlog release can create a second demand wave

## Trigger

DCRE-038 shows a recovery-speed tradeoff using a synthetic linear rebound term tied to restored capacity.

DCRE-039 removes that rebound coefficient and instead keeps a separate state for **unserved work accumulated during the shock**.

The question is whether immediately releasing all deferred work actually clears the backlog faster once recovered capacity is still finite.

## Frozen recovered system

```text
recovered capacity = 120
baseline demand     = 100
shock backlog       = 40
```

So only 20 capacity units per epoch are available to clear backlog without displacing baseline work.

## RELEASE_ALL

Release the entire 40-unit backlog immediately.

```text
epoch 0:
  demand = 100 + 40 = 140
  served = 120
  newly unserved = 20
  ending backlog = 20

epoch 1:
  demand = 120
  ending backlog = 0
```

Metrics:

```text
peak demand = 140
new shortfall = 20
backlog clearance time = 2 epochs
```

## CAPACITY_AWARE

Release only available spare capacity:

```text
epoch 0: release20 -> demand120 -> backlog20
epoch 1: release20 -> demand120 -> backlog0
```

Metrics:

```text
peak demand = 120
new shortfall = 0
backlog clearance time = 2 epochs
```

## Result

```text
fastest attempted demand release
!= fastest completed backlog clearance
```

In this frozen world, dumping all deferred work back into the system does not clear it sooner because recovered throughput remains the bottleneck. It only recreates a service shortfall and a larger demand peak.

This separates two states that should not be conflated:

```text
restored capacity
!= released backlog
```

## Boundary

Backlog has no expiry, priority, user abandonment, value decay, retries, duplication, or heterogeneous deadlines. Baseline demand is fixed and recovered capacity is perfectly reliable. All values are synthetic.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_BACKLOG_RELEASE_SECOND_WAVE
```

## Next direction

The recovery mini-chain has now separated restoration rate, resource peak, and backlog release. DCRE-040 should add **backlog value decay / abandonment** so that capacity-aware delay is no longer free. The next question is when pacing avoids rebound versus when waiting destroys valuable work.
