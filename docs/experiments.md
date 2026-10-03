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

## E014 — Pairwise interaction surfaces

**Purpose:** test whether two matched moderate stresses can cross the viability boundary when neither stress does so alone.

Three 7×7 surfaces are evaluated for every mechanism:

- Price × Platform cost
- Price × Churn
- Platform cost × Churn

The experiment found **155 interaction-only cells** across the tested surfaces.

Notable interaction frontiers include:

- creator-heavy Price × Cost at 2+4;
- diversity-heavy Price × Churn at 3+3;
- creator-heavy Cost × Churn at 3+3;
- usage-only, light-floor, and balanced Price × Cost at 4+5;
- platform-heavy Price × Cost only at 6+6.

The failure channel is not universal: price × cost usually reaches platform insolvency, while price × churn can first destroy service quality.

[Read the E014 ODD](ODD_E014.md)

---

## E015 — Adaptive boundary sampling

**Purpose:** improve the experiment machinery itself without weakening verification.

E015 treats the exhaustive E014 surfaces as verifier truth and tests a monotone staircase boundary sampler.

Current result:

- exhaustive pair-cell queries: **882**;
- adaptive queries: **205**;
- query reduction: **76.8%**;
- all-cell classification: **100%**;
- first-frontier recovery: **18/18**;
- interaction-only counts: **exact**;
- monotonicity violations in the current E014 surfaces: **0**.

The candidate passed every promotion gate. It is promoted for exploratory boundary search, while exhaustive E014 remains the periodic audit/reference path.

[Read the E015 ODD](ODD_E015.md)

---

## E016 — Generation-scoped adaptive guard

**Purpose:** prove that E015's faster evaluator can lose authorization safely.

E016 binds the adaptive certificate to a structural/evaluation generation fingerprint. Changing the horizon from 60 to 61 invalidates the certificate and requires exhaustive mode.

A second adversarial probe inserts a hidden survival island into an unqueried region of creator-heavy Price × Cost. The naive staircase reaches only **97.96% classification accuracy** while still preserving the same first frontier. Exhaustive audit detects **23 monotonicity violations** and revokes adaptive authorization.

[Read the E016 ODD](ODD_E016.md)

---

## E017 — Certificate lifecycle and audit cadence

**Purpose:** decide when expensive exhaustive verification is required without weakening E016's authority boundaries.

The default deterministic policy audits every 3 evidence epochs and hard-expires at 6 epochs without a successful audit.

Current 12-epoch result:

- always exhaustive: **10,584 queries**;
- stable lifecycle: **5,168 queries** (**51.2% savings**);
- generation drift at epoch 5: **5,845 queries** (**44.8% savings**).

Failed audits remain REVOKED/exhaustive, and skipped audits reach EXPIRED/exhaustive at the hard TTL.

[Read the E017 ODD](ODD_E017.md)

---

## What comes next

Extend the certificate scheduler to multiple optimized evaluators, where audit priority depends on evidence age, structural drift, expected failure cost, and verifier budget.

See the [Roadmap on GitHub](https://github.com/hopeless-t/market-microcosm-lab/blob/main/ROADMAP.md).
