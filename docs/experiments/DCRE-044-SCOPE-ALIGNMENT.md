# DCRE-044 — Scope-alignment audit before causal calibration

## Trigger

DCRE-043 established an empirical boundary and prohibited automatic writes from public observations or forecasts into synthetic structural parameters.

DCRE-044 asks a narrower question:

> Do currently available public numbers provide a scope-aligned numerator and denominator from which DCRE's causal demand elasticity could legitimately be identified?

The answer in this first audit is **no**.

Retrieved: 2026-10-07.

## Candidate 1 — Google efficiency versus electricity growth

Google reports both:

```text
>6x computing power per unit of electricity versus five years earlier
27% year-over-year data-center electricity-consumption growth in 2024
```

Source:

- https://sustainability.google/commitments/water/

This is a valuable qualitative consistency signal for DCRE: unit efficiency can improve while total electricity use rises.

It is not a causal elasticity pair because:

```text
five-year efficiency comparison
!= one-year electricity-growth interval

compute-per-electricity ratio
!= independently observed workload/capacity-volume time series
```

## Candidate 2 — LBNL accelerator shipments versus total electricity

The 2026 LBNL update reports an updated 2024 U.S. data-center electricity estimate of about 192 TWh and a Reference Case of 649 TWh in 2030.

It also reports accelerator shipments of just over seven million units in 2024 and a projection of 19 million units in 2030.

Source:

- https://escholarship.org/uc/item/33m6w3x0

This is closer to a common macro scope, but the grain still fails:

```text
accelerator shipments = equipment flow
not installed compute stock or delivered workload

reported total electricity = servers + storage + networking + facility infrastructure
not accelerator electricity alone
```

Dividing shipment growth by total electricity growth would manufacture a structural elasticity from mismatched quantities.

## Candidate 3 — Microsoft PUE/WUE panel without workload volume

Microsoft publishes a matched FY24/FY25 operational table for fully owned and controlled datacenters that were operational for the relevant eligibility period.

Global values include:

```text
PUE: FY24 1.16 -> FY25 1.17
WUE: FY24 .30 -> FY25 .27 L/kWh
```

Source:

- https://datacenters.microsoft.com/sustainability/efficiency/

This is useful for constraining facility-overhead and water-intensity directions, but it still lacks a matched public workload, installed-compute, or throughput-volume series needed for a demand elasticity.

## Promotion contract

A public evidence pair may only become a causal-elasticity candidate when all of these are explicit:

```text
matched_scope
matched_period_or_explicit_lag_model
stock_or_throughput_volume_not_unmatched_shipment_flow
total_resource_boundary_documented
metric_semantics_and_denominators_documented
causal_confounders_or_identification_strategy_explicit
```

Current result:

```text
candidate pairs audited = 3
causal-elasticity-ready pairs = 0
eta_status = UNKNOWN
automatic_eta_write = None
```

## Why UNKNOWN is a result

The lab now distinguishes two kinds of progress:

```text
finding a number
finding an identifiable quantity
```

The former is easy and dangerous. The latter is what allows a synthetic mechanism parameter to cross into empirical calibration.

DCRE-044 therefore treats refusal to estimate `eta` as successful evidence discipline, not missing work.

## What the current evidence can still do

Even without causal calibration, the sources can constrain model relevance and scenario envelopes:

- LBNL's 2024 historical estimate and 2030 scenario range can bound U.S. electricity stress-test magnitudes.
- LBNL sensitivity cases identify server installations, accelerator mix/lifetime, utilization, and idle power as important modeled drivers.
- Microsoft PUE/WUE can inform whether a synthetic facility-overhead or water-intensity scenario is directionally absurd.
- Google's simultaneous efficiency improvement and electricity growth can reject a model invariant that incorrectly assumes unit efficiency must force total consumption downward.

None of these uses identifies a causal rebound coefficient.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = EMPIRICAL_SCOPE_ALIGNMENT_AUDIT_V1
```

## Next empirical target

DCRE-045 should pursue **aligned historical stock/throughput and electricity series**, not another forecast ratio. Candidate paths include:

1. historical installed server-stock series paired with the same LBNL electricity boundary;
2. operator-level workload/capacity and electricity disclosures with common period/scope;
3. a documented quasi-experimental or structural identification strategy if direct volume data remain unavailable.

If none can satisfy the promotion contract, `eta` remains UNKNOWN and the lab should calibrate only non-causal scenario envelopes.
