# Generated research dashboard

> Generated from E011/E012/E013/E014/E015/E016/E017 report JSON by `scripts/render_research_dashboard.py`.
> Do not hand-edit this file.

## E011 — pressure resilience

![E011 pressure resilience](e011-pressure.svg)

| Mechanism | Survival AUC | Preliminary knee |
| --- | ---: | ---: |
| platform-heavy | 0.364 | 4 |
| balanced | 0.355 | 4 |
| light-floor | 0.282 | 3 |
| diversity-heavy | 0.273 | 3 |
| usage-only | 0.273 | 3 |
| creator-heavy | 0.268 | 3 |

## E012 — evaluator meta-improvement

![E012 evaluator meta-improvement](e012-evaluator.svg)

| Evaluation curriculum | Mechanism selected |
| --- | --- |
| neutral-only | balanced |
| mild-curriculum | platform-heavy |
| boundary-curriculum | platform-heavy |

**Outer winner:** mild-curriculum → platform-heavy

## E013 — one-dimensional pressure decomposition

![E013 pressure decomposition](e013-decomposition.svg)

| Axis | usage-only | light-floor | balanced | diversity-heavy | creator-heavy | platform-heavy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Price ↓ | 8 | 8 | 7 | 6 | 7 | 7 |
| Platform cost ↑ | 9 | 10 | 10 | 10 | 6 | 10+ |
| Churn ↑ | 6 | 6 | 6 | 6 | 6 | 6 |

Composite E011 knees were 3–4, while the earliest E013 single-axis knee is 6. That gap is evidence of interaction inside the declared synthetic world.

## E014 — pairwise interaction surfaces

![E014 pairwise interaction frontiers](e014-interactions.svg)

| Mechanism | Price × Cost | Price × Churn | Cost × Churn |
| --- | ---: | ---: | ---: |
| usage-only | 4+5★ · 10 | 0+6 · 4 | 0+6 · 6 |
| light-floor | 4+5★ · 10 | 0+6 · 6 | 0+6 · 6 |
| balanced | 4+5★ · 9 | 0+6 · 15 | 0+6 · 6 |
| diversity-heavy | 6+0 · 5 | 3+3★ · 15 | 0+6 · 6 |
| creator-heavy | 2+4★ · 17 | 0+6 · 15 | 3+3★ · 14 |
| platform-heavy | 6+6★ · 1 | 0+6 · 10 | 0+6 · 0 |

Each cell is `frontier level_a+level_b · interaction-only cell count`. ★ means the first failing frontier itself is interaction-only.

**Total interaction-only cells:** 155

## E015 — adaptive boundary sampling

![E015 adaptive boundary sampling](e015-sampling.svg)

| Metric | Exhaustive | Adaptive |
| --- | ---: | ---: |
| Pair-surface queries | 882 | 205 |
| Mean queries / surface | 49.0 | 11.39 |

- Query savings: **76.8%**
- Cell classification accuracy: **100%**
- Exact frontier recovery: **100%**
- Monotonicity violations: **0**
- Promotion: **PASS**

## E016 — generation-scoped adaptive guard

![E016 adaptive guard](e016-guard.svg)

| Guard case | Decision |
| --- | --- |
| Same generation fingerprint | **adaptive** |
| Horizon 60 → 61 | **exhaustive** |
| Hidden non-monotone island | naive accuracy **97.96%** |
| Exhaustive audit | **23 violations detected** |
| Post-audit mode | **exhaustive** |

Guard contract: **PASS**.

## E017 — certificate lifecycle and audit cadence

![E017 certificate lifecycle](e017-lifecycle.svg)

| Schedule | Queries | Savings vs always exhaustive |
| --- | ---: | ---: |
| Always exhaustive | 10584 | 0% |
| Stable generation | 5168 | 51.2% |
| Drift at epoch 5 | 5845 | 44.8% |

- Stable schedule: **8 adaptive / 4 exhaustive epochs**
- Failed audit: **REVOKED → exhaustive**
- Skipped audit through hard expiry: **EXPIRED → exhaustive**
- Lifecycle contract: **PASS**

These are model-relative synthetic results. They are not real-market recommendations.
