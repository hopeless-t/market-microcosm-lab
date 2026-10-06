# DCRE-056 — Capacity-to-energy theorem without population laundering

## Trigger

DCRE-055 expanded the evidence boundary around The Dalles and found two new kinds of public quantities:

- utility-territory aggregate energy;
- large-load capacity / contract thresholds.

Neither is the missing Google site annual MWh.

A tempting next move is to use power capacity as an annual-energy upper bound.

Mathematically:

```text
annual energy <= power capacity * 8760 hours
```

That theorem is correct. DCRE-056 asks whether the available real-world capacity observation belongs to the same target population.

## Exact mathematical authority

For any continuously bounded load with peak capacity `P` MW:

```text
E_annual <= P * 8760 MWh
```

The inequality is exact because annual energy is the integral of instantaneous power over time and instantaneous power cannot exceed `P`.

## External observation

Oregon Data Center Advisory Committee material reports that Northern Wasco County PUD load grew from roughly 90 MW in January 2016 to 277 MW in January 2026, driven substantially by data-center growth.

That 277 MW observation is useful infrastructure context.

But it is not identified as:

```text
Google The Dalles site capacity
```

It is a utility/service-territory load quantity.

Primary source:

- Oregon Department of Energy, May 29, 2026 Data Center Advisory Committee facilitator summary
- https://www.oregon.gov/energy/get-involved/Documents/2026-05-29-DCAC-Facilitator-Meeting-Summary.pdf

## Counterexample to naive promotion

If one mechanically inserts 277 MW into the theorem:

```text
277 MW * 8760 h = 2,426,520 MWh/year
```

this produces a mathematically valid upper bound for a 277 MW load envelope.

But it is **not** an empirically certified upper bound for Google The Dalles, because the observed 277 MW is not customer-specific, site-specific, or population-matched to that target.

Therefore:

```text
mathematical_bound = 2,426,520 MWh/year
promoted_Google_site_bound = UNKNOWN
```

## Proof certificate

Before a real site-energy upper bound may be promoted, DCRE-056 requires:

```text
capacity_positive                     = TRUE
capacity_customer_specific            = TRUE
capacity_site_specific                = TRUE
capacity_population_matches_target    = TRUE
capacity_is_peak_power_not_energy      = TRUE
```

The current evidence satisfies only the first and last conditions.

## Result

```text
POWER_CAPACITY_TO_ENERGY_THEOREM = PASS
GOOGLE_SITE_CAPACITY_CERTIFICATE = FAIL
GOOGLE_SITE_ENERGY_UPPER_BOUND   = UNKNOWN
GOOGLE_SITE_ANNUAL_ENERGY        = UNKNOWN
authority_effect                 = NONE
```

The key discipline is:

> A conservative inequality is not automatically conservative if the quantity inserted into it belongs to the wrong population.

This mirrors DCRE-049: mathematical authority and empirical authority must remain separate.

## Claim ceiling

```text
claim_ceiling = CAPACITY_TO_ENERGY_THEOREM_AND_CERTIFICATE_ONLY
```

DCRE-056 does not estimate Google The Dalles peak demand, annual MWh, load factor, WUE, or energy-water substitution.

## Next falsifier

DCRE-057 should ask whether **customer-specific load factor** or interval-meter information is publicly observable through utility tariffs, public contracts, regulatory records, or demand-response disclosures. If only minimum take-or-pay or flexibility percentages are exposed, those must not be coerced into realized annual utilization. The next guard is:

```text
CONTRACTED_MINIMUM != REALIZED_LOAD_FACTOR
```
