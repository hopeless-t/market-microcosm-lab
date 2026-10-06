# DCRE-048 — Reporting-boundary lineage audit

## Trigger

DCRE-047 retains a conditional Google compute-growth lower bound but blocks promotion because the calculation crosses report vintages and relies on an opaque compute-efficiency metric.

DCRE-048 audits the electricity series itself.

The first hypothesis was that visible overlapping total-electricity values were fully stable across the 2023, 2024, and 2025 Environmental Report vintages. A direct table-level check falsified that hypothesis before promotion.

## Report-vintage comparison

### 2023 Environmental Report

```text
2019  12,237,200 MWh
2020  15,138,500 MWh
2021  18,287,100 MWh
2022  21,776,200 MWh
```

### 2024 Environmental Report

```text
2019  12,237,200 MWh
2020  15,138,500 MWh
2021  18,287,100 MWh
2022  21,776,200 MWh
2023  25,307,000 MWh
```

### 2025 Environmental Report

```text
2020  15,166,800 MWh
2021  18,287,100 MWh
2022  21,776,200 MWh
2023  25,307,000 MWh
2024  32,179,900 MWh
```

The overlap therefore partitions into:

```text
stable years = 2019, 2021, 2022, 2023
vintage drift = 2020
2020 absolute drift = 28,300 MWh
```

The initial `OVERLAP_STABLE` interpretation is rejected.

## Why the 2020 discrepancy matters

Google explicitly maintains an internal recalculation policy for historical environmental metrics. The 2024 report states that selected historical energy-consumption metrics were recalculated after reporting-boundary changes, including purchased steam and cooling. The 2025 report likewise notes recalculation of certain previously reported energy-consumption and carbon-free-energy metrics for improved accuracy.

DCRE-048 therefore treats the observed 2020 drift as expected evidence that report vintages are not interchangeable simply because a metric label is identical.

## A useful semantic correction

The 2019 value used by DCRE-047 is correctly labeled:

```text
Total electricity consumption = 12,237,200 MWh
Purchased electricity         = 12,226,200 MWh
```

These are distinct metrics. Total electricity includes purchased and self-generated electricity.

The DCRE-047 inequality did not accidentally use the purchased-electricity value. The remaining problem is lineage compatibility, not metric-name confusion.

## Result

Machine-readable state:

```text
visible_total_electricity_lineage = PARTIAL_DRIFT_DETECTED
stable_overlap_years              = [2019, 2021, 2022, 2023]
drift_years                       = [2020]
maximum_observed_drift            = 28,300 MWh
full_cross_report_lineage         = OPEN
2019 data-center-only electricity = UNKNOWN
compute metric definition         = UNKNOWN
DCRE-047 promoted bound           = BLOCKED
```

This is stronger than either of the two naive positions:

```text
"all vintages are incompatible"
"all matching labels are directly comparable"
```

Instead, compatibility is itself an empirical property that can vary by year and metric.

## Sources

Google environmental reports and report index:

- `https://sustainability.google/reports/`
- `https://sustainability.google/reports/google-2025-environmental-report/`

The 2025 report also decomposes 2024 total electricity into:

```text
data centers                30,825,600 MWh
offices and other facilities 1,354,300 MWh
total                       32,179,900 MWh
```

This confirms the subset semantics at the 2024 endpoint but does not supply an equivalent 2019 data-center-only observation.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = REPORTING_LINEAGE_DRIFT_AUDIT_ONLY
```

No real-world elasticity or promoted compute-growth bound is produced.

## Next falsifier

DCRE-049 should formalize the subset inequality used in DCRE-047. It should distinguish an exact historical denominator from an upper-bound denominator and enumerate which boundary changes preserve or invalidate the lower-bound proof. The goal is not another point estimate; it is a proof obligation for cross-scope partial identification.
