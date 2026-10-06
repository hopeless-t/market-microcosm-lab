# DCRE-062 — Independent utility energy-structure cross-check

## Trigger

DCRE-058 established a system-level observation from Oregon public records: Northern Wasco County PUD load rose from 90 MW in 2016 to 277 MW in 2026, with data centers described as a substantial driver.

DCRE-061 then independently verified one favorable outcome—low 2024 residential price—using EIA data.

Before chasing harder reliability metrics, DCRE-062 asks a simpler official-data question:

> What does EIA directly report about NWCPUD’s 2024 annual electricity sales structure?

## Official EIA observations

U.S. Energy Information Administration 2024 utility-level retail-sales tables report:

```text
Northern Wasco County PUD

total sales       1,530,602 MWh
industrial        1,263,389 MWh across 190 customers
commercial          121,887 MWh
residential         145,326 MWh
```

Primary sources:

- EIA 2024 Utility Bundled Retail Sales — Industrial
  - https://www.eia.gov/electricity/sales_revenue_price/pdf/table_8.pdf
- EIA 2024 Utility Bundled Retail Sales — Commercial
  - https://www.eia.gov/electricity/sales_revenue_price/pdf/table_7.pdf
- EIA 2024 Utility Bundled Retail Sales — Residential
  - https://www.eia.gov/electricity/sales_revenue_price/pdf/table_6.pdf
- EIA 2024 Utility Bundled Retail Sales — Total
  - https://www.eia.gov/electricity/sales_revenue_price/pdf/table_10.pdf

The sector values sum exactly to the reported total in the frozen observation.

## Directly derived structure

```text
industrial share  = 1,263,389 / 1,530,602 ~= 82.54%
commercial share  ~= 7.96%
residential share ~= 9.49%
```

So NWCPUD’s 2024 delivered energy is strongly concentrated in EIA’s industrial sector classification.

The total also independently confirms a utility-scale annual energy volume above one terawatt-hour.

## Critical classification guard

DCRE-062 does **not** equate:

```text
industrial sales == data-center sales
```

EIA’s industrial sector includes loads other than data centers, and the public table does not expose an exact data-center share for NWCPUD.

Therefore:

```text
INDUSTRIAL_MAJORITY_OF_SALES = TRUE
INDUSTRIAL_EQUALS_DATA_CENTER = FALSE
EXACT_DATA_CENTER_SHARE       = UNKNOWN
```

This blocks a tempting but unsupported calculation that would assign all 1.263 TWh of industrial sales to data centers.

## Connection to the synthetic and empirical chain

DCRE-012–020 model how large concentrated loads can create capacity, pricing, concentration, and cost-allocation problems.

DCRE-058 observes utility-scale load growth with data centers source-reported as a substantial driver.

DCRE-062 independently adds an official annual-energy structure:

```text
utility annual sales > 1.5 TWh
industrial sector > 82% of sales
```

This strengthens the claim that large-load planning is economically material without fabricating a customer-specific data-center meter.

## Result

```text
independent_system_energy_crosscheck = TRUE
utility_total_2024_mwh                = 1,530,602
industrial_share                      ~= 0.8254
industrial_equals_data_center         = FALSE
exact_data_center_share               = UNKNOWN
customer_specific_causality           = UNKNOWN
authority_effect                      = NONE
```

## Claim ceiling

```text
claim_ceiling = UTILITY_ENERGY_STRUCTURE_CROSSCHECK_ONLY
```

No exact data-center share, Google-specific annual MWh, causal growth attribution, tariff effect, or welfare conclusion is inferred.

## Next falsifier

DCRE-063 should continue the independent-outcome ladder only if an official utility-level reliability row can be recovered directly from the EIA-861 Reliability schedule. The EIA confirms that the 2024 final Form EIA-861 detailed-data ZIP contains utility-level SAIDI/SAIFI responses, but until the NWCPUD row itself is directly inspected, secondary transcriptions of its reliability metrics remain evidence candidates rather than promoted official observations.
