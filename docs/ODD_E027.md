# ODD addendum — E027 Game Pass metric-definition drift guard

## Purpose

Use public Game Pass membership headlines as an adversarial test of empirical time-series identity.

Microsoft announced in January 2022 that Game Pass had reached **more than 25 million subscribers**. In September 2023, Xbox Live Gold members automatically became Game Pass Core members. In February 2024, Xbox publicly referred to **34 million Game Pass members**.

The tempting calculation is:

```text
34 / 25 - 1 = 36%
```

E027 asks whether that number is authorized as an empirical growth rate.

## Typed observations

The laboratory records more than a scalar:

```text
(value,
 value semantics,
 date,
 metric label,
 definition generation,
 source)
```

The 2022 value is a strict lower-bound headline, not an exact 25.0 million point estimate.

The 2024 value is a rounded public headline.

A membership-definition event lies between them: Xbox Live Gold members were automatically converted into Game Pass Core members.

## Guard

A precise growth estimator is authorized only when:

1. observations are chronological;
2. both values satisfy the estimator's exact-point semantic contract;
3. both observations belong to the same metric-definition generation.

The two Game Pass headlines fail conditions 2 and 3.

E027 still computes 36% as an **illustrative naive ratio** so the dangerous shortcut remains visible in the evidence bundle, but it is explicitly denied inferential authority.

## Promoted rule

`metric-definition-version-required-for-time-series-growth-v1`

Public availability alone is insufficient. Metric-definition continuity and value semantics are part of empirical identity.

## Why this matters to the market lab

Subscription ecosystems frequently change:

- plan names;
- bundle composition;
- included user populations;
- pricing;
- geography;
- counting rules;
- product tiers.

A self-improving empirical loop that ignores these changes can manufacture apparent growth or decline from taxonomy drift.

The evidence plane must therefore version metric definitions the same way the synthetic plane versions simulator generations.

## Limitation

E027 does not estimate true Game Pass subscriber growth and does not assert the exact population included in every Microsoft headline. The point is precisely that the public values do not establish enough definition continuity for a precise growth estimate.
