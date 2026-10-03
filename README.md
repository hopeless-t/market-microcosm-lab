# market-microcosm-lab

A research laboratory for **sustainable market microcosms**: closed economic ecosystems in which users, creators/developers, publishers, and platforms must remain viable over long horizons while service quality, diversity, innovation, and entry remain healthy.

The repository is intentionally built as a **self-improving research system**. It contains both a loop that improves ecosystem policy and a separate meta-loop that improves how policy improvement itself is performed.

## North Star

> Discover allocation and governance rules that keep the whole ecosystem inside a robust viability region for as long as possible, under uncertainty, strategic adaptation, shocks, and imperfect observation.

The target is not maximum one-period profit, watch time, play time, or any other single proxy.

## Architecture

The laboratory separates seven roles:

1. **World** — authoritative simulated ecosystem dynamics.
2. **Oracle** — god-view truth used only for exact checking and upper bounds.
3. **Observer** — information a deployable policy is allowed to see.
4. **Governor** — allocation/governance intervention policy.
5. **Experimenter** — counterfactual, Monte Carlo, and stress-test machinery.
6. **Verifier** — independent promotion gate and invariant checker.
7. **Meta-Governor** — improves observer/search/evaluation machinery.

A minimal **Root of Trust** sits outside same-generation self-modification. If that constitution changes, incumbent and challengers must be re-certified under a new generation.

## Two closed loops

### L1: ecosystem self-improvement

Observe → generate challengers → shadow evaluate → held-out verify → promote/reject → repeat until no verified improvement remains.

There are now two executable worlds:

- **E000 exact finite world** — the correctness oracle for the laboratory.
- **E010 ecological market** — a stylized subscription economy with users, developers, publishers, content, entry/exit, survival floors, and ecosystem funds.

### L2: meta self-improvement

Generate alternative improvement systems → run complete L1 instances → evaluate them on a **third, isolated meta-holdout** → select better machinery → mutate machinery → repeat.

Discovery, inner promotion, and outer meta-evaluation use disjoint scenario banks.

## Mathematical anchor: robust viability

For ecosystem state x, action a, uncertain model parameters theta, and disturbance w:

    x[t+1] = F_theta(x[t], a[t], w[t])

The main object is the robust viability kernel: states from which some policy can keep the ecosystem inside all hard survival/integrity constraints under every declared bounded disturbance.

E000 is finite, so its robust viability kernel is computed **exactly by fixed-point enumeration**. Approximate methods introduced at larger scale must continue to reproduce this small-world truth.

## E010: a circulating economic ecosystem

E010 closes the first complete economic cycle:

    users
      -> subscription revenue
      -> platform / creator pool
      -> publishers + developers
      -> content availability
      -> user utility
      -> churn / acquisition
      -> next-period users

Actor cash buffers, costs, exits, and a bounded entrant mechanism are explicit. Internal transfers conserve cash; subscription revenue and entrant capital are explicit external sources; operating and production costs are explicit sinks.

Mechanisms currently include usage-only allocation, survival floors, ecosystem funds, and different platform/creator splits. These are synthetic research mechanisms, not policy recommendations for any named service.

## Current synthetic findings

- E010 neutral baseline: all six initial mechanisms survived all 40 neutral 60-month scenarios. Neutral survival alone was therefore not discriminative.
- E011 pressure knees: balanced and platform-heavy first fell below 90% observed survival at pressure level 4; usage-only, light-floor, diversity-heavy, and creator-heavy did so at level 3.
- E011 resilience area across the tested ladder was highest for platform-heavy, followed closely by balanced.
- Collapse modes differed: several creator-favoring or usage mechanisms eventually exhausted platform reserves, while platform-heavy could preserve the platform but lose publishers and service quality.
- E012 showed evaluator choice matters: neutral-only selected balanced, while stress-aware curricula selected platform-heavy. A mild stress curriculum generalized best on the isolated outer stress holdout while using less search than the wider boundary curriculum.

These are model-relative findings from the declared synthetic world, not recommendations for real services.

## Verification stack

The laboratory does not allow the optimizer to certify itself.

- accounting/state invariants;
- exact finite-world viability oracle;
- deterministic seeded scenarios;
- replay identities;
- discovery / promotion / meta-holdout isolation;
- independent promotion rules;
- Wilson lower confidence bound for ecological survival;
- reference implementations;
- property/differential testing hooks;
- CI-generated experiment artifacts.

See docs/VALIDATION.md, docs/THREATS_TO_VALIDITY.md, and spec/ROOT_OF_TRUST.md.

## Run

Requires Python 3.11+.

    python -m pip install -e ".[dev]"
    pytest -q
    python scripts/run_e000.py
    python scripts/run_e010.py

GitHub Actions runs both experiments and uploads their JSON reports.

## Repository map

- NORTH_STAR.md — research objective and optimization ordering
- spec/ROOT_OF_TRUST.md — minimal constitution
- docs/ARCHITECTURE.md — system planes and trust boundaries
- docs/MATHEMATICAL_MODEL.md — model contracts
- docs/VALIDATION.md — verification ladder
- docs/META_LOOP.md — meta-improvement design
- docs/ODD_E000.md — exact reference world
- docs/ODD_E010.md — ecological market world
- docs/RESEARCH_PROTOCOL.md — promotion/research protocol
- docs/THREATS_TO_VALIDITY.md — known ways the lab can fool itself
- experiments/E000_reference — exact reference experiment
- experiments/E010_ecological_market — circulating market experiment
- wiki — source-of-truth drafts for the optional GitHub Wiki
- ROADMAP.md — staged expansion toward causal allocation and empirical case studies

## Public documentation

The docs directory is GitHub-Pages-ready. After Pages is enabled with **main /docs** as the source, the expected URL is:

    https://hopeless-t.github.io/market-microcosm-lab/

Exact repository settings to apply are documented in docs/GITHUB_SETUP.md.

## Research discipline

A result is not accepted because its score improved. It must remain replayable, satisfy hard invariants, survive untouched evaluation, preserve oracle isolation, and state the assumptions under which it could be falsified.

**Visualization is not evidence. Simulation output is not truth. Promotion requires independent evidence.**
