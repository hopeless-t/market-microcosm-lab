# ODD addendum — E034 hidden human-delivery cost

## Purpose

Convert a qualitative false-PMF failure signal into an explicit accounting guard.

Srush's founder describes a misleading state in which unit prices were high but substantial human effort was required and people were solving the customer's problem instead of the product.

The market lab currently represents operating costs, but an empirical SaaS extension also needs to know **what kind of cost delivers the value**.

## Finite ranking-reversal witness

Candidate A:

```text
revenue = 100
software/infra cost = 20
human delivery cost = 70
```

If human delivery is omitted, apparent gross margin is 80%.

Fully loaded margin is only 10%.

Candidate B:

```text
revenue = 80
software/infra cost = 20
human delivery cost = 10
```

Apparent software-only gross margin is 75%, lower than candidate A.

Fully loaded margin is 62.5%, far higher than candidate A.

Therefore:

```text
software-only margin winner
!=
fully-loaded delivery-margin winner
```

## Model consequence

Future empirical SaaS state should distinguish:

- software/infrastructure cost;
- onboarding/implementation labor;
- recurring customer-success/service labor;
- product-delivered value;
- human-delivered value.

Human involvement is not automatically bad. The failure mode appears when recurring human effort is necessary for the product to appear successful while that burden does not scale with the intended market.

## Promotion rule

`fully-loaded-human-delivery-cost-required-v1`

## Limitation

The numerical witness is synthetic. It demonstrates an accounting/ranking failure mode and does not estimate Srush's historical margins.
