---
layout: default
title: Research Contract
---

{% include nav.html %}

# Research Contract

Market Microcosm Lab is designed around one rule:

> **A candidate does not become evidence merely because it improved a score.**

## Promotion requirements

A promoted result should be:

- replayable;
- invariant-preserving;
- evaluated on evidence not used to discover it;
- isolated from Oracle-only state;
- explicit about protected quantities;
- explicit about failure cases;
- explicit about assumptions and falsification conditions.

## Three truth levels

### World truth
The simulator's complete latent state.

### Operational truth
What a deployable Governor is allowed to observe.

### Certification truth
Persisted evidence accepted by the independent Verifier.

Collapsing these levels creates a self-certifying system and invalidates the experiment.

## Root of Trust

The same-generation constitution protects:

- accounting conservation;
- causality;
- Oracle isolation;
- reproducibility;
- independent promotion;
- held-out isolation;
- constitutional versioning.

[Read the Root of Trust on GitHub](https://github.com/hopeless-t/market-microcosm-lab/blob/main/spec/ROOT_OF_TRUST.md)

## Interpretation discipline

Synthetic worlds can reveal structural failure modes and generate hypotheses. They do not by themselves estimate a real market or justify a real-world policy.

**Visualization is not evidence. Simulation output is not truth. Promotion requires independent evidence.**
