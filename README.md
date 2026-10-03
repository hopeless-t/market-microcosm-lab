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

The executable reference implementation is in:

- src/market_microcosm/improvement.py
- src/market_microcosm/verifier.py
- src/market_microcosm/policies.py

### L2: meta self-improvement

Generate alternative improvement systems → run complete L1 instances → evaluate them on a **third, isolated meta-holdout** → select better machinery → mutate machinery → repeat.

The implementation is in:

- src/market_microcosm/meta_improvement.py

The three scenario sets are deliberately distinct:

- discovery scenarios;
- inner promotion holdout;
- outer meta holdout.

## Mathematical anchor: robust viability

For ecosystem state x, action a, uncertain model parameters theta, and disturbance w:

    x[t+1] = F_theta(x[t], a[t], w[t])

The main object is the robust viability kernel: states from which some policy can keep the ecosystem inside all hard survival/integrity constraints under every declared bounded disturbance.

The tiny E000 world is finite, so its robust viability kernel is computed **exactly by fixed-point enumeration**. Approximate methods introduced later must reproduce this small-world truth before being trusted at scale.

## Verification stack

The laboratory does not allow the optimizer to certify itself.

- accounting/state invariants;
- exact finite-world viability oracle;
- deterministic seeded scenarios;
- replay identities;
- discovery/holdout/meta-holdout isolation;
- independent promotion rules;
- reference implementations;
- property/differential testing hooks;
- CI-generated experiment artifacts.

See docs/VALIDATION.md and spec/ROOT_OF_TRUST.md.

## Run E000

Requires Python 3.11+.

    python -m pip install -e ".[dev]"
    pytest -q
    python scripts/run_e000.py

The experiment writes:

    artifacts/e000/meta-report.json

GitHub Actions runs the same experiment and uploads the report as an artifact.

## Current experiment

E000 is intentionally a toy universe: one platform, two developer classes, finite integer reserves, payout actions, and bounded shocks.

It is **not** claimed to model Netflix, Game Pass, SARTRAS, or any real market. Its job is to make the laboratory machinery falsifiable and exactly checkable before realism is introduced.

## Repository map

- NORTH_STAR.md — research objective and optimization ordering
- spec/ROOT_OF_TRUST.md — minimal constitution
- docs/ARCHITECTURE.md — system planes and trust boundaries
- docs/MATHEMATICAL_MODEL.md — model contracts
- docs/VALIDATION.md — verification ladder
- docs/META_LOOP.md — meta-improvement design
- docs/ODD_E000.md — ODD description of the finite reference world
- docs/RESEARCH_PROTOCOL.md — promotion/research protocol
- docs/THREATS_TO_VALIDITY.md — known ways the lab can fool itself
- experiments/E000_reference — reference experiment specification
- ROADMAP.md — staged expansion from exact toy world to empirical case studies

## Research discipline

A result is not accepted because its score improved. It must remain replayable, satisfy hard invariants, survive untouched evaluation, preserve oracle isolation, and state the assumptions under which it could be falsified.

**Visualization is not evidence. Simulation output is not truth. Promotion requires independent evidence.**
