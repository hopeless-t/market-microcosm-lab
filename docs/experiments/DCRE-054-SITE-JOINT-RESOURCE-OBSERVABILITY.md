# DCRE-054 — Site-level joint-resource observability remains incomplete

## Trigger

DCRE-053 found that the FY2024 global data-center electricity and water totals can be divided mechanically, but the electricity and water reporting populations are not certified identical. Therefore the resulting liters/kWh ratio must not be promoted as WUE or an energy-water substitution coefficient.

A natural next move is to align the geography:

> If water and efficiency are both published for the same named data-center location, can site-level energy-water calibration finally become identifiable?

## Official surfaces that overlap by location

Alphabet’s FY2024 Environmental Indicators Assurance Letter publishes water consumption by named data-center location. Examples include:

```text
Dublin, Ireland             0.1 million gallons consumed
Eemshaven, Netherlands    330.0 million gallons consumed
Hamina, Finland             0.3 million gallons consumed
St. Ghislain, Belgium     393.3 million gallons consumed
```

Google Data Centers separately publishes campus-level PUE for these same locations.

So for multiple named campuses the public evidence state is:

```text
site water volume = OBSERVED
site PUE          = OBSERVED
```

## The missing absolute quantity

The official surfaces inspected for DCRE-054 do **not** disclose corresponding annual site-level electricity consumption in MWh for those campuses.

PUE does not solve that problem.

PUE is a ratio:

```text
PUE = total facility energy / IT equipment energy
```

Without either total facility energy or IT equipment energy in absolute units, a site PUE value cannot reconstruct annual site electricity consumption.

Therefore:

```text
site water + site PUE
!=
site water + site electricity
```

and cannot identify site WUE or a marginal energy-water tradeoff.

## Machine-readable result

DCRE-054 freezes a small overlap set of official locations and records:

```text
water_location_series_observed       = TRUE
campus_pue_series_observed           = TRUE
site_absolute_electricity_observed   = FALSE
identified_site_wue_count            = 0
missing_variable                     = SITE_ABSOLUTE_ELECTRICITY_MWH
site_energy_water_substitution       = UNKNOWN
authority_effect                     = NONE
```

## Why this matters

DCRE-053 failed at global scope identity.

DCRE-054 resolves the location-name problem but exposes a different missing variable: **absolute electricity volume**.

This is a useful refinement of the empirical observability map:

```text
global totals      -> values exist, population identity incomplete
site water + PUE   -> geography aligns, absolute energy volume missing
```

The research problem is therefore not simply “find more data.” It is to identify the exact missing state variable required for each proposed inference.

## Primary sources

Alphabet’s 2025 (FY2024) Environmental Indicators Assurance Letter:

- https://www.sustainability.google/reports/alphabet-fy2024-environmental-indicators-assurance-letter/

Google Data Centers — Power usage effectiveness:

- https://datacenters.google/efficiency/

The assurance letter provides FY2024 water consumption by named data-center location. The Google Data Centers efficiency surface provides campus-level PUE, including the overlapping locations used by the frozen DCRE-054 fixture.

## Claim ceiling

```text
claim_ceiling = SITE_JOINT_RESOURCE_OBSERVABILITY_AUDIT_ONLY
```

DCRE-054 does not claim that no site-level electricity data exist anywhere. It claims only that the defined official Google/Alphabet source surfaces inspected here do not expose the absolute annual MWh needed to identify site-level WUE or energy-water substitution.

## Next falsifier

DCRE-055 should expand the source boundary carefully to external authoritative infrastructure records—utility filings, environmental permits, grid interconnection records, or regulator disclosures—to ask whether absolute electricity can be observed for any one matched site without mixing incompatible facility boundaries. If external records still provide capacity rather than actual consumption, `POWER_CAPACITY != ENERGY_CONSUMPTION` must become the next guard.
