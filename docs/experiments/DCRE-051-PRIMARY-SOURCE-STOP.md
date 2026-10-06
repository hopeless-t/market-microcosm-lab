# DCRE-051 — Primary-source stop rule for the 2019 denominator

## Trigger

DCRE-050 established that Google's 2025 Environmental Report visually represents a 2019 data-center electricity bar but publishes exact data-center values only from 2020 onward.

The next risk is research-pathology rather than arithmetic: repeatedly searching the same missing denominator without a stopping rule.

DCRE-051 therefore audits the highest-authority primary surfaces available for the two endpoints and asks whether the 2019 data-center-only denominator becomes observable.

## FY2019 assurance surface

Alphabet's 2020 (FY2019) Environmental Indicators Assurance Letter includes, in its reviewed schedule:

```text
Total energy consumption  12,749,458 MWh
Electricity consumption   12,237,198 MWh
```

The accompanying criteria describe the subject-matter geography as Alphabet Inc. and subsidiaries' data centers, offices, and networking infrastructure under operational control (Global Facilities), with Calico and Sidewalk Labs excluded for the listed energy/emissions scope.

This materially strengthens one piece of DCRE-047:

```text
2019 total electricity is not an unaudited convenience number.
```

It is a third-party-reviewed reported metric.

But the assurance schedule does **not** split the 12,237,198 MWh into data centers versus offices/other facilities.

## FY2024 assurance surface

Alphabet's 2025 (FY2024) Environmental Indicators Assurance Letter includes an exact electricity-consumption schedule:

```text
Data centers                 30,825,600 MWh
Offices and other facilities  1,354,300 MWh
Total electricity            32,179,900 MWh
```

The current criteria describe the reporting boundary as Alphabet globally, using the operational-control approach for owned and leased data centers, offices, and other assets.

Thus:

```text
2024 target-specific denominator = observed in assurance schedule
2019 target-specific denominator = absent from assurance schedule
```

## Boundary lineage remains open

The two assurance letters clearly share an operational-control concept, but their published boundary wording is not identical:

```text
2019: data centers + offices + networking infrastructure; explicit exclusions
2024: owned/leased data centers + offices + other assets; Alphabet globally
```

DCRE-051 does not infer that this wording difference necessarily means the populations are incompatible. It records the narrower statement:

```text
CROSS_BOUNDARY_SUBSET_CERTIFIED = FALSE
```

because an explicit lineage mapping from the 2019 target population to the 2024 data-center population has not been found.

## Search stopping rule

The denominator search is considered complete for the following primary-source set:

1. FY2019 Environmental Indicators Assurance Letter;
2. FY2024 Environmental Indicators Assurance Letter;
3. Google 2025 Environmental Report Figure 2;
4. Google 2025 Environmental Report environmental-data table.

None exposes an exact FY2019 data-center-only electricity value.

The promoted state is therefore deliberately scoped:

```text
EXACT_2019_DC_DENOMINATOR
= PUBLICLY_UNOBSERVED_IN_CHECKED_PRIMARY_SOURCES
```

This does **not** claim that no unpublished record exists or that no future official disclosure can ever surface. It means this research branch has reached its predefined evidence stop condition.

## Result

```text
FY2019 total electricity assured            = TRUE
FY2019 total electricity                    = 12,237,198 MWh
FY2019 exact data-center split observed     = FALSE
FY2024 exact data-center electricity assured= TRUE
FY2024 data-center electricity              = 30,825,600 MWh
boundary wording identical                  = FALSE
cross-boundary subset certified             = FALSE
promoted DCRE-047 bound                     = UNKNOWN
candidate eta                               = UNKNOWN
next action                                 = PIVOT_FROM_DENOMINATOR_SEARCH
```

The missing denominator is now a bounded evidence gap rather than an open-ended search task.

## Primary sources

Google Sustainability:

- `https://sustainability.google/reports/alphabet-fy2019-environmental-indicators-assurance-letter/`
- `https://sustainability.google/reports/alphabet-fy2024-environmental-indicators-assurance-letter/`
- `https://sustainability.google/reports/google-2025-environmental-report/`

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = PRIMARY_SOURCE_MISSING_DATA_AUDIT_ONLY
```

No rebound elasticity, compute-growth bound, or historical data-center denominator is promoted.

## Next research direction

DCRE-052 should stop chasing the missing 2019 split and use the exact 2020–2024 data-center electricity series for a different, directly observable question.

A high-information next test is whether total data-center electricity can more than double while facility overhead efficiency remains approximately flat or improves. That would provide an empirical consistency check for the synthetic distinction:

```text
unit/facility efficiency != total resource consumption
```

without pretending to identify causal rebound or demand elasticity.
