# DCRE-016 — Construction lag and capacity oscillation

## Trigger

DCRE-015 introduces provider entry/exit under static resource prices. Static viability does not imply dynamic stability when capacity takes time to arrive or retire.

DCRE-016 adds a one-period construction/decommission lag to an alternating demand shock.

## Frozen demand trace

```text
100, 180, 100, 180, 100, 180
```

Initial capacity is 100.

Each policy observes the current demand-capacity gap and schedules a signed capacity adjustment that arrives one period later.

## FULL_REACTIVE_ONE_PERIOD_LAG

The provider schedules 100% of the current gap.

Capacity becomes:

```text
100, 100, 180, 100, 180, 100
```

It is almost perfectly out of phase with demand.

Frozen totals:

```text
total unmet + idle mismatch = 400
capacity movement            = 320
```

A locally intuitive "close the whole gap" rule creates repeated overbuild/underbuild because the signal is stale by the time capacity arrives.

## DAMPED_HALF_RESPONSE

Schedule only 50% of the observed gap.

Frozen totals:

```text
total mismatch    = 285
capacity movement = 115
unmet demand      = 195
idle capacity     = 90
```

The damped policy reduces both mismatch and construction churn in this trace, but still leaves substantial unmet demand.

## Result

```text
static equilibrium viability
!= dynamic stability
```

Capacity control can become a delayed feedback system. A rule that would be reasonable with instantaneous actuation can oscillate when construction and retirement have latency.

DCRE-016 does not promote the 50% damping coefficient. It is only a constructive counterexample showing that actuation lag must be modeled explicitly.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_DELAYED_CAPACITY_CONTROL_COUNTEREXAMPLE
```

## Next physical falsifier

DCRE-017 should introduce expectations rather than purely reactive control. Forecasting may reduce lag-induced oscillation, but shared forecasts can also synchronize provider investment and recreate a capacity race at the market level.
