# DCRE-041 — Recovery throughput should preserve value, not just clear volume

## Trigger

DCRE-040 shows that delaying backlog can destroy value and creates a pacing-versus-burst knee.

The next problem is heterogeneous backlog: if only part of the queue can be served now, **which work should receive scarce recovery throughput?**

DCRE-041 deliberately reuses the already-qualified E018 portfolio scheduler instead of building another priority engine.

## Frozen backlog classes

Current recovery capacity:

```text
20 units
```

Backlog:

```text
BULK
  size = 20
  current value = 20
  delayed value = 20
  delay loss = 0
  arrival = first

URGENT
  size = 10
  current value = 40
  delayed value = 10
  delay loss = 30

FLEX
  size = 10
  current value = 20
  delayed value = 18
  delay loss = 2
```

## FIFO

FIFO spends all 20 recovery units on `BULK`.

The remaining classes are delayed:

```text
preserved total value = 20 + 10 + 18 = 48
prevented delay loss = 0
```

The queue shrinks by 20 units, but the highest-decay work waits.

## E018 portfolio projection

Map:

```text
backlog size             -> E018 audit_cost_units
delay loss prevented     -> E018 restoration_value
```

The exact oracle and bounded DP both select:

```text
URGENT + FLEX
capacity used = 20
prevented delay loss = 32
preserved total value = 80
```

`BULK` can wait without modeled value loss.

## Result

```text
backlog volume cleared
!= backlog value preserved
```

A recovery policy that maximizes units processed can destroy more value than a value-decay-aware allocation using the same throughput budget.

The architectural result matters too: **the lab reused E018's existing portfolio mechanism rather than inventing a new recovery scheduler.**

## Boundary

Value and delayed value are synthetic and known exactly. Backlog classes are indivisible, deadlines are one-step, and there is no fairness, starvation, strategic labeling, or uncertainty in value estimates.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_BACKLOG_VALUE_PORTFOLIO
```

## Chapter handoff

The recovery mini-chain now separates:

```text
capacity restoration rate
recovery-resource peak
backlog release rate
backlog value decay
recovery throughput allocation
```

Do not recurse into queue-governance rules here. The next foreground branch should reconnect recovery to **provider investment and post-shock resource prices**: a recovery subsidy or emergency price can accelerate rebuilding but may also trigger synchronized over-reconstruction or another capacity rebound.
