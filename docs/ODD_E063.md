# ODD addendum — E063 real portfolio-transition KPI sign reversal

## Purpose

Re-anchor the meta-loop in real longitudinal SaaS evidence after the extended synthetic trust/lineage sequence.

E063 uses BBD Initiative's published FY2025 quarterly SaaS KPIs to test a tempting scalar heuristic:

```text
churn improves
=> ARR / portfolio health improves
```

## Published FY2025 series

| Quarter | ARR (JPY m) | Churn | Contracts | ARPA (JPY) |
| --- | ---: | ---: | ---: | ---: |
| Q1 | 1,605 | 1.93% | 3,390 | 473,682 |
| Q2 | 1,640 | 1.76% | 3,358 | 488,431 |
| Q3 | 1,688 | 2.16% | 3,304 | 511,090 |
| Q4 | 1,662 | 1.67% | 3,265 | 509,166 |

The company defines ARR as quarter-end MRR multiplied by 12 and churn as the quarterly average of monthly Churn MRR divided by prior month-end MRR.

## Sign transitions

### Q1 → Q2

```text
churn down
ARR up
ARPA up
contracts down
```

### Q2 → Q3

```text
churn up
ARR up
ARPA up
contracts down
```

### Q3 → Q4

```text
churn down
ARR down
ARPA down
contracts down
```

Therefore the same churn-improvement sign coexists with both ARR growth and ARR decline inside one company-year and one metric-definition generation.

A naive rule that predicts ARR up whenever churn falls and ARR down whenever churn rises is correct in only one of the three transitions.

## Event semantics

The FY2025 Q4 material states that ARR decreased as the planned launch timing of Knowledge Suite+ slipped.

It also states that low-price-plan cancellations continued while ARPA temporarily decreased amid the launch delay and service-withdrawal preparation.

These explanations remain company-reported event annotations, not independently identified causal effects.

## Consequence

Directional KPI signs cannot certify transition health on their own.

A portfolio-transition record should carry:

- KPI values and definitions;
- product launches/delays;
- service withdrawal/preparation;
- pruning/migration state;
- event timing.

## Promotion rule

`portfolio-transition-kpi-direction-requires-event-semantics-v1`

## Limitation

This is one four-quarter company counterexample, not a population-level causal estimate.
