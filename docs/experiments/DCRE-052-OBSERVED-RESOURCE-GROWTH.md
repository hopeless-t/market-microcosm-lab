# DCRE-052 — Observed resource growth under non-worsening facility PUE

## Trigger

DCRE-051 closed the search for an exact 2019 Google data-center electricity denominator within a predefined primary-source set.

Rather than continue chasing one missing number, DCRE-052 pivots to a directly observed question using the complete 2020–2024 data-center electricity series:

> Can total data-center electricity grow substantially while a major facility-efficiency metric remains flat or improves?

This is deliberately **not** a rebound-elasticity estimate.

## Observed Google data-center electricity

Google's 2025 Environmental Report publishes exact data-center electricity consumption:

```text
2020  14,426,600 MWh
2021  17,659,000 MWh
2022  20,806,200 MWh
2023  24,294,900 MWh
2024  30,825,600 MWh
```

From 2020 to 2024:

```text
growth ratio ~= 2.1367x
four-year CAGR ~= 20.9%
```

So reported total data-center electricity more than doubled over the interval.

## Facility-efficiency context

Google reports average annual fleet-wide PUE across Google-owned and -operated data-center campuses as:

```text
2020  1.10
2021  1.10
2022  1.10
2023  1.10
2024  1.09
```

The 2021 Environmental Report independently states that 2020 average annual PUE was 1.10. The 2025 Environmental Report states that in 2024 the fleet-wide annual PUE fell below 1.10 to 1.09 for the first time in six years.

Within this broad operational context:

```text
PUE did not worsen
while
total reported data-center electricity > doubled
```

That observation is qualitatively consistent with the DCRE synthetic distinction:

```text
unit/facility efficiency != total resource consumption
```

## Important scope guard

DCRE-052 does **not** divide total data-center electricity by PUE to infer a precise IT-energy series.

Why?

The published PUE metric is explicitly described as fleet-wide across **Google-owned and -operated data-center campuses**. The environmental electricity boundary may include a broader set of Alphabet/Google data-center electricity, including electricity associated with leased facilities or IT assets depending on reporting criteria.

Therefore:

```text
PUE_SCOPE == ELECTRICITY_SCOPE
```

has not been certified.

Machine-readable state:

```text
scope_identity_certified = FALSE
derived_it_energy_series = UNKNOWN
```

This blocks a tempting but potentially invalid calculation:

```text
IT_energy = total_DC_electricity / PUE
```

until the boundaries are proven identical.

## What is actually learned

DCRE-052 promotes only the observational consistency statement:

```text
TOTAL_DC_ELECTRICITY_MORE_THAN_DOUBLED
WHILE_FLEET_PUE_DID_NOT_WORSEN
```

It does **not** establish that PUE improvement caused demand growth, that efficiency induced rebound, or that a Jevons effect occurred.

Possible explanations for the electricity increase include workload growth, capacity expansion, hardware mix, utilization, AI accelerator deployment, geographic expansion, or other factors. DCRE-052 does not identify their contributions.

## Primary sources

Google 2025 Environmental Report:

- `https://sustainability.google/reports/google-2025-environmental-report/`

Google 2021 Environmental Report:

- `https://sustainability.google/reports/google-2021-environmental-report/`

The 2021 report states 2020 fleet-wide average annual PUE = 1.10. The 2025 report gives the 2020–2024 PUE series and 2020–2024 data-center electricity series, with 2024 PUE = 1.09.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = EMPIRICAL_CONSISTENCY_CHECK_ONLY
causal_rebound_identified = FALSE
candidate_eta = UNKNOWN
```

## Next falsifier

DCRE-053 should use same-year, same-report 2024 energy and water observations to ask a different directly observable question: what aggregate water-per-electricity ratio is implied by the assured 2024 data-center totals, and what does that ratio **not** tell us about cooling substitution or marginal water intensity?

This moves the empirical chapter from one resource to joint-resource observability without pretending that an aggregate ratio is a causal coefficient.
