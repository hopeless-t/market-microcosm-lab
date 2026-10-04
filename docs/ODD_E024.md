# ODD addendum — E024 empirical evidence plane

## Purpose

Introduce a separate empirical-evidence plane without collapsing published observations, synthetic worlds, and causal claims into one object.

E024 asks whether public real-world observations can constrain model structure while access restrictions, period mismatch, sampling design, and source authority remain explicit and machine-checkable.

## Evidence classes

The registry distinguishes:

- `public_official`: public observations published by the operating institution;
- `public_academic`: public research data with an explicit academic source;
- `public_archive`: historical public data retained through an archive;
- `restricted_partner`: a documented schema whose observed values require authorization;
- `request_only`: data that require a separate request or approval;
- `exploratory_nonofficial`: useful discovery material that cannot certify an empirical anchor.

A public schema is not a public observation.

## Initial sources

### SARTRAS 2022 management overview

The official management overview publishes both accounting flows and the sampling design used for usage reports.

Tax-exclusive receipts reported in the document:

- primary / secondary education: 2,263,598 thousand JPY;
- higher education: 2,397,753 thousand JPY;
- Article 4 compensation: 1,027 thousand JPY.

Their sum is 4,662,378 thousand JPY.

Published allocations:

- distribution fund: 3,403,744 thousand JPY;
- common-purpose fund: 932,270 thousand JPY;
- administration fee: 326,365 thousand JPY.

Their sum is 4,662,379 thousand JPY. The 1-thousand-JPY difference is within the document's explicit rounding caveat.

The same source reports 35,130 applications, approximately 1,200 sampled institutions, approximately 46,600 usage reports, and approximately 118,600 works in the reports.

This becomes the first real-world conservation and observation-model anchor.

### Netflix H2 2025 engagement

Netflix states that its July–December 2025 engagement report captures 96 billion hours watched. E024 records that period total as a demand/engagement anchor but forbids silently combining it with membership figures from another period.

### Netflix Q2 2024 regional streaming economics

The official shareholder letter reports Q2 2024 ARM of:

- UCAN: USD 17.17;
- EMEA: USD 10.80;
- LATAM: USD 8.28;
- APAC: USD 7.17.

The max/min ratio is greater than 2.3. ARM is average revenue per membership, not a posted subscription price, but the dispersion is sufficient to reject a single global revenue-per-membership value as an empirical calibration assumption.

### Game Pass Partner Center

Microsoft publicly documents Game Pass purchase and usage fields including title, month, platform, unique users, total hours, hours per user, new users, purchase quantity, and estimated revenue.

However, the download page requires authorization. E024 therefore admits the schema as an adapter contract while refusing to treat its partner-specific values as public calibration evidence.

### MovieLens and Spotify

MovieLens 32M provides a public preference-structure benchmark. The Spotify Million Playlist Dataset remains useful as a structural reference, but the current access path is request-based, so it is not admitted into the immediate public-data portfolio.

## Exact source-portfolio oracle

Let the target observable set be:

```text
allocation_accounting
sampling_design
demand_engagement
regional_subscription_economics
preference_structure
catalog_diversity
```

E024 exhaustively enumerates subsets of eligible public sources and selects the smallest portfolio that covers the full target set, with evidence-class cost as the deterministic tie-breaker.

Restricted and request-only sources are ineligible regardless of how useful their schema would be.

## Promotion gates

Promotion requires all of the following:

1. SARTRAS accounting closes within the published rounding tolerance.
2. The exact public portfolio covers every declared target observable.
3. No restricted or request-only values enter that portfolio.
4. Game Pass schema visibility is not confused with observation visibility.
5. Netflix regional ARM dispersion is large enough to invalidate a single global empirical ARM assumption.
6. A period-alignment guard prevents cross-period ratios from being manufactured by default.

## Model consequences

E024 does not calibrate E010 directly. It changes what future calibration is allowed to assume.

The next empirical world should:

- introduce regional subscription economics before fitting a Netflix-like market;
- model sampled observation separately from complete world truth for SARTRAS-like systems;
- keep Game Pass data adapters dormant until authorized values are actually available;
- attach source, period, unit, and access authority to every empirical anchor;
- retain the existing rule that calibration does not imply causal identification.

## Trust boundary

Three evidence planes are now explicit:

- **synthetic evidence** — generated by declared simulator worlds;
- **empirical evidence** — measured values admitted through the source registry;
- **certification evidence** — evidence accepted by the independent verifier.

An empirical observation may constrain a synthetic parameter without becoming proof that the simulator's causal mechanism is true.

## Next experiments

- **E025**: regionalized demand/revenue world constrained by Netflix regional ARM and engagement data.
- **E026**: sampled-observation calibration using the SARTRAS sampling structure.
- Later: activate a Game Pass adapter only if authorized title-level observations are supplied; otherwise keep Game Pass comparisons structural rather than empirical.
