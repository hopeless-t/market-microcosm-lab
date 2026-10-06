# DCRE-017 — Shared-forecast investment herding

## Trigger

DCRE-016 shows that lagged reactive capacity control can oscillate. A natural correction is better forecasting.

Forecasting can reduce stale reaction, but shared forecasts can also synchronize provider investment.

DCRE-017 isolates that coordination failure with a deliberately perfect forecast: the error comes from duplicated response, not forecast inaccuracy.

## Frozen market

```text
providers = 2
initial market capacity = 100
forecast next demand    = 160
actual next demand      = 160
construction resource   = .5 per capacity unit
```

The market gap is exactly 60.

## UNCOORDINATED_SHARED_FORECAST

Each provider observes the same market-level gap and behaves as if it alone must close it:

```text
provider A investment = 60
provider B investment = 60
future capacity       = 220
actual demand          = 160
idle capacity          = 60
construction resource = 60
```

The forecast is perfectly correct, yet correlated action overbuilds the market.

## COORDINATED_RESIDUAL_SPLIT

The same gap is divided across providers:

```text
provider A investment = 30
provider B investment = 30
future capacity       = 160
idle capacity          = 0
construction resource = 30
```

Both policies fully serve the frozen demand. The difference is duplicated physical investment.

## Result

```text
shared information
!= coordinated action
```

A common high-quality forecast can become a common-mode behavioral signal. If each actor optimizes against the same aggregate residual without accounting for other actors' responses, better information can synchronize overinvestment rather than prevent it.

This is the physical-capacity analogue of DCRE-004 belief herding: the same structural mechanism reappears after projection into a different market surface.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_SHARED_FORECAST_HERDING_COUNTEREXAMPLE
```

The forecast is intentionally perfect. No claim is made about real forecast accuracy or provider investment behavior.

## Next physical falsifier

DCRE-018 should remove central coordination and ask whether a decentralized capacity-right or reservation market can prevent duplicated investment without creating market power or strategic withholding.
