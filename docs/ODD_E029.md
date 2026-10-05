# ODD addendum — E029 strategic exit before insolvency

## Purpose

Test a structural assumption exposed by E028: actor exit is not always the terminal consequence of insolvency.

The current E010 ecological market makes active developers and publishers inactive when post-period cash falls below zero. That rule is intentionally simple and remains valid for forced financial failure.

Japanese negative evidence adds a different class: deliberate withdrawal while a service or company is still operating.

## Empirical motivation

Four E028 cases motivate the new action class:

- BBD Initiative withdraws/reorganizes businesses based on data-compounding fit, profitability, and strategic concentration;
- RickCloud has an orderly future sunset and migration plan because the proprietary operating model is difficult to sustain at current pricing under platform substitution;
- Leaner withdrew a product after sales eventually appeared because expected customer success and company scalability were inadequate;
- SalesNow's predecessor portfolio was completely withdrawn/pivoted after management judged the market ceiling too low for the intended scale.

The evidence does not establish that these actors were insolvent at the withdrawal decision. More importantly, insolvency is not required by the stated decision logic.

## Finite structural witness

E029 defines two incremental values:

```text
continue_value
  = expected_monthly_net * planning_horizon

exit_value
  = redeployment_value - sunset_cost
```

The current cash balance is tracked separately.

The full small grid enumerates:

- positive cash: 10, 50, 100;
- monthly net: -20, -10, 0, +10;
- horizon: 3, 6, 12 months;
- redeployment value: 0 or 50;
- sunset cost: 10.

The fixed witness has:

```text
cash = +100
monthly net = -10
horizon = 12
redeployment = 50
sunset cost = 10

continue = -120
exit = +40
```

Strategic exit is optimal before insolvency.

## Model consequence

Future empirical worlds need two distinct transitions:

1. **forced failure** — financial or viability constraints make continued participation impossible;
2. **strategic exit** — the governor deliberately leaves because continuation value is dominated by an orderly exit/redeployment path.

A strategic exit may still reduce catalog diversity or user welfare. Therefore it is not automatically a system-level success.

## Promotion rule

`separate-strategic-exit-from-insolvency-v1`

## Limitation

The finite values are structural witnesses, not estimates of any named company's decision function.
