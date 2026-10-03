# market-microcosm-lab

A research lab for sustainable market microcosms: closed economic ecosystems in which users, creators/developers, publishers, and platforms can remain viable over long horizons while service quality, diversity, innovation, and entry remain healthy.

## North Star

> Discover allocation and governance rules that keep the whole ecosystem inside a robust viability region for as long as possible, under uncertainty, strategic adaptation, shocks, and imperfect observation.

This repository treats subscription and pooled-revenue systems as dynamic ecosystems rather than one-shot allocation problems.

## Core research rule

The lab separates:

1. **World** — ground-truth ecosystem dynamics in simulation.
2. **Observer** — what a deployable controller is allowed to see.
3. **Governor** — interventions and allocation policy.
4. **Experimenter** — counterfactual and Monte Carlo evaluation.
5. **Verifier** — independent invariants, exact small-world checks, replay and statistical gates.
6. **Meta-governor** — improves the improvement loop itself.
7. **Root of Trust** — minimal invariants that a candidate may not rewrite in the same generation that it is being evaluated.

The oracle/god-view exists for benchmarking and verification, not as hidden information available to ordinary policies.

## Status

Bootstrap phase. The first architecture PR defines the control loop, meta-loop, mathematical contracts, validation strategy, and executable reference micro-world.
