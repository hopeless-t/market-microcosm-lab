# Japan capital ecology: intergenerational and geographic retention

## Research question

How can Japan preserve the long-run viability of its economic ecosystem while a large stock of household wealth moves across generations, regions, asset classes, firms, and public institutions?

This is **not** a study of how to maximize local wealth retention or wealthy-household assets. The target is ecosystem viability: preserving the ability of households, firms, regions, public systems, and new entrants to remain functional while capital circulates.

The framing extends the lab's existing pooled-market ecology from platforms to a national/regional economy. In both settings the key object is not one-period efficiency, but whether value continues to circulate through a diverse set of actors without pathological concentration, leakage, or collapse.

## Empirical signal motivating the case study

A 2026 Daiwa Institute of Research report using the 2024 National Survey of Family Income, Consumption and Wealth and tax statistics highlights several useful observations:

- households with financial assets of JPY 100 million or more increased from 1.0% in 2019 to 1.7% in 2024;
- households with JPY 50-100 million increased from 4.2% to 5.2%;
- 58.0% of households in the JPY 100 million-or-more class had a household head aged 65 or older;
- the share aged 55-64 rose from 20.6% to 24.2%, suggesting a large future transition into older wealthy cohorts;
- regional patterns of inheritance-tax incidence and gift-tax incidence are similar enough to motivate, but not prove, a hypothesis that a meaningful fraction of wealth remains in the same or nearby regions after intergenerational transfer.

Primary source:

- Daiwa Institute of Research, **"増える高齢富裕層とその地域分布―高齢富裕層はどこにいるのか、その資産は今後どこへ向かうのか"**, 2026-10-01: https://www.dir.co.jp/report/research/capital-mkt/it/20261001_026101.pdf

The source itself warns that the tax series are proxies. Inheritance-tax incidence describes the deceased person's region and uses a broader taxable-estate concept than financial-asset wealth; gift-tax incidence describes recipients, not necessarily heirs of wealthy households; donors need not be wealthy; and recipients may later move. These observations therefore motivate a latent-flow problem rather than identify a causal transfer matrix.

## Atomic decomposition

Treat the economy as a flow network.

| Object | Candidate state/flow |
| --- | --- |
| Household/cohort | wealth, income, consumption capacity, age, migration propensity |
| Firm | cash flow, ownership, succession state, employment capacity |
| Region | resident wealth stock, tax base, housing stock, business stock, public-service capacity |
| Financial system | deposits, securities, credit, intermediation capacity |
| Public sector | taxes, transfers, services, infrastructure |
| Intergenerational edge | inheritance, gifts, business succession |
| Geographic edge | migration, property purchase/sale, firm relocation, investment destination |
| Asset-class edge | cash -> securities -> housing -> business equity -> consumption |
| Leakage | capital leaving an actor class or region without replacing viability-critical capacity |
| Retention | value remaining inside a viable circulation loop |
| Shock | mortality wave, asset-price change, interest rates, inflation, migration, tax-rule change |

## Minimal model

Let \(W_{r,a,t}\) be private wealth held in region \(r\), age/cohort class \(a\), at time \(t\).

Let \(M_{ij}\) be the fraction of transferable wealth originating in region \(j\) that arrives in region \(i\) after inheritance/gifting and related migration effects.

A first-order transition is

\[
\mathbf W_{t+1}=M_t\mathbf W_t + \mathbf R_t + \mathbf I_t - \mathbf C_t - \mathbf T_t,
\]

where \(R\) is investment/asset return, \(I\) is new income or inward capital, \(C\) is consumption/outward use, and \(T\) is taxes and other sinks. Each term should later be decomposed by actor class and asset type.

A simple geographic retention statistic is

\[
\rho_{local}=\frac{\sum_r M_{rr}}{\sum_{i,j} M_{ij}}.
\]

However, high \(\rho_{local}\) is not automatically good. It may also encode exclusion, housing inflation, incumbent capture, or lack of mobility. The lab should optimize **viability**, not retention itself.

## Hidden object: the interregional transfer matrix

The available public statistics mostly expose marginals or proxies rather than direct origin-destination flows. The central empirical object is therefore the latent matrix

\[
P(destination=i\mid source=j).
\]

Candidate reconstruction methods:

1. maximum-entropy / iterative proportional fitting under observed marginals;
2. Bayesian partial pooling across regions and age cohorts;
3. optimal-transport bounds rather than a single point estimate;
4. sensitivity analysis over migration, housing, donor-recipient relation, and asset-mix assumptions;
5. explicit non-identifiability intervals when multiple transfer matrices explain the same marginals.

The model must preserve a strict distinction between **observed marginals**, **assumptions**, and **inferred flows**.

## Falsifiable hypotheses

### H1 — Geographic capital retention

Intergenerational transfers have meaningful diagonal or near-diagonal mass: recipients are more likely than a population baseline to remain in the same or neighboring economic region as the source household.

**Reject or weaken H1 if:** plausible transfer matrices consistent with the observed marginals do not require excess local retention, or direct microdata show substantial long-distance transfer/migration.

### H2 — Capital-attractor feedback

Some regions exhibit a reinforcing loop:

\[
wealth \uparrow \rightarrow local\ transfer/investment \uparrow
\rightarrow asset/business capacity \uparrow \rightarrow wealth \uparrow.
\]

**Reject or weaken H2 if:** regional wealth growth is better explained by exogenous income, national asset-price exposure, or migration with no persistent local reinvestment channel.

### H3 — Capital-drain feedback

Regions with outward migration of heirs may experience a reverse loop in which inherited capital, ownership, and demand move outward faster than locally viable replacements emerge.

**Reject or weaken H3 if:** outward heir migration does not predict losses in business succession, tax base, investment, or service viability after controlling for broader regional trends.

### H4 — Retention has a viability knee

Both very low and very high geographic retention may be harmful. Too little can drain regional capacity; too much can intensify concentration, incumbency, and asset-price lock-in. The viable set may therefore have an interior retention range rather than a monotonic optimum.

**Reject or weaken H4 if:** welfare and viability remain monotonic over credible retention ranges across structurally different worlds.

### H5 — Intergenerational transfer is an ecosystem transition, not only a wealth event

The most consequential effect of aging household wealth may be how ownership, housing, firms, deposits, securities, and local demand are reallocated together, rather than the nominal wealth transfer alone.

**Reject or weaken H5 if:** adding these coupled channels does not materially change predicted viability boundaries relative to a wealth-only model.

## Viability constraints

A Japan-scale microcosm should not use aggregate GDP or aggregate household wealth as the sole objective. Candidate hard or semi-hard constraints include:

- minimum household consumption/financial resilience across income and age classes;
- minimum viable business-entry and business-succession rates;
- minimum regional public-service and fiscal capacity;
- bounded housing unaffordability / asset-price stress;
- bounded concentration of wealth and ownership;
- continued credit/intermediation access for viable entrants;
- labor and population mobility without forcing destructive capital drain;
- preservation of innovation and new-firm entry;
- no accounting violations across transfers, taxes, and asset revaluation.

The lexicographic rule from `NORTH_STAR.md` still applies: no intervention may improve an aggregate score by silently destroying an essential actor class.

## Candidate experiment program

### Phase A — synthetic small world

Build a 3-5 region, 3-cohort economy with households, firms, housing, a public sector, and intergenerational transfer. Use an exact small-world checker to find the robust viability kernel under migration and asset-price shocks.

### Phase B — latent-flow reconstruction

Use public regional wealth/tax/demographic data to generate a **set** of admissible transfer matrices, not one privileged matrix. Run the same mechanism across that ensemble.

### Phase C — retention-pressure surface

Sweep local-retention, migration, housing illiquidity, business-succession, and tax/transfer parameters. Search for viability knees and interaction-only collapse regions using the lab's existing E011-E016 methodology.

### Phase D — policy/mechanism stress tests

Candidate mechanisms should be treated as experimental controls, not recommendations. Examples include regional investment channels, business-succession support, inheritance/gift timing rules, housing-liquidity changes, and fiscal transfers. Each candidate must be tested for distributional effects, gaming, concentration, and cross-region spillovers.

### Phase E — failure biopsy

For every collapse, record the first violated constraint and causal chain, such as:

```text
heir migration
-> ownership / deposits leave region
-> local credit or demand falls
-> firm succession fails
-> employment and fiscal base shrink
-> public-service floor violated
```

or the opposite failure:

```text
excess local retention
-> incumbent wealth compounds
-> housing/business entry costs rise
-> entrant rate collapses
-> concentration floor violated
```

## Connection to the existing lab

The structural analogy to subscription/platform ecosystems is strong:

```text
platform world:
user payment -> pool -> creators/publishers -> content -> user value -> payment

regional economy:
wealth/income -> households/firms/public sector -> investment/services/jobs
-> future income/wealth -> next generation
```

Both systems can look healthy in aggregate while one actor class is being starved. Both can also fail through local optimization: maximizing take rate, wealth retention, tax extraction, asset price, or incumbent survival can reduce the long-run viable region.

The research target is therefore the same:

> Find allocation and governance rules that keep value circulating through a diverse ecosystem while preserving entry, adaptation, and long-run survival under shocks and imperfect observation.

## Threats to validity

- inheritance-tax and gift-tax incidence are imperfect proxies for source/destination wealth flows;
- taxable estates include real assets and liabilities and do not match the report's financial-asset definition of wealthy households;
- asset-price appreciation can create apparent wealth growth without new productive capacity;
- recipient location at tax filing is not necessarily long-run destination;
- high local retention can be caused by housing immobility rather than productive reinvestment;
- region-level aggregation can hide within-region inequality and actor-class collapse;
- policy effects are endogenous and may change migration, valuation, avoidance, and reporting behavior.

No empirical calibration should be promoted as causal evidence unless identification is independently justified.

## Next concrete experiment

A suitable next experiment is a synthetic **Japan Capital Ecology small world** that asks:

> Does a non-monotonic viability frontier emerge when intergenerational geographic retention is jointly varied with heir migration, housing illiquidity, and business succession?

This is deliberately small enough for an exact oracle and directly reuses the lab's pressure-knee, interaction-surface, failure-biopsy, and independent-promotion machinery before any claim is made about the real Japanese economy.
