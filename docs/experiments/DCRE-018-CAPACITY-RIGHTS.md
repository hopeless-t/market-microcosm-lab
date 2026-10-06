# DCRE-018 — Capacity rights: quantity coordination versus concentration

## Trigger

DCRE-017 constructs a market where two providers share a perfect demand forecast but each independently closes the full market gap, duplicating physical investment.

A natural decentralized repair is to issue capacity rights or reservations for only the residual market gap.

DCRE-018 asks whether solving the quantity problem also solves market structure.

## Frozen market

```text
initial capacity = 100
next demand      = 160
residual gap     = 60
providers        = 2
construction resource = .5 per new capacity unit
```

## NO_CAPACITY_RIGHTS

Both providers invest 60:

```text
future capacity       = 220
idle capacity         = 60
construction resource = 60
```

This reproduces DCRE-017 duplicated investment.

## WINNER_TAKE_ALL_RIGHTS

Exactly 60 rights are issued to one provider:

```text
investments           = 60, 0
future capacity       = 160
idle capacity         = 0
construction resource = 30
investment HHI        = 1.0
```

The quantity problem disappears, but new investment is maximally concentrated.

## SPLIT_CAPACITY_RIGHTS

The same rights are split evenly:

```text
investments           = 30, 30
future capacity       = 160
idle capacity         = 0
construction resource = 30
investment HHI        = .5
```

Both rights mechanisms hit the same capacity target with the same construction resource. Their market structure differs.

## Result

```text
capacity coordination
!= competitive structure
```

A quantity instrument can remove duplicated construction without deciding whether ownership, bargaining power, and future withholding become concentrated.

DCRE-018 does not claim that equal splitting is optimal. It only shows that a mechanism that solves overbuild can create or preserve a distinct concentration problem.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_CAPACITY_RIGHTS_COUNTEREXAMPLE
```

## Next physical falsifier

DCRE-019 should let a capacity-right holder strategically withhold reserved capacity. The next question is whether rights that prevent overbuild can create scarcity rents or service loss through non-deployment.
