# RPE-010 — Hidden common mode in semantic observation health

## Question

RPE-009 introduced group-health guards around atom-level staleness hazards. RPE-010 attacks the next assumption:

> Do distinct observation-channel labels really represent independent failure domains?

## Topology

Five semantic observation channels have distinct declared labels:

- governance;
- economics;
- workflow;
- presentation;
- provenance.

The nominal model assigns each label to a distinct failure domain.

The hidden model reveals that **governance** and **economics** both depend on one undeclared `shared-metadata-registry` source.

A value-first health probe therefore selects the two apparently strongest channels — governance and economics — and mistakenly treats them as independent.

## Synthetic shock model

Each independent failure domain has a declared 1% compromise probability.

A compromised domain can make all health probes depending on it falsely attest healthy.

This is an exact synthetic model, not an estimate of any real service, provider, registry, repository, or data source.

## Results

### Nominal label topology

For governance + economics:

- effective domains: 2;
- minimum domain shocks to forge both healthy: 2;
- exact modeled forge probability: **0.01%**.

### Hidden common mode

The same two labels share one hidden domain:

- effective domains: 1;
- minimum shocks: 1;
- exact modeled forge probability: **1%**.

The modeled probability is therefore inflated **100×** while the visible channel count remains two.

The two channels jointly protect 17 synthetic decision-value units in the fixture.

### Dependency-aware pair

Selecting governance + workflow after exposing the dependency graph restores two effective failure domains:

- minimum shocks: 2;
- exact modeled forge probability: **0.01%**.

## Theory update

RPE-010 reproduces the E022/E023 lesson inside the semantic-observation layer:

```text
distinct channel names
!=
independent evidence
```

The Research Portfolio Ecology stack now needs provenance not only for semantic content, but also for the **failure domains of the mechanisms claiming that the content is fresh**.

## Candidate rule

```text
CERTIFY_SPARSE_SEMANTIC_OBSERVATION
BY EVIDENCED FAILURE DOMAINS
NOT CHANNEL LABELS
```

## Next direction

RPE-011 should stop extending the synthetic ladder temporarily and replay this theory against sampled real hopeless-t history:

- identify repeated semantic sources that fanned out across repositories;
- estimate observed duplicate projection count and review surface;
- recover candidate canonical meanings without silently merging independent hypotheses;
- compare direct fan-out with a retrospective on-demand projection plan;
- preserve provenance back to every original PR/commit.

That would be the first bridge from the RPE synthetic aquarium to the actual 500+ PR research ecosystem.

## Claim ceiling

`EXACT_SYNTHETIC_INDEPENDENT_DOMAIN_MODEL_ONLY_NO_REAL_PROVIDER_OR_SOURCE_INDEPENDENCE_CLAIM`
