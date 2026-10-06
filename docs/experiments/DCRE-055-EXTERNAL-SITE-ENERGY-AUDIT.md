# DCRE-055 — External infrastructure records still do not identify site annual energy

## Trigger

DCRE-054 aligned geography by matching named Google data-center locations across two official surfaces:

- location-level water consumption;
- campus-level PUE.

But absolute annual electricity consumption by site remained unobserved.

DCRE-055 expands the evidence boundary beyond Google/Alphabet to authoritative public infrastructure records around The Dalles, Oregon.

The question is:

> Do utility or regulator records provide the missing annual MWh for the Google data center, or only adjacent quantities such as aggregate utility load and contract capacity?

## External authoritative observations

Northern Wasco County People’s Utility District states that it has served data-center customers since 2005 and describes rapid large-load growth in its service territory. A public history notes that district load more than doubled and exceeded one billion kilowatt-hours per year.

That is useful system context, but it is **utility-territory aggregate energy**, not a customer-specific Google annual-consumption value.

Oregon Data Center Advisory Committee material describing Northern Wasco County PUD’s large-load service process distinguishes expected peak-load and service-agreement thresholds, including:

```text
expected peak load > 1 MW
loads > 5 MW -> Electric Service Agreement
```

These are planning / contract / capacity quantities, not realized annual energy.

Primary sources:

- Northern Wasco County PUD, data-center services and historical system-load material
  - https://www.nwascopud.org/about-us/data-center-services/
  - https://www.nwascopud.org/news-releases/a-sense-of-purpose/
- Oregon Department of Energy, Data Center Advisory Committee presentation by Northern Wasco County PUD
  - https://www.oregon.gov/energy/get-involved/Documents/07-Humaira-Falkenberg-NWCPUD-DCAC-05-29-2026.pdf

## Semantic guard

DCRE-055 explicitly prevents two invalid coercions:

```text
MW capacity or contract threshold
!=
MWh annual consumption
```

and

```text
utility-territory annual load
!=
individual customer annual load
```

Even a perfectly accurate 100 MW capacity value would still not determine annual MWh without load factor and operating-time information. Likewise, a utility’s one-billion-kWh system total cannot be assigned to one customer without a customer-specific allocation.

## Machine-readable result

```text
utility_aggregate_energy_observed       = TRUE
power_or_contract_capacity_observed     = TRUE
customer_site_annual_energy_observed    = FALSE
google_the_dalles_annual_mwh            = UNKNOWN
POWER_CAPACITY_IS_ENERGY_CONSUMPTION    = FALSE
UTILITY_AGGREGATE_IS_CUSTOMER_LOAD      = FALSE
site_WUE                                = UNKNOWN
authority_effect                        = NONE
```

## Result

Expanding the source boundary adds infrastructure context but does not close the site-energy gap.

The missing state variable remains:

```text
GOOGLE_THE_DALLES_ACTUAL_ANNUAL_ELECTRICITY_CONSUMPTION
```

The evidence ladder is now:

```text
Google official surface:
  site water observed
  site PUE observed
  site MWh missing

external authoritative infrastructure records:
  utility aggregate energy observed
  capacity / contract thresholds observed
  customer annual MWh still missing
```

This is stronger than merely saying “data unavailable.” It identifies which neighboring quantities are public and why none is algebraically interchangeable with the target quantity.

## Claim ceiling

```text
claim_ceiling = EXTERNAL_INFRASTRUCTURE_OBSERVABILITY_AUDIT_ONLY
```

No Google site annual-energy estimate, load factor, WUE, or energy-water substitution coefficient is inferred.

## Next falsifier

DCRE-056 should test whether a **bounded interval** for site annual energy can be constructed without inventing a point estimate. For example, a certified service-capacity upper bound plus hard physical limits could in principle imply an energy upper bound:

```text
annual_energy <= power_capacity * 8760 hours
```

But that is only valid if the capacity value is actually customer/site specific and refers to the same facility population. The next experiment should separate a mathematically valid capacity-to-energy bound from an empirically certified one, mirroring DCRE-049’s theorem-versus-certificate discipline.
