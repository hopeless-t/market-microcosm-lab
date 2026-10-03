---
layout: default
title: Experiments
---

{% include nav.html %}

# Experiments

The experiment series deliberately grows from exactly checkable toy worlds toward richer market ecology.

## E000 — Exact finite universe

**Purpose:** verify the research machinery itself.

The state/action graph is small enough to enumerate. The robust viability kernel is computed exactly, giving later approximate algorithms a known-answer calibration target.

**Key role:** mathematical checksum.

[Read the E000 ODD](ODD_E000.md)

---

## E010 — Circulating ecological market

**Purpose:** close the first economically meaningful loop.

Users pay subscription revenue; the platform allocates a creator pool; publishers and developers survive or exit; catalog quality affects utility; utility affects churn and acquisition; the next period begins from the resulting population and reserves.

**Important negative result:** all six initial mechanisms survived every neutral 60-month reporting scenario. The neutral benchmark was therefore too easy.

[Read the E010 ODD](ODD_E010.md)

---

## E011 — Pressure knee + failure biopsy

**Purpose:** expose the viability boundary hidden by the neutral world.

Composite pressure lowers subscription revenue while increasing platform cost and baseline churn.

Current preliminary knees:

| Mechanism | Knee |
| --- | ---: |
| balanced | 4 |
| platform-heavy | 4 |
| usage-only | 3 |
| light-floor | 3 |
| diversity-heavy | 3 |
| creator-heavy | 3 |

Failure modes differ. Some mechanisms exhaust platform reserves; others preserve the platform but lose publishers or service quality.

**Key role:** turn collapse from an outlier into evidence.

[Read the E011 ODD](ODD_E011.md)

---

## E012 — Evaluator meta-improvement

**Purpose:** improve the way mechanisms are selected.

Three curricula compete:

- neutral-only;
- mild-curriculum (mild stress);
- boundary stress.

Each curriculum selects a mechanism, then the selected mechanisms compete on a shared unseen, longer-horizon stress holdout.

Current result: the **mild-curriculum** design generalized best and selected platform-heavy.

**Key role:** improve the self-improvement loop itself.

[Read the E012 ODD](ODD_E012.md)

---

## E013 — One-dimensional pressure decomposition

**Purpose:** determine which component of E011's composite pressure is sufficient to trigger each collapse mode.

Price, platform operating cost, and baseline churn are swept independently while the other two remain at baseline.

Current knee matrix:

| Axis | usage-only | light-floor | balanced | diversity-heavy | creator-heavy | platform-heavy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Price ↓ | 8 | 8 | 7 | 6 | 7 | 7 |
| Platform cost ↑ | 9 | 10 | 10 | 10 | 6 | 10+ |
| Churn ↑ | 6 | 6 | 6 | 6 | 6 | 6 |

The key comparison is that E011's joint pressure collapsed at levels 3–4, well before any single E013 axis. This makes stress interaction the next research target.

[Read the E013 ODD](ODD_E013.md)

---

## What comes next

Map two-dimensional interaction surfaces around the E013 knees before introducing richer recommendation, pricing, bargaining, and causal-attribution controllers.

See the [Roadmap on GitHub](https://github.com/hopeless-t/market-microcosm-lab/blob/main/ROADMAP.md).
