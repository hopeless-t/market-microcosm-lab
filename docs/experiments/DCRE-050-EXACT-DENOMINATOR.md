# DCRE-050 — Exact 2019 data-center denominator remains unobserved

## Trigger

DCRE-049 formalizes the proof obligations for using a historical superset electricity value as a conservative denominator.

A cleaner path would be to avoid the superset bound entirely and use an exact 2019 Google data-center electricity observation.

Google's 2025 Environmental Report appears promising because Figure 2 plots total data-center electricity consumption from 2019 through 2024.

DCRE-050 asks whether the exact 2019 value is actually disclosed.

## Direct inspection of the 2025 report

Figure 2 contains bars for:

```text
2019 2020 2021 2022 2023 2024
```

but the bars do not carry exact numeric labels. The y-axis is in million MWh and is suitable for qualitative trajectory reading, not for recovering an exact denominator without digitization.

The report's environmental data table separately gives exact data-center electricity values only for:

```text
2020  14,426,600 MWh
2021  17,659,000 MWh
2022  20,806,200 MWh
2023  24,294,900 MWh
2024  30,825,600 MWh
```

There is no 2019 data-center row in that numeric table.

## Evidence state

DCRE-050 therefore distinguishes:

```text
2019 data-center electricity represented visually = TRUE
2019 data-center electricity observed exactly      = FALSE
2020-2024 exact table series available             = TRUE
```

The promoted state is:

```text
EXACT_2019_DC_DENOMINATOR = UNOBSERVED
```

## Why chart digitization is blocked

A bar height could be visually estimated, but doing so would create a pseudo-exact input whose uncertainty is dominated by image scaling and reading precision.

More importantly, DCRE-045 already established that exact structural calibration must not be built from chart-reading guesswork when a reproducible numeric source is absent.

Therefore:

```text
chart_digitization_authorized = FALSE
```

This is not a claim that digitization is never scientifically useful. It is a local evidence-authority rule: a digitized approximation cannot silently become an exact historical denominator for a lower-bound or elasticity calculation.

## Primary source

Google 2025 Environmental Report:

- `https://sustainability.google/reports/google-2025-environmental-report/`

Relevant surfaces:

- Figure 2, page 19: 2019–2024 trajectory of total data-center electricity consumption and energy emissions.
- Environmental data table, page 107: exact electricity consumption for data centers, offices/other facilities, and total electricity for 2020–2024.

## Result

```text
promoted_2019_dc_mwh      = UNKNOWN
promoted_DCRE047_bound    = UNKNOWN
candidate_eta             = UNKNOWN
authority_effect          = NONE
```

The research gain is not a new coefficient. It is a precise missing-data boundary.

## Claim ceiling

```text
claim_ceiling = EXACT_DENOMINATOR_OBSERVABILITY_AUDIT_ONLY
```

## Next falsifier

DCRE-051 should inspect the 2025 independent assurance schedule, older Google environmental disclosures, and any official downloadable data source for an exact 2019 data-center electricity value or a certified lineage mapping. If those sources also begin in 2020 or omit the value, the missing denominator should be treated as structurally unavailable in current public reporting rather than repeatedly searched without a stopping rule.
