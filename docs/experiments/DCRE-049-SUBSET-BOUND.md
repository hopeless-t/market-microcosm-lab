# DCRE-049 — Proof obligations for cross-scope partial identification

## Trigger

DCRE-047 retains a conditional >15x compute-growth implication. DCRE-048 then found a real report-vintage drift in 2020 total electricity, proving that metric labels alone do not certify historical boundary compatibility.

DCRE-049 strips the problem down to the inequality itself.

The question is:

> What must be true for a historical **superset** electricity observation to provide a valid lower bound for an unobserved historical **target** denominator?

## Mathematical theorem

Let:

```text
T0 = historical target electricity
U0 = observed historical superset electricity
T1 = current target electricity
r  = lower bound on growth in activity per unit electricity
```

If:

```text
0 < T0 <= U0
0 < T1
r > 0
```

then:

```text
T1 / T0 >= T1 / U0
```

and therefore:

```text
activity_growth > r * T1 / U0
```

The arithmetic used by DCRE-047 is therefore mathematically valid **if the subset relation is certified**.

Using its conditional numbers:

```text
T1 = 30,825,600 MWh
U0 = 12,237,200 MWh
r  = 6
```

produces a conditional lower bound greater than 15x.

## The empirical proof certificate

A theorem is not an empirical certificate.

DCRE-049 requires all of the following before a bound may be promoted:

```text
current_target_positive                         = TRUE
historical_superset_positive                    = TRUE
historical_target_subset_of_superset_certified  = TRUE
current_and_historical_target_same_population   = TRUE
activity_metric_endpoint_comparable             = TRUE
```

For the current Google evidence state, the first two are trivial numeric facts. The remaining three are still blocked.

Why?

- the 2019 total-electricity value comes from an earlier report lineage;
- the current report exposes data-center electricity under an Alphabet operational-control boundary, while the 2019 data-center-only denominator is not tabulated;
- the public `computing power per unit electricity` statement does not expose a reproducible metric definition or raw endpoint series.

Therefore:

```text
conditional_bound = retained
promoted_bound    = UNKNOWN
```

## Constructive boundary counterexample

The subset condition is not bookkeeping trivia.

Suppose a historical report labels an observed value `U0 = 12`, but a later target definition includes additional facilities so that the true historical target under the new definition would be `T0 = 14`.

With:

```text
T1 = 30
r  = 2
```

a naive calculation gives:

```text
2 * 30 / 12 = 5.0
```

but the true target-consistent growth would be:

```text
2 * 30 / 14 ~= 4.286
```

The supposed lower bound is now **above** the true value. It is not a lower bound at all.

So this implication:

```text
same company name
+ same metric label
-> safe historical superset
```

is false.

## Result

DCRE-049 separates two authorities:

### Mathematical authority

The subset-bound theorem is exact.

### Empirical authority

Applying the theorem to Google remains uncertified until the population/subset and metric-lineage obligations are discharged.

This allows Market Microcosm to preserve real mathematical information without laundering an unresolved reporting boundary into an empirical fact.

## Evidence context

Google's 2025 Environmental Report decomposes 2024 electricity into:

```text
data centers                  30,825,600 MWh
offices and other facilities   1,354,300 MWh
total                         32,179,900 MWh
```

and describes the reporting boundary for selected environmental metrics using Alphabet's operational-control approach across owned and leased data centers, offices, and other assets.

Earlier report vintages give 2019 total electricity of 12,237,200 MWh, but DCRE-048 found a 2020 cross-vintage drift, so lineage cannot be inferred from label continuity alone.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = CROSS_SCOPE_BOUND_THEOREM_AND_CERTIFICATE_ONLY
```

No real-world compute-growth bound or elasticity is promoted.

## Next falsifier

DCRE-050 should search for a direct 2019 data-center electricity value under a source lineage compatible with the 2025 report. Figure 2 in the 2025 report visually contains a 2019–2024 data-center electricity trajectory, but DCRE must not silently digitize a chart. The next task is to determine whether the exact underlying 2019 value is disclosed elsewhere in an official table, assurance schedule, downloadable dataset, or machine-readable source. If not, `EXACT_2019_DC_DENOMINATOR = UNOBSERVED` becomes the promoted result.
