# DCRE-058 — Pivot from hidden customer meter to observable utility-scale pressure

## Trigger

DCRE-054 through DCRE-057 progressively closed several tempting shortcuts to Google The Dalles annual MWh:

```text
site water + PUE        -> no absolute energy
utility aggregate load  -> wrong population
capacity                 -> power is not energy
contract minimum         -> obligation is not realized utilization
24/7 delivery            -> availability is not consumption
```

At this point, continuing to search the same hidden customer meter has declining information value.

DCRE-058 changes the empirical question:

> What robust system-level claim can be made using public quantities without customer-specific MWh?

## Primary observation

The Oregon Governor’s Data Center Advisory Committee facilitator summary for May 29, 2026 records Northern Wasco County PUD load growth from:

```text
January 2016  90 MW
January 2026 277 MW
```

and states that the increase was driven substantially by data centers.

Primary source:

- Oregon Department of Energy, Data Center Advisory Committee, May 29, 2026 facilitator summary
- https://www.oregon.gov/energy/get-involved/Documents/2026-05-29-DCAC-Facilitator-Meeting-Summary.pdf

## Directly observed system-level growth

The load ratio is:

```text
277 / 90 ~= 3.078x
```

So the public record supports:

```text
UTILITY_LOAD_MORE_THAN_TRIPLED = TRUE
```

over the stated ten-year endpoints.

The source also provides a qualitative attribution:

```text
DATA_CENTERS = SUBSTANTIAL_DRIVER
```

but not an exact numerical share.

Therefore:

```text
EXACT_DATA_CENTER_SHARE = UNKNOWN
```

## Why this pivot matters

A hidden customer-level variable is not required to establish every economically relevant fact.

DCRE-058 can promote a narrower but stronger observation:

> Large-load growth associated substantially with data-center expansion became a material utility-scale planning problem in the Northern Wasco County PUD service territory.

This observation is directly relevant to DCRE-012 through DCRE-020, which model capacity expansion, infrastructure planning, synchronized investment, concentration, and service obligations.

It does **not** identify Google’s individual contribution, a causal elasticity, or a counterfactual without data centers.

## Machine-readable state

```text
utility_start_load_mw                   = 90
utility_end_load_mw                     = 277
utility_load_growth_ratio               ~= 3.078
data_centers_reported_substantial_driver = TRUE
exact_data_center_share                 = UNKNOWN
customer_specific_causality             = UNKNOWN
system_level_planning_pressure_observed = TRUE
authority_effect                        = NONE
```

## Result

DCRE-058 is an empirical strategy correction.

Instead of treating missing customer MWh as a blocker for the whole research program, it separates:

```text
customer-level calibration      -> still blocked
system-level planning pressure  -> observable
```

That allows Market Microcosm to keep moving without fabricating hidden quantities.

## Claim ceiling

```text
claim_ceiling = SYSTEM_LEVEL_LOAD_GROWTH_AND_SOURCE_ATTRIBUTION_ONLY
```

No exact data-center share, Google-specific load, annual energy, load factor, price elasticity, or counterfactual is inferred.

## Next falsifier

DCRE-059 should inspect whether the public record contains observable **institutional response** to this load growth—separate customer classes, direct cost assignment, deposits, take-or-pay, grid studies, infrastructure payment, or flexibility programs—and distinguish:

```text
policy / contract mechanism observed
!=
mechanism caused good outcomes
```

The next empirical chapter should map real governance mechanisms onto the synthetic market-failure chain without claiming causal effectiveness unless outcome evidence supports it.
