# DCRE-063 — Empirical evidence matrix and promotion guard

## Trigger

DCRE-043 through DCRE-062 moved the research from frozen synthetic falsifiers into real-world evidence. That phase now contains several distinct evidence qualities:

- company-reported observations;
- third-party-assured primary observations;
- independent government cross-checks;
- public-source qualitative attributions;
- candidate values transcribed from official datasets by secondary services;
- unresolved causal claims.

Without an explicit matrix, those categories can blur together as the chain grows.

DCRE-063 normalizes the empirical evidence state without collapsing it to a scalar score.

## Evidence classes

```text
PRIMARY_SOURCE_REPORTED
THIRD_PARTY_ASSURED_PRIMARY
INDEPENDENT_OFFICIAL_CROSSCHECK
SECONDARY_DERIVED_CANDIDATE
```

These are categorical provenance/authority states, not a universal ranking. A company-reported quantity can be exactly the right evidence for one descriptive claim while still being insufficient for a causal one.

## Current promoted observations

The matrix includes, among others:

- Google data-center electricity more than doubled from 2020 to 2024;
- FY2024 Google data-center electricity and water totals appear on third-party-assured schedules;
- EIA independently reports NWCPUD 2024 residential price at 7.72 cents/kWh, below the Oregon residential average;
- EIA independently reports NWCPUD 2024 total sales of 1,530,602 MWh, with more than 82% classified as industrial sales;
- Oregon public records report NWCPUD load growth from 90 MW in 2016 to 277 MW in 2026 and describe data centers as a substantial driver;
- NWCPUD publicly documents multiple large-load governance mechanisms.

Every one of these rows remains:

```text
causal = FALSE
```

because none identifies the relevant counterfactual.

## Reliability candidate guard

EIA confirms that the final 2024 Form EIA-861 detailed-data package contains utility-level Reliability responses, including SAIDI/SAIFI where reported.

Secondary services derived from EIA-861 currently surface a candidate NWCPUD 2024 reliability pair of approximately:

```text
SAIDI = 34.8 minutes
SAIFI = 0.22 interruptions/customer
```

But the NWCPUD row in the official EIA-861 Reliability file has not been directly inspected in the current evidence path because the binary ZIP cannot be read through the present retrieval surface.

Therefore DCRE-063 stores that pair only as:

```text
SECONDARY_DERIVED_CANDIDATE
promoted = FALSE
```

The existence of the official schedule is not the same as direct observation of the target row.

Official source defining the target dataset:

- EIA Form EIA-861 detailed data, Reliability schedule
  - https://www.eia.gov/electricity/data/eia861/

## Why there is no single evidence score

A scalar authority score would hide the shape of uncertainty.

For example:

```text
assured water total
```

can have strong measurement provenance while still failing a scope-identity requirement for WUE.

Likewise:

```text
independently verified low residential price
```

can be a strong outcome observation while remaining useless for causal attribution without a counterfactual.

DCRE-063 therefore keeps separate fields for:

```text
source / provenance class
promotion state
causal state
specific blocker
```

## Result

The empirical chapter now supports an explicit ladder:

```text
observation candidate
-> source-qualified observation
-> independently cross-checked outcome
-> causal identification
```

Current DCRE evidence reaches the first three states for different claims, but **zero rows reach causal identification**.

The reliability candidate remains below promotion until a direct official utility row is inspected.

## Claim ceiling

```text
claim_ceiling = EMPIRICAL_EVIDENCE_STATE_NORMALIZATION_ONLY
authority_effect = NONE
```

DCRE-063 does not create new physical, economic, reliability, or policy-effect estimates.

## Next research direction

The matrix makes the highest-value gaps visible:

1. direct official utility-level reliability evidence, if obtainable without lowering provenance standards;
2. genuinely independent financial/reliability outcomes;
3. a credible comparative or quasi-experimental design before any governance-effect claim;
4. return to broader Market Microcosm mechanisms if the marginal value of another data-point cross-check falls below the value of a new market/ecology question.

This last condition is intentional: the empirical audit must not become another infinite side tunnel.
