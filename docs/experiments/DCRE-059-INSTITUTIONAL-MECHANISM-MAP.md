# DCRE-059 — Real governance mechanisms observed without causal promotion

## Trigger

DCRE-058 pivoted away from an unobservable customer meter and established a system-level empirical fact: Northern Wasco County PUD load grew from 90 MW in 2016 to 277 MW in 2026, with data centers described by the public source as a substantial driver.

The next question is institutional:

> What real mechanisms did the utility put in place to manage large-load growth, and which synthetic market failures do those mechanisms resemble?

## Primary source

Northern Wasco County PUD — Data Center Services:

- https://www.nwascopud.org/about-us/data-center-services/

The utility publicly describes multiple large-load governance mechanisms, including:

- separate cost assignment for new large loads;
- engineering and grid-feasibility studies;
- customer-funded infrastructure upgrades;
- credit, collateral, and service-deposit requirements;
- minimum purchase commitments and take-or-pay provisions;
- separate large-load power procurement;
- continuous-service requirements.

## Projection onto the DCRE synthetic chain

The mapping is interpretive but explicit:

```text
cost assignment
-> cross-subsidy / stranded-asset externality

engineering + grid studies
-> capacity overcommitment / reliability risk

customer-funded infrastructure
-> infrastructure-cost socialization

credit / collateral / deposits
-> provider exit / stranded-asset risk

minimum purchase / take-or-pay
-> capacity commitment / revenue risk

separate power procurement
-> resource-cost cross-subsidy

continuous service requirement
-> reliability obligation
```

These are not claimed to be exact one-to-one causal solutions. They are real institutional mechanisms that address failure modes structurally similar to mechanisms generated in the synthetic experiments.

## Critical authority guard

Observed mechanism existence does **not** imply mechanism effectiveness.

DCRE-059 therefore blocks:

```text
mechanism exists
-> mechanism caused low rates
-> mechanism prevented all cross-subsidy
-> mechanism is optimal policy
```

No untreated counterfactual is observed, and the source is not a randomized or quasi-experimental evaluation.

Machine-readable state:

```text
mechanisms_exist                      = TRUE
causal_effectiveness_identified       = FALSE
counterfactual_without_mechanisms     = UNOBSERVED
policy_recommendation_authorized      = FALSE
authority_effect                      = NONE
```

## Result

DCRE-059 establishes the first direct bridge from the DCRE market-failure taxonomy to a real utility’s governance toolkit.

The empirical claim is narrow:

> A utility experiencing large data-center load growth publicly documents a bundle of cost-allocation, reliability, credit, procurement, and contractual mechanisms that are structurally relevant to the synthetic failure modes.

The stronger claim—whether those mechanisms caused superior outcomes—remains open.

## Claim ceiling

```text
claim_ceiling = INSTITUTIONAL_MECHANISM_OBSERVATION_AND_MAPPING_ONLY
```

No causal policy effectiveness, optimal tariff design, welfare effect, or counterfactual is inferred.

## Next falsifier

DCRE-060 should ask whether any outcome metric coexists with this governance bundle in the public record—residential rates, reliability, cross-subsidy claims, infrastructure cost recovery, or service expansion—and then explicitly test whether co-occurrence can be separated from causality.

The next guard is:

```text
MECHANISM_PLUS_GOOD_OUTCOME != MECHANISM_CAUSED_GOOD_OUTCOME
```
