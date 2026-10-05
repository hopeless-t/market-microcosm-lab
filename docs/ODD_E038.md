# ODD addendum — E038 real longitudinal component holdout

## Purpose

Move one step outside synthetic generators.

Informetis publicly reports quarterly ARR by service family and separately explains that a major rental-business customer service would end in March 2026. New recruitment to the affected service had stopped and tenant move-outs were causing natural subscriber decline.

E038 tests whether preserving component identity and the event annotation yields a useful real quarterly holdout.

## Public quarterly series

From the FY2025 results presentation, ARR in million JPY is:

| Quarter | Total | Smart Living Standard | Smart Living Light | Energy Management |
| --- | ---: | ---: | ---: | ---: |
| 2024-Q4 | 487 | 278 | 56 | 153 |
| 2025-Q1 | 445 | 266 | 54 | 125 |
| 2025-Q2 | 384 | 256 | 44 | 84 |
| 2025-Q3 | 364 | 231 | 48 | 85 |
| 2025-Q4 | 345 | 216 | 65 | 64 |

The company defines ARR as twelve times the average MRR over the six months immediately preceding quarter end.

## Component holdout

For each component, E038 fits a deliberately minimal constant quarterly-retention model on 2025-Q1 through Q3:

```text
retention = sqrt(Q3 / Q1)
Q4_prediction = Q3 * retention
```

For Smart Living Standard:

```text
266 → 256 → 231
retention ≈ 0.931891
predicted Q4 ≈ 215.27
observed Q4 = 216
relative error ≈ 0.34%
```

The same simple law is not universal.

Smart Living Light has a holdout relative error above 20%, and aggregate ARR is less tightly predicted than the Standard component.

This is exactly the desired behavior: an event-linked decay mechanism should remain component-scoped rather than silently becoming a global ARR law.

## Concentration-shock context

The same public materials report:

- total ARR: 487 million JPY at 2024-Q4 → 345 million JPY at 2025-Q4;
- revenue: 982 → 530 million JPY;
- operating income: +49 → -628 million JPY;
- net income: +56 → -721 million JPY.

The company identifies the unexpected ending of the major rental-business relationship as an important contributor to the deterioration, while also describing project timing and other business factors.

E038 records the aggregate shock but does not assign every yen of the decline to one customer.

## Promotion rule

`event-annotated-component-longitudinal-holdout-v1`

## Consequence

A real longitudinal record should carry:

- metric definition;
- component identity;
- event annotations;
- discovery interval;
- untouched holdout interval;
- explicit causal limitations.

Aggregate ARR alone is insufficient when components are under different mechanisms.

## Limitation

This is ex-post validation, not a prospective alarm before public disclosure. The Standard component can include customers other than the ending major account, so the tight decay fit does not identify a customer-specific causal effect.
