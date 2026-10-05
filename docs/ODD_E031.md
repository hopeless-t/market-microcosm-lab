# ODD addendum — E031 short-run signal / PMF proxy guard

## Purpose

Test whether locally positive business signals can certify PMF or long-run viability.

E028-E030 showed that failure evidence can invalidate generic exit and churn assumptions. E031 attacks a more subtle success-side proxy: revenue itself.

## Postmortem triangulation

### Srush

Srush's founder describes several misleading positive signals during the pre-PMF period:

- customers were paying;
- some customers were enthusiastic;
- unit prices could be high.

Yet customer attributes were inconsistent, substantial human effort was required, and people sometimes solved the customer's problem instead of the product.

The founder describes an initial PLG SaaS as withdrawn soon after launch and says the company took roughly four years from founding to reach the later repeatable STP/PMF state.

### Leaner

Leaner reports that revenue had eventually begun for the prior product. The company still withdrew it because long-run customer success and company scalability looked inadequate.

### SalesNow

SalesNow's retrospective describes deep customer pain and an operating business, yet management estimated a roughly 2–3 billion JPY ARR ceiling and chose complete withdrawal/pivot because that local success did not satisfy the desired market headroom.

## Finite proxy witness

E031 creates two synthetic candidates.

One has higher current revenue but poor repeatability, customer success, scalability, and market headroom.

The other has lower current revenue but high values on those four viability dimensions.

Ranking by current revenue selects the first candidate; ranking by the product of the four viability dimensions selects the second.

The exact numbers are only a structural witness. The important result is the ranking reversal.

## Promotion consequence

Revenue, ACV, engagement, and enthusiastic users remain useful observations.

They do not independently grant PMF authority.

Future empirical promotion should separately test:

- repeatability / stable target;
- customer success;
- product-delivered value versus continuous human service burden;
- scalability;
- market headroom.

This directly supports the lab's North Star: one-period revenue and engagement are proxies, not the objective.

## Promotion rule

`short-run-positive-signals-cannot-certify-pmf-v1`

## Limitation

The company narratives are retrospective and are not independent causal audits. E031 promotes an evidence requirement, not a universal PMF formula.
