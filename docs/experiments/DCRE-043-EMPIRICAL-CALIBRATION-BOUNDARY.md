# DCRE-043 — Empirical calibration boundary v1

## Why this experiment exists

DCRE-001–042 built a large exact/constructive synthetic falsifier chain. That is useful for finding mechanism boundaries, but continuing to add synthetic layers without a reality boundary would turn the laboratory into a self-contained toy universe.

DCRE-043 therefore changes mode.

It records fresh public anchors and explicitly separates:

```text
OBSERVED_COMPANY_REPORTED
AUTHORITATIVE_FORECAST
UNKNOWN_STRUCTURAL_PARAMETER
```

The goal is **not** to fit DCRE coefficients yet. It is to define what the current evidence can and cannot legitimately constrain.

Retrieved: 2026-10-07.

## Public anchors

### Google — simultaneous efficiency improvement and electricity growth

Google reports that its data-center electricity consumption increased 27% year over year in 2024, while also reporting more than six times the computing power per unit of electricity versus five years earlier.

Source:

- https://sustainability.google/commitments/water/

These two company-reported observations are useful because they show that a large unit-efficiency improvement and rising total electricity consumption can coexist.

They **do not** identify DCRE-001 demand elasticity `eta`, prove causal Jevons rebound, or tell us how much of electricity growth was caused by AI, product demand, capacity expansion, cooling, geography, or other factors.

### Google — water stewardship accounting

Google's 2026 Environmental Report reports approximately 7.7 billion gallons replenished in 2025, roughly 78% of its 2025 total freshwater consumption.

Source:

- https://sustainability.google/google-2026-environmental-report/

This establishes that water is a material reported resource dimension. Replenishment is kept semantically separate from reduced withdrawal or reduced consumption; it is not converted into a site-level water-efficiency coefficient.

### LBNL — U.S. data-center electricity scenario envelope

The June 2026 *United States Data Center Energy Usage Report: 2025 Update* estimates that data centers could account for 11.8% of U.S. electricity use in 2030, with a scenario range of 9.5% to 15.3%. The report describes a bottom-up model based on planned IT-equipment shipments, device electricity use, cooling simulations, facility types, and locations.

Source:

- https://bies.lbl.gov/publications/united-states-data-center-energy-2025

This is an authoritative model forecast, not a 2030 observation.

### IEA — data centers as a major electricity-growth driver

IEA *Electricity 2026* projects that data-center expansion will account for around half of total U.S. electricity-demand growth through 2030.

Source:

- https://www.iea.org/reports/electricity-2026/executive-summary

IEA *Energy and AI* Base Case projects global data-center electricity consumption around 945 TWh in 2030.

Source:

- https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai

These remain forecasts with explicit scenario uncertainty.

## What can be calibrated now

Current anchors can support:

```text
1. qualitative consistency checks
2. scenario-envelope stress tests
3. order-of-magnitude / scope checks
```

Examples:

- A DCRE scenario in which unit compute efficiency improves while total electricity use rises is not automatically inconsistent with Google's reported direction of travel.
- U.S. 2030 electricity-share stress tests can be checked against the LBNL 9.5–15.3% scenario envelope without pretending that the envelope identifies a causal model.
- Rapid demand-growth worlds are relevant enough to study because both LBNL and IEA project data centers to be a material U.S. electricity-growth driver.

## What remains unknown

The following are intentionally **not** inferred from these anchors:

```text
causal_demand_elasticity_eta
causal_rebound_coefficient
verified_utility_per_compute
site_level_energy_water_substitution
provider_recovery_response_curve
shock_probability_and_cross_region_correlation
```

In particular:

```text
company efficiency metric + company electricity growth
!= causal demand elasticity

water replenishment percentage
!= site water-use intensity

forecast electricity share
!= observed future demand

compute throughput
!= verified ecosystem utility
```

## Machine-readable guard

`dcre043_empirical_boundary.py` stores the anchors with evidence class, scope, period, units, source URL, and caveat.

The contract contains:

```text
automatic_synthetic_parameter_writes = ()
```

Tests fail if the calibration boundary is casually converted into automatic DCRE parameter writes.

## Result

The lab now has an explicit projection boundary from exact synthetic mechanism studies into real-world evidence.

The next improvement should not be "add more realism everywhere." It should choose one high-value structural unknown and obtain the missing evidence needed to constrain it.

## Next empirical target

The highest-value gap is currently the bridge between:

```text
unit efficiency
-> installed capacity / workload growth
-> total facility electricity
```

A useful DCRE-044 should therefore search for time-series data that jointly observes capacity or compute growth and electricity use at a comparable scope. If the numerator and denominator are not scope-aligned, the model must keep the causal elasticity UNKNOWN rather than manufacture it.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = EMPIRICAL_BOUNDARY_AND_PROVENANCE_CONTRACT_V1
```
