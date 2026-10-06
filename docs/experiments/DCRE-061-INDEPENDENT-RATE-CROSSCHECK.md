# DCRE-061 — Independent residential-rate cross-check without causal upgrade

## Trigger

DCRE-060 separates favorable outcome claims from causal effectiveness. One of the utility’s recurring public claims is that residential rates remain low while data-center load has expanded.

DCRE-061 asks whether that particular outcome can be independently verified from a public source outside the utility’s own narrative.

## Independent public data

U.S. Energy Information Administration 2024 annual retail-price tables report:

```text
Northern Wasco County PUD residential average price = 7.72 cents/kWh
Oregon residential average price                    = 14.70 cents/kWh
```

Primary sources:

- EIA, 2024 Utility Bundled Retail Sales — Residential
  - https://www.eia.gov/electricity/sales_revenue_price/pdf/table_6.pdf
- EIA, 2024 Total Electric Industry — Average Retail Price
  - https://www.eia.gov/electricity/sales_revenue_price/pdf/table_4.pdf

The ratio is:

```text
7.72 / 14.70 ~= 0.525
```

or approximately:

```text
47.5% below the Oregon residential average
```

for the same 2024 annual-average price concept.

## What this upgrades

DCRE-060 held the low-rate outcome as source-reported and not independently checked.

DCRE-061 upgrades **only that outcome observation**:

```text
independent_low_rate_outcome_verified = TRUE
```

This is a real empirical gain.

## What this does not upgrade

The EIA table does not establish that the data-center governance bundle caused the low price.

Possible confounders include, among others:

- wholesale power portfolio;
- hydroelectric resource access;
- historical capital structure;
- customer mix;
- taxes and public-utility governance;
- load density;
- transmission arrangements;
- unrelated operational choices.

No matched counterfactual is identified here.

Therefore:

```text
mechanism_caused_low_rate       = UNKNOWN
causal_effectiveness_identified = FALSE
```

## Empirical ladder after DCRE-061

```text
Level 1: governance mechanism exists                    PASS
Level 2: favorable outcome claim coexists               PASS
Level 3: one favorable outcome independently verified   PASS
Level 4: governance caused outcome                      NOT IDENTIFIED
```

This is exactly the kind of asymmetric evidence state DCRE’s empirical chapter is intended to preserve.

## Claim ceiling

```text
claim_ceiling = INDEPENDENT_RATE_OUTCOME_CROSSCHECK_ONLY
authority_effect = NONE
```

No policy effectiveness, welfare effect, counterfactual savings, or optimal tariff claim is inferred.

## Next falsifier

DCRE-062 should seek an independently reported reliability outcome—such as SAIDI/SAIFI or outage duration—from EIA/Form-861-derived official data and compare it with an appropriate benchmark. The same rule applies: independent outcome verification may rise while causal attribution remains blocked.
