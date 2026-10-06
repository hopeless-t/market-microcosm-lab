# DCRE-048 — Reporting-boundary lineage audit

## Trigger

DCRE-047 derives a conditional lower bound on Google data-center compute growth, but refuses to promote it because the bound crosses report vintages and depends on a public compute-efficiency endpoint metric whose lineage is not reproducible.

DCRE-048 asks whether the electricity side of that lineage can be narrowed without pretending that all reporting-boundary questions are solved.

## Observed report-vintage overlap

Google's published environmental data tables expose a stable total-electricity sequence across visible overlapping report vintages.

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
2020  15,138,500 MWh
2021  18,287,100 MWh
2022  21,776,200 MWh
2023  25,307,000 MWh
2024  32,179,900 MWh
```

For every year that appears in more than one of these visible tables, the total-electricity value is identical.

Therefore DCRE-048 promotes the narrow statement:

```text
VISIBLE_TOTAL_ELECTRICITY_OVERLAP = STABLE
```

## Why this does not close the lineage

Google explicitly maintains a recalculation policy for historical environmental metrics. The 2024 report states that selected energy-consumption metrics were recalculated, including prior total-energy values after changes to the reporting boundary for purchased steam and cooling. The 2025 report likewise notes recalculation of certain previously reported energy and carbon-free-energy metrics for improved accuracy.

The stable electricity overlap is therefore useful evidence, but not permission to assume that every historical denominator used by every data-center efficiency statement has an identical lineage.

Three gaps remain.

### 1. The current report does not restate 2019 total electricity

The 2025 report's tabular history begins in 2020. The 2019 `12,237,200 MWh` value is visible in the 2023 and 2024 report vintages, not restated in the 2025 table.

### 2. 2019 data-center-only electricity is not disclosed in the same table lineage

DCRE-047 deliberately used total-company electricity as a conservative upper bound on data-center electricity. That is an inequality construction, not a directly observed 2019 data-center denominator.

### 3. `Computing power` remains opaque

The 2025 report anchors the six-times statement to 2024 versus five years earlier, so the endpoint years are now clear. But the report does not expose a reproducible annual compute-power index, normalization rule, or raw metric series.

## Result

DCRE-048 replaces one coarse blocker with a more precise state:

```text
visible total-electricity overlap consistency = PASS
full cross-report lineage                     = OPEN
2019 data-center electricity                  = UNKNOWN
compute metric definition                     = UNKNOWN
DCRE-047 conditional lower bound              = RETAINED
DCRE-047 promoted lower bound                 = BLOCKED
```

This matters because empirical uncertainty is not binary. Some parts of a provenance chain can be independently strengthened while other links remain unresolved.

## Sources

Google environmental reports and report index:

- `https://sustainability.google/reports/`
- `https://sustainability.google/reports/google-2025-environmental-report/`

The visible total-electricity tables are preserved across Google's 2023, 2024, and 2025 Environmental Report vintages. DCRE records the values as evidence-lineage observations, not as causal model coefficients.

Google's 2025 report also explicitly states that in 2024 its data centers delivered over six times more computing power per unit electricity than five years earlier.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = REPORTING_LINEAGE_AUDIT_ONLY
```

No real-world elasticity, rebound coefficient, or promoted compute-growth bound is produced.

## Next falsifier

DCRE-049 should test whether the inequality structure itself can survive the remaining denominator-scope uncertainty. Instead of requiring an exact 2019 data-center value, it should formalize which subset relations are sufficient for a valid lower bound, and which reporting-boundary changes could invalidate those relations. If the subset relation cannot be source-certified, the conditional bound remains non-promoted.
