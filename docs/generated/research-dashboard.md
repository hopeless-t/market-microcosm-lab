# Generated research dashboard

> Generated from E011/E012/E013 report JSON by `scripts/render_research_dashboard.py`.
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

These are model-relative synthetic results. They are not real-market recommendations.
