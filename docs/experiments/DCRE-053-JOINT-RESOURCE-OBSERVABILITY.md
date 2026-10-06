# DCRE-053 — Joint energy/water observability without false WUE promotion

## Trigger

DCRE-052 established a real-world consistency check: Google data-center electricity more than doubled from 2020 to 2024 while reported fleet PUE did not worsen. That is useful evidence that unit/facility efficiency and total resource consumption must remain separate quantities, but it does not identify a causal rebound coefficient.

DCRE-053 asks the next physical-resource question:

> Can FY2024 electricity and water observations be combined into a trustworthy energy-water coefficient?

## Primary evidence

Alphabet’s FY2024 Environmental Indicators Assurance Letter reports, for the year ended December 31, 2024:

```text
Data-center electricity consumption = 30,825,600 MWh
Data-center water consumption       = 7,787 million gallons
```

Both values appear in the assured environmental schedules.

The same assurance material also reveals an important boundary difference:

- the electricity methodology includes electricity for owned/operated global data centers and electricity related to Alphabet IT assets at leased data centers and other locations;
- the water methodology states that relevant operations include owned and fully leased data centers (plus offices and other assets).

Therefore, the labels `data centers` are similar but **metric-scope identity is not certified**.

Primary source:

- Alphabet’s 2025 (FY2024) Environmental Indicators Assurance Letter
- https://www.sustainability.google/reports/alphabet-fy2024-environmental-indicators-assurance-letter/

## Reproducible conditional ratio

If the two published FY2024 aggregates are divided mechanically:

```text
7,787,000,000 gallons / 30,825,600,000 kWh
~= 0.252615 gallons/kWh
~= 0.956251 liters/kWh
```

The arithmetic is reproducible.

But the ratio is promoted only as:

```text
CONDITIONAL_DESCRIPTIVE_RATIO_ONLY
```

It is **not** promoted as Google WUE, nor as a cooling coefficient, nor as an energy-water substitution parameter.

## Why the promotion is blocked

A valid WUE-like or substitution claim would require a shared denominator and matching operational population.

The current evidence does not certify that:

```text
numerator water population == denominator electricity population
```

Therefore these transformations remain blocked:

```text
conditional aggregate ratio
-> WUE
-> marginal cooling tradeoff
-> energy-water substitution coefficient
-> causal resource elasticity
```

This is a scope problem, not an arithmetic problem.

## Result

```text
electricity_third_party_assured = TRUE
water_third_party_assured       = TRUE
metric_scope_identity_certified = FALSE
conditional_gallons_per_kWh     ~= 0.252615
conditional_liters_per_kWh      ~= 0.956251
promoted_WUE                     = UNKNOWN
energy_water_substitution        = UNKNOWN
causal_cooling_tradeoff          = UNKNOWN
authority_effect                 = NONE
```

## Connection to the synthetic chain

DCRE-014 showed synthetically that optimizing energy alone can push load into water, and vice versa. DCRE-053 does **not** calibrate that synthetic tradeoff.

Instead it establishes the empirical prerequisite:

> Before a joint-resource model can be calibrated, the energy and water observations must be proven to describe the same operational population at compatible temporal and spatial grain.

## Claim ceiling

```text
claim_ceiling = JOINT_RESOURCE_OBSERVABILITY_AUDIT_ONLY
```

No real-world WUE, cooling efficiency, marginal water cost, energy-water substitution coefficient, or causal rebound parameter is inferred.

## Next falsifier

DCRE-054 should search for a scope-aligned pair rather than forcing the global aggregates together. The FY2024 assurance letter exposes water use by named data-center location. The next question is whether official location-matched electricity data exist for any of those same facilities. If not, location-level energy-water substitution remains structurally unidentifiable from current public reporting.
