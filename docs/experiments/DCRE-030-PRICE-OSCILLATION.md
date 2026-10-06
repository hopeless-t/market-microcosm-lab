# DCRE-030 — Lagged congestion prices can create temporal oscillation

## Trigger

DCRE-029 shows that identical actors can overconsume the same offpeak headroom when they react concurrently.

A natural correction is a temporal congestion price: make the overloaded period expensive so flexible demand moves elsewhere.

DCRE-030 attacks the assumption that a correct congestion price automatically stabilizes the system when the price is based on the previous period's load.

## Frozen two-slot market

```text
base load A = 40
base load B = 40
flexible load = 40
initial signal A = 60
initial signal B = 40
next price signal = previous realized load
```

Actors send price-responsive flexible work to the cheaper slot.

## FULL_RESPONSE

With 100% of flexible work responding to the lagged signal:

```text
epoch 0: A=40, B=80
epoch 1: A=80, B=40
epoch 2: A=40, B=80
...
```

The cheap period becomes the next expensive period, so the entire flexible load jumps back and forth.

Frozen six-epoch metrics:

```text
peak load = 80
flexible movement = 200 task-units
```

## PARTIAL_RESPONSE

Let only half of the flexible load respond to price and keep the other half evenly anchored.

```text
epoch 0: A=50, B=70
epoch 1: A=70, B=50
...
```

Frozen metrics:

```text
peak load = 70
flexible movement = 100
```

The oscillation remains, but its amplitude and movement cost are lower.

## Result

```text
correct scarcity signal
+ one-step observation lag
+ synchronized response
!= dynamic stability
```

A price can internalize current congestion and still destabilize the next period when all responsive demand chases the same delayed signal.

This is a temporal analogue of DCRE-016 construction-lag oscillation, but the moving object is demand rather than physical capacity.

## Boundary

Prices are simply previous loads. There is no real electricity tariff, bidding, heterogeneity, forecasting, transaction cost, storage, or strategic behavior. Partial response is a synthetic damping arm, not a promoted policy.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_LAGGED_PRICE_RESPONSE_OSCILLATION
```

## Next falsifier

Do not create another generic anti-oscillation controller yet. DCRE-031 should first add heterogeneous response delays or thresholds and test whether diversity dampens synchronized movement naturally, or merely hides instability until a larger shock arrives.
