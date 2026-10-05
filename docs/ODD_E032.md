# ODD addendum — E032 booked revenue / cash-conversion lag

## Purpose

Attack the assumption that healthy demand and positive booked margin imply near-term liquidity viability.

TDB reports a strong software demand environment alongside high bankruptcy counts. For package-software firms it specifically identifies a structural timing problem: revenue can take time to become cash while labor and other fixed costs continue to rise.

This is broader than SaaS, so E032 uses it as mechanism evidence rather than a SaaS failure-rate estimate.

## Current model gap

E010 currently converts contemporaneous users directly into contemporaneous subscription cash:

```text
external_revenue = total_users * subscription_price
```

That is a valid synthetic simplification, but an empirical extension needs a separate receivables / collection state.

## Fixed liquidity witness

E032 uses:

```text
initial cash = 100
booked revenue / month = 100
cash cost / month = 80
collection lag = 2 months
horizon = 6 months
```

Booked unit margin is positive:

```text
100 - 80 = +20
```

But cash evolves:

```text
month 1: 100 - 80 = 20
month 2:  20 - 80 = -60
```

The actor fails before the first delayed revenue collection can repair liquidity.

After month 2, cumulative booked profit is already +40 while cash is -60.

## Exact liquidity buffer

Integer enumeration finds that the minimum initial cash needed to survive the declared six-month horizon is exactly 160.

The simple booked-margin warning produces no alert at time zero.

A lag-aware liquidity check:

```text
initial_cash < monthly_cash_cost * collection_lag
```

alerts immediately and therefore has two months of lead time in the fixed witness.

## Model consequence

Future empirical worlds must separate:

- demand;
- booked/contracted revenue;
- accounts receivable;
- cash collection;
- immediate payroll/fixed costs;
- liquidity runway.

A positive revenue or accounting-margin signal cannot certify viability when cash obligations arrive before collections.

## Promotion rule

`separate-booked-revenue-from-cash-arrival-v1`

## Limitation

The witness values are synthetic. TDB motivates the mechanism but does not identify a universal SaaS collection lag or required cash buffer.
