---
layout: default
title: Market Microcosm Lab
---

<div class="mm-hero">
  <img src="assets/hero.svg" alt="Market Microcosm Lab ecosystem diagram">
</div>

<div class="mm-kicker">Research system · synthetic evidence · verified loops</div>

# Sustainable markets as living systems

Market Microcosm Lab studies pooled-revenue markets as miniature ecosystems. Users, developers, publishers, content, and platforms exchange value over time, and a locally efficient rule can still destroy the long-run system that generated the value.

<div class="mm-warning">
<strong>Synthetic evidence only.</strong> Current experiments are structural research worlds, not empirical estimates or policy recommendations for a named service.
</div>

## Research dashboard

<div class="mm-grid">
  <div class="mm-card">
    <div class="mm-kicker">E000</div>
    <div class="mm-metric">Exact</div>
    <h3>Finite-world oracle</h3>
    <p>Exhaustive robust viability checks provide a mathematical checksum for the laboratory.</p>
  </div>
  <div class="mm-card">
    <div class="mm-kicker">E010</div>
    <div class="mm-metric">Closed loop</div>
    <h3>Ecological market</h3>
    <p>Revenue, creators, publishers, content, utility, churn, entry, and exit circulate over time.</p>
  </div>
  <div class="mm-card">
    <div class="mm-kicker">E011</div>
    <div class="mm-metric">3 → 4</div>
    <h3>Pressure knees</h3>
    <p>Mechanisms separate only after the neutral world is stressed toward its viability boundary.</p>
  </div>
  <div class="mm-card">
    <div class="mm-kicker">E012</div>
    <div class="mm-metric">Meta</div>
    <h3>Evaluator improvement</h3>
    <p>The laboratory improves how it tests mechanisms, not only the mechanisms themselves.</p>
  </div>
</div>

## North Star

> Discover allocation and governance rules that keep the whole ecosystem inside a robust viability region for as long as possible, under uncertainty, strategic adaptation, shocks, and imperfect observation.

## Research arc

**E000** builds an exact finite universe.  
**E010** closes the economic circulation.  
**E011** finds viability boundaries and captures collapse traces.  
**E012** makes the evaluation curriculum itself an object of meta-improvement.

This produces a repeating research pattern:

```text
neutral saturation
→ pressure search
→ failure biopsy
→ theory update
→ improve the evaluator
→ repeat
```

## Trust boundary

The project explicitly separates **World truth**, **Operational truth**, and **Certification truth**. The Oracle is an exact checker and upper-bound comparator, not hidden information available to deployable policies.

## Core documents

- [Architecture](ARCHITECTURE.md)
- [Mathematical model](MATHEMATICAL_MODEL.md)
- [Validation](VALIDATION.md)
- [Meta-loop](META_LOOP.md)
- [Threats to validity](THREATS_TO_VALIDITY.md)
- [E000 ODD](ODD_E000.md)
- [E010 ODD](ODD_E010.md)
- [E011 ODD](ODD_E011.md)
- [E012 ODD](ODD_E012.md)

## Run locally

```bash
python -m pip install -e ".[dev]"
pytest -q
python scripts/run_e000.py
python scripts/run_e010.py
python scripts/run_e011.py
python scripts/run_e012.py
```

**Visualization is not evidence. Simulation output is not truth. Promotion requires independent evidence.**
