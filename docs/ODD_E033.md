# ODD addendum — E033 upstream KPI / downstream value attenuation

## Purpose

Attack another success proxy: local funnel KPI attainment.

Leaner publishes two useful examples where upstream target achievement substantially exceeded downstream target achievement.

## Empirical observations

A retrospective example reports:

```text
appointment KPI attainment = 150%
order KGI attainment       = 20%
```

The downstream/upstream target-attainment ratio is about 0.133.

A later organizational example reports:

```text
lead acquisition target attainment = 300%
order target attainment            = 80%
```

The corresponding ratio is about 0.267.

These observations do not say that appointments or leads are bad metrics. They show that an upstream metric can look excellent while downstream value remains below target.

## Finite ranking-reversal witness

E033 compares two synthetic funnel policies.

The volume optimizer creates more upstream opportunities but has weak qualification, close, and customer-success rates.

The quality optimizer creates fewer upstream opportunities but converts them into far more successful customers.

Ranking by upstream opportunity count selects a different winner from ranking by successful customer outcomes.

## Model consequence

Future empirical demand state should separate at least:

- lead/opportunity volume;
- qualification;
- order/conversion;
- activation;
- customer success / retained value.

An upstream metric can trigger investigation. It cannot certify downstream value.

## Promotion rule

`upstream-kpi-cannot-certify-downstream-value-v1`

## Limitation

The Leaner observations are company/team narratives, not controlled causal experiments. E033 promotes a measurement-identity guard rather than universal funnel coefficients.
