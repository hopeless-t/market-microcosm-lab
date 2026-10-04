# ODD addendum — E030 churn semantics counterexample

## Purpose

Attack a common empirical shortcut: treating every quantity called "churn" as the same directional health signal.

The synthetic E010/E013 baseline user churn axis represents end-user demand loss and remains a valid declared stress variable.

BBD Initiative's public KPI, however, is MRR churn across a B2B SaaS portfolio and includes deliberate portfolio actions.

## Published counterexample

BBD defines Churn Rate as the three-month quarterly average of monthly Churn MRR divided by prior month-end MRR.

From FY2023 Q4 to FY2024 Q3:

```text
Churn:     1.15%   → 2.33%
ARR:       1,593   → 1,607 million JPY
ARPA:      437,545 → 466,303 JPY
Contracts: 3,641   → 3,416
```

The changes are approximately:

- churn relative change: +102.6%;
- ARR: +0.88%;
- ARPA: +6.57%;
- contracts: -6.18%.

The same official material states that churn increased with unprofitable-service exits and migration from low-price customers toward higher-price plans.

Therefore the observed sign pattern is:

```text
churn ↑
contracts ↓
ARR ↑
ARPA ↑
```

This is impossible to interpret correctly if churn is represented as one generic "ecosystem deterioration" scalar.

## Model consequence

Future empirical SaaS layers must type both **layer** and **cause**.

Layer examples:

- end-user churn;
- account/logo churn;
- MRR churn;
- supplier/content exit.

Cause examples:

- distress or demand loss;
- intentional portfolio pruning;
- plan/segment migration.

The model must not transfer a churn coefficient across layers merely because the metric name is the same.

## Relation to E013

E030 does **not** falsify E013's result that increasing the declared synthetic end-user churn parameter eventually reduces user viability.

It falsifies a broader inference:

```text
"higher metric named churn" => "worse ecosystem state"
```

without layer/cause identity.

## Promotion rule

`churn-must-be-layer-and-cause-typed-v1`

## Limitation

The public data identify the sign counterexample and company-stated mechanisms, not the causal share attributable to each mechanism.
