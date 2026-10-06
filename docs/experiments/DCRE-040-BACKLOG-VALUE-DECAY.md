# DCRE-040 — Backlog value decay creates a pacing/burst knee

## Trigger

DCRE-039 shows that releasing deferred work only at available spare capacity can avoid a second demand wave without increasing backlog-clearance time in its homogeneous frozen world.

That result makes waiting free.

DCRE-040 adds value decay to the delayed half of the backlog and gives the system an alternative: buy temporary burst capacity now.

## Frozen world

```text
backlog = 40
normal spare capacity = 20 / epoch
burst clears the extra 20 immediately
burst cost = 4 synthetic value units
```

If pacing is used, 20 units complete now and 20 complete one epoch later. Let `d` be the fraction of value lost by that one-epoch delay.

## PACE

```text
net value = 20 + 20(1-d)
          = 40 - 20d
```

## BURST

All 40 units complete now, but the emergency burst costs 4:

```text
net value = 40 - 4 = 36
```

## Exact decay knee

Set the two strategies equal:

```text
40 - 20d = 36
20d = 4
d = .20
```

Frozen examples:

```text
d=.10 -> PACE 38 > BURST 36
d=.30 -> PACE 34 < BURST 36
```

## Result

```text
rebound-safe pacing
!= universally value-preserving recovery
```

Waiting can be the right way to avoid a second resource peak when deferred work is patient. The same pacing policy becomes costly when backlog value decays faster than the price of temporary capacity.

The relevant recovery state therefore includes at least:

```text
backlog quantity
backlog value decay
available spare capacity
burst-resource price
```

## Boundary

Value is linear and homogeneous, decay lasts exactly one epoch, and burst capacity is perfectly reliable with a fixed price. There is no priority queue, deadline distribution, abandonment behavior, or real economic valuation.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_BACKLOG_DECAY_BURST_KNEE
```

## Next direction

Do not turn this into a general scheduling-governance branch. DCRE-041 should add heterogeneous backlog classes and ask whether a single recovery rate destroys value even when total capacity is sufficient. The key new question is **which work to restore first under finite recovery throughput**, while reusing existing portfolio machinery where possible.
