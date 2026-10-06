# DCRE-047 — Conditional partial identification without promotion

## Trigger

DCRE-046 found a near-miss: Google publicly reports both a data-center electricity series and an endpoint statement that its data centers deliver more than six times as much computing power per unit electricity as five years earlier.

The evidence is insufficient for a point estimate, but it may still support a **conditional lower bound**.

DCRE-047 asks a narrower question:

> Can we preserve mathematically valid inequality information without silently promoting unverified cross-report assumptions?

## Public inputs

### 2024 Google data-center electricity

Google's 2025 Environmental Report reports 2024 data-center electricity consumption of:

```text
30,825,600 MWh
```

### 2019 Google total electricity

Google's historical environmental reporting gives 2019 total company electricity consumption of:

```text
12,237,200 MWh
```

Because data-center electricity is a subset of total company electricity:

```text
E_DC_2019 <= E_TOTAL_2019
```

therefore, if the reporting boundaries are compatible:

```text
E_DC_2024 / E_DC_2019
>= 30,825,600 / 12,237,200
~= 2.519
```

### Compute-per-electricity endpoint statement

Google currently states that its data centers deliver **six times more computing power per unit electricity than five years ago**.

Taking `6x` only as a strict lower-bound factor for the matched 2019→2024 endpoint gives the conditional identity:

```text
compute_growth
= compute_per_electricity_growth * electricity_growth
> 6 * 2.519
> 15.11x
```

## Why the >15.11x value is not promoted

The arithmetic is valid only under assumptions that are not yet verified.

### 1. Denominator-scope equivalence

The 2019 number is **total Google electricity**, while the 2024 number is **data-center electricity**. Using total electricity as an upper bound makes the inequality conservative only if the historical reporting scopes are compatible enough for subset reasoning.

### 2. Reporting-boundary compatibility

Google has recalculated prior environmental metrics in later reports as reporting boundaries changed. The 2019 total value and 2024 data-center value come from different report vintages. DCRE-047 has not established a common restated boundary for both endpoints.

### 3. Compute-metric stability

The public `computing power per unit electricity` claim is an endpoint statement, not a reproducible annual metric series. Google described roughly seven times more computing power for the same electrical power in a 2020 publication and uses a six-times-over-five-years statement today. These refer to different windows and are not inherently contradictory, but they demonstrate why the metric cannot be treated as a stable public index without its definition and lineage.

## Contract

DCRE-047 preserves two different objects:

```text
conditional mathematical bound:
  compute_2024 / compute_2019 > 15.11x
  IF all scope/lineage/metric assumptions hold

promoted empirical bound:
  UNKNOWN
```

Machine-readable state:

```text
endpoint_year_alignment                  = TRUE
denominator_scope_equivalence_verified   = FALSE
reporting_boundary_compatibility_verified= FALSE
compute_metric_stability_verified        = FALSE
promoted_compute_growth_lower_bound      = UNKNOWN
candidate_eta                            = UNKNOWN
```

This is the first DCRE experiment to explicitly retain a useful **conditional identification result** while refusing an authority upgrade.

## Why this matters

A binary evidence system would force one of two bad choices:

1. discard the >15.11x implication entirely because assumptions are unresolved; or
2. present >15.11x as an empirical fact and hide the assumptions.

Partial identification provides a third state:

```text
mathematical implication = retained
empirical promotion      = blocked
```

That is a better fit for Market Microcosm's separation between world truth, operational truth, and certification truth.

## Primary-source lineage

Google Sustainability / Environmental Reports:

- `https://sustainability.google/reports/google-2025-environmental-report/`
- `https://sustainability.google/reports/`

Google Cloud efficiency statements:

- `https://cloud.google.com/ai-infrastructure`
- `https://cloud.google.com/blog/topics/sustainability/google-achieves-four-consecutive-years-of-100-percent-renewable-energy`

The earlier ~7x and current 6x statements are used only to justify the `COMPUTE_METRIC_STABILITY` blocker, not to interpolate an annual series.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = CONDITIONAL_PARTIAL_IDENTIFICATION_ONLY
```

DCRE-047 does not estimate real-world rebound elasticity, does not promote a compute-growth lower bound, and does not authorize policy inference.

## Next falsifier

DCRE-048 should audit Google reporting-boundary lineage across report vintages. If a restated 2019 data-center electricity value under a boundary compatible with 2024 can be located and the compute metric lineage can be made reproducible, some blockers may be discharged. Otherwise the partial bound remains conditional and the missing lineage itself becomes the promoted empirical result.
