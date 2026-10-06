# DCRE-046 — Output observability near-miss

## Trigger

DCRE-045 found that LBNL server-stock and server-electricity histories can share geography, equipment scope, and time while still failing causal identification.

The next question is whether a public hyperscaler reports a genuinely closer activity/output measure.

Google provides a useful near-miss.

## Primary evidence

Google Sustainability reports that in 2024 data-center electricity consumption increased 27% year over year while data-center energy emissions fell 12%.

It also reports that Google data centers deliver **over six times more computing power per unit of electricity than five years earlier**.

Sources:

- `https://sustainability.google/commitments/carbon/`
- `https://sustainability.google/reports/google-2025-environmental-report/`
- `https://cloud.google.com/ai-infrastructure`

The 2025 Environmental Report exposes a data-center electricity series for 2020–2024. The compute-per-electricity statement is an endpoint-relative claim corresponding to approximately 2019→2024, but Google does not publish a reproducible annual compute-power index or enough methodological detail to reconstruct that metric externally.

## What improved relative to DCRE-045

This candidate is much closer to an output measure than equipment stock:

```text
server count        -> hardware stock proxy
computing power     -> activity/capability-side measure
```

And the compute-efficiency and electricity evidence refer to the same Google data-center fleet at a high level.

## Why absolute output growth still cannot be reconstructed

### 1. Baseline-period mismatch

```text
compute-per-electricity relative claim: ~2019 -> 2024
data-center electricity table:          2020 -> 2024
```

Without a matched 2019 data-center electricity value under the same reporting boundary, direct multiplication does not produce a reproducible five-year output-growth factor.

### 2. The compute metric is not externally reproducible

The public claim does not expose a raw annual index, workload mix, normalization method, hardware weighting, or service-output definition.

Therefore:

```text
"6x compute per electricity"
!= public compute-output time series
```

### 3. Efficiency contains electricity in its denominator

The compute-efficiency metric is not an independent demand observation. It is useful for reconstructing output only when paired with boundary-aligned electricity data and a reproducible metric definition.

## Contract

```text
scope_aligned                 = TRUE
period_aligned                = FALSE
compute_definition_reproducible = FALSE
public_compute_index_series   = FALSE
absolute_output_reconstructible = FALSE
candidate_output_growth       = UNKNOWN
candidate_eta                 = UNKNOWN
```

## Important upgrade in epistemic state

DCRE-046 does **not** classify the public evidence as useless.

Instead it promotes a new state:

```text
POINT_IDENTIFICATION = BLOCKED
PARTIAL_IDENTIFICATION = CANDIDATE
```

The next experiment may ask whether public upper/lower bounds can constrain output growth without inventing a point estimate.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = EMPIRICAL_OUTPUT_OBSERVABILITY_AUDIT_ONLY
```

No causal rebound coefficient or elasticity is estimated here.

## Next falsifier

DCRE-047 should attempt a conservative partial-identification bound. A possible path is to use a same-boundary upper bound on 2019 data-center electricity together with the >6x compute-per-electricity endpoint ratio and 2024 data-center electricity. If the assumptions cannot be made explicit and source-compatible, the bound must fail closed.
