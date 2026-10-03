---
layout: default
title: Market Microcosm Lab
---

# Market Microcosm Lab

**A self-improving research laboratory for sustainable market ecosystems.**

The project studies pooled-revenue markets as miniature ecosystems: users, developers, publishers, content, and platforms exchange value over time, and a locally profitable rule can still destroy the long-run system that generated the profit.

## North Star

Find allocation and governance rules that keep essential actors viable while preserving user value, service quality, diversity, innovation, and entry under uncertainty and shocks.

## The laboratory has two loops

### Ecosystem improvement loop

Observation → challenger generation → shadow simulation → untouched holdout → independent verification → promotion/rejection → repeat.

### Meta-improvement loop

The lab also changes **how it improves**: observation granularity, search width, simulation budget, horizon, estimators, and stress generation can themselves compete under an outer holdout.

The evaluator that certifies a proposal is deliberately separated from the optimizer that proposed it.

## Experiments

### E000 — exact finite universe

A tiny market with an exhaustively enumerable state/action graph. It computes an exact robust viability kernel and acts as the laboratory's mathematical checksum.

[ODD model description](ODD_E000.md) · [Architecture](ARCHITECTURE.md)

### E010 — ecological subscription market

A larger synthetic cycle with users, platform revenue, creator pools, publishers, developers, content availability, user utility, churn/acquisition, entry, and exit.

Mechanisms include usage-only allocation, survival floors, ecosystem funds, and different platform/creator splits.

[ODD model description](ODD_E010.md) · [Research protocol](RESEARCH_PROTOCOL.md)

### E011 — pressure-knee and failure biopsy

The neutral world did not expose survival differences, so E011 progressively lowers revenue while raising operating cost and churn. It records each mechanism's preliminary collapse knee and retains concrete failure trajectories instead of discarding them as outliers.

[ODD addendum](ODD_E011.md)

### E012 — meta-improvement of the evaluator

E012 makes the test curriculum itself a candidate: neutral-only, mild-stress, and boundary-stress evaluation designs each select a mechanism, then compete on a common unseen stress holdout.

In the current synthetic world, mild-stress evaluation generalized best while using less search than the widest curriculum.

[ODD addendum](ODD_E012.md)

## Trust boundary

The project explicitly distinguishes:

- **World truth** — complete simulator state;
- **Operational truth** — what a deployable Governor may observe;
- **Certification truth** — evidence independently accepted by the Verifier.

The Oracle is a benchmark, not a hidden information channel to the Governor.

## What this project does not claim

E010 is not an empirical model of Netflix, Game Pass, SARTRAS, Spotify, or any other named service. Synthetic experiments are used to discover structural questions and failure modes. Real-world calibration and causal claims require separate evidence.

## Core documents

- [Architecture](ARCHITECTURE.md)
- [Mathematical model](MATHEMATICAL_MODEL.md)
- [Validation](VALIDATION.md)
- [Meta-loop](META_LOOP.md)
- [Threats to validity](THREATS_TO_VALIDITY.md)
- [GitHub setup](GITHUB_SETUP.md)

**Visualization is not evidence. Simulation output is not truth. Promotion requires independent evidence.**
