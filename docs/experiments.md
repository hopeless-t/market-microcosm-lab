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

## E018 — Audit portfolio scheduler

**Purpose:** allocate a limited authoritative-audit budget across multiple optimized evaluator certificates.

E018 uses exhaustive subset enumeration as a small-world oracle and tests a bounded dynamic program plus a greedy value-per-cost heuristic.

Across 48 deterministic 8-certificate portfolios:

- bounded-DP exact match: **100%**;
- bounded-DP work reduction: **87.3%**;
- greedy exact match: **79.2%**.

A fixed counterexample produces **160** under greedy selection versus **220** under the exact oracle / DP. A mandatory-over-budget portfolio fails closed.

[Read the E018 ODD](ODD_E018.md)

---

## E019 — Durable certificate provenance ledger

**Purpose:** make certificate authority history replayable and detect history rewriting.

The reference eight-event ledger verifies internally, matches its out-of-ledger checkpoint, and replays to ACTIVE/adaptive on the recertified generation.

Local payload edits, deletion, and event reordering are rejected by the hash chain.

The stronger adversarial result rewrites history and recomputes every downstream hash. The forged chain remains internally valid and replays to REVOKED/exhaustive, but the previously anchored checkpoint rejects the new head hash.

[Read the E019 ODD](ODD_E019.md)

---

## E020 — Checkpoint rotation and anchor continuity

**Purpose:** rotate external provenance checkpoints without allowing a new checkpoint to erase older trust.

The 10-event reference ledger emits checkpoints at event counts 2, 4, 6, and 8. The final two events remain explicitly unanchored.

Honest rotation and a pinned historical checkpoint verify. Checkpoint deletion, reorder, and fork attacks are detected.

A rewritten old prefix plus a forged latest-only checkpoint passes a weak latest-only verifier. The same rewritten history fails when verification must stay continuous with the previously pinned checkpoint.

[Read the E020 ODD](ODD_E020.md)

---

## E021 — Multi-witness checkpoint quorum

**Purpose:** reduce the single-anchor trust assumption with an exact threshold-witness small world.

Five synthetic witnesses attest to checkpoint hashes. The promoted threshold is 3-of-5.

Exact enumeration finds 10 possible 3-witness quorums and 45 quorum pairs. Every pair intersects in at least one witness and none is disjoint. By contrast, 2-of-5 has 15 disjoint quorum pairs.

Forged checkpoint results are explicit: one or two compromised witnesses cannot reach quorum; three can.

Two conflicting 3-of-5 views can both verify, but because the quorums intersect, retained attestations expose witness-2 signing both checkpoint hashes.

[Read the E021 ODD](ODD_E021.md)

---

## E022 — Failure-domain diversity

**Purpose:** test whether five witness identities actually represent five independent failure domains.

The same 3-of-5 threshold is evaluated under three placements:

- concentrated 3-1-1;
- balanced 2-2-1;
- independent 1-1-1-1-1.

Exact domain-subset enumeration shows minimum domains to forge of **1, 2, and 3** respectively.

At the experiment's illustrative 10% independent per-domain event probability, modeled forge probability is **10.0%, 2.8%, and 0.856%**. Full separation reduces the modeled forge probability by **91.44%** versus the concentrated topology.

[Read the E022 ODD](ODD_E022.md)

---

## E023 — Hidden common-mode dependency adversary

**Purpose:** attack the declared independence of the strongest E022 topology.

The nominal model keeps five separate witness domains and five independent 1% shocks. A hidden shared-KMS shock is then added across witnesses 0, 1, and 2 without changing the nominal labels.

Exact subset enumeration changes the minimum forge shock count from **3 to 1** and exact synthetic forge probability from **0.000985% to 1.000975%**, a **1016.16×** inflation.

The conclusion is structural: domain labels are not evidence of causal independence.

[Read the E023 ODD](ODD_E023.md)

---

## What comes next

Model heterogeneous and overlapping dependency graphs, then add active dependency discovery and common-mode fault injection instead of relying only on declared topology.

See the [Roadmap on GitHub](https://github.com/hopeless-t/market-microcosm-lab/blob/main/ROADMAP.md).


## E024 — Empirical evidence plane

**Question:** can public real-world observations constrain future model calibration without allowing restricted, schema-only, stale, or period-misaligned evidence to gain silent authority?

The experiment registers SARTRAS, Netflix, MovieLens, Game Pass Partner Center, and Spotify evidence classes; exhaustively selects the smallest eligible public source portfolio for the initial target observables; reconciles the SARTRAS FY2022 published accounting; and checks Netflix regional ARM dispersion.

The promotion rule is an evidence-admission rule. It does not promote an empirical causal model.

[Read the E024 ODD](ODD_E024.md)


## E025 — Regional empirical complexity knee

**Question:** what is the smallest regional ARM model family that preserves the admitted Netflix aggregate structure to a 10% maximum-relative-error tolerance?

E025 enumerates every partition of UCAN, EMEA, LATAM, and APAC. Four discovery quarters select model complexity and topology; Q2 2024 is held out. One and two groups remain too coarse, while three groups cross the fidelity knee with `{UCAN}`, `{EMEA}`, and `{LATAM, APAC}`.

A stronger one-quarter-forward test freezes the Q1 2024 centroids and remains below 10% maximum relative error on Q2 2024.

The result is structural compression, not a causal segmentation or a claim that ARM equals posted subscription price.

[Read the E025 ODD](ODD_E025.md)


## E026 — Sampled-observation assumption audit

**Question:** what can the published SARTRAS sample count establish about detection and prevalence when the institution-selection mechanism is not yet identified?

A hypothetical simple-random-sampling reference gives an exact rarity curve: with 35,130 applications and a 1,200-institution sample, 87 carrier institutions cross 95% one-or-more detection.

The meta-loop then removes the unverified random-selection assumption. The same nominal sample size can avoid all 87 carriers under an unconstrained selection mechanism, so sample count alone has a 0% worst-case detection lower bound.

The SRS curve remains a mathematical reference, but the promoted empirical rule requires sampling-design metadata before prevalence or observation-noise inference.

[Read the E026 ODD](ODD_E026.md)


## E027 — Game Pass metric-definition drift guard

**Question:** can official Game Pass membership headlines from 2022 and 2024 authorize a precise growth calculation across the Xbox Live Gold → Game Pass Core transition?

No. The 2022 figure is a lower bound (>25M subscribers), the 2024 figure is a rounded 34M member headline, and a membership-definition event lies between them.

E027 deliberately computes the tempting 36% ratio but marks it illustrative-only. The promoted estimator rule requires compatible metric-definition generations and value semantics before time-series growth gains authority.

[Read the E027 ODD](ODD_E027.md)


## E028 — Japanese negative-evidence corpus

**Question:** which failure mechanisms become visible when Japanese withdrawal, sunset, pivot, pruning, and bankruptcy evidence is admitted alongside surviving subscription systems?

The first corpus includes BBD Initiative, RickCloud, Leaner, SalesNow, and TDB industry context. It adds ten declared failure mechanisms beyond the current synthetic price/cost/end-user-churn stress core and promotes a rule requiring negative evidence for empirical market calibration.

[Read the E028 ODD](ODD_E028.md)

## E029 — Strategic exit before insolvency

**Question:** does an insolvency-only exit rule omit rational withdrawals by still-operating actors?

Yes. The negative-evidence corpus contains multiple strategic exits, and an exact finite reference grid contains positive-cash states where orderly exit/redeployment dominates continued operation.

[Read the E029 ODD](ODD_E029.md)

## E030 — Churn semantics counterexample

**Question:** can higher reported SaaS churn coexist with higher ARR and ARPA?

BBD's published pruning period provides exactly that sign pattern. E030 therefore prevents B2B MRR churn from being silently mapped into end-user demand churn and requires both layer and cause identity.

[Read the E030 ODD](ODD_E030.md)


## E031 — Short-run signal / PMF proxy guard

**Question:** can revenue, high ACV, enthusiastic users, or current sales certify PMF and long-run viability on their own?

Srush, Leaner, and SalesNow provide three distinct counterexamples. E031 adds a finite ranking-reversal witness and promotes a rule requiring separate evidence for repeatability, customer success, product-vs-human delivery burden, scalability, and market headroom.

[Read the E031 ODD](ODD_E031.md)


## E032 — Booked revenue / cash-conversion lag

**Question:** can positive booked margin and healthy demand coexist with liquidity failure before receivables arrive?

Yes. A finite witness fails in month two despite positive booked margin; exact search finds the survival buffer and a lag-aware warning catches the risk at time zero.

[Read the E032 ODD](ODD_E032.md)

## E033 — Upstream KPI / downstream value attenuation

**Question:** can upstream funnel target achievement certify downstream value?

Leaner examples and a finite ranking reversal say no. Lead/appointment volume, qualification, orders, activation, and customer success become separate empirical stages.

[Read the E033 ODD](ODD_E033.md)

## E034 — Hidden human-delivery cost

**Question:** can high ACV and apparent software gross margin hide non-scalable human delivery?

Yes. The fixed witness reverses product ranking after implementation/CS/service labor is included.

[Read the E034 ODD](ODD_E034.md)

## E035 — Negative-evidence early-warning tournament

**Question:** do revenue-only or churn-only health proxies survive the failure mechanisms discovered in E028-E034?

No. They miss or false-alarm reference archetypes. A five-axis multi-signal rule exactly matches the declared finite oracle, earning promotion only as a reference warning representation.

[Read the E035 ODD](ODD_E035.md)


## E036 — Discovery-tuned warning with generated holdout

**Question:** does E035's multi-signal warning survive broad generated scenarios when thresholds are chosen on discovery only?

E036 searches 324 threshold candidates over 500 discovery states, freezes the winner, and evaluates 500 states from an untouched seed. Holdout precision, recall, and F1 remain above 98%; scalar revenue/churn baselines retain severe blind spots.

This is within-generator generalization, not real-world predictive certification.

[Read the E036 ODD](ODD_E036.md)


## E037 — Structural-drift revocation

**Question:** does E036 remain authoritative when the failure law itself changes rather than only the random seed?

No. An interaction-only market-headroom × downstream-success failure drops the frozen E036 warning below its prior recall authority threshold. The old certificate is revoked, and an interaction-aware v2 candidate restores greater than 99% precision and recall on the shifted generation.

[Read the E037 ODD](ODD_E037.md)


## E038 — Real longitudinal component holdout

**Question:** does a component-scoped mechanism survive a real-company quarterly holdout?

Informetis's published Smart Living Standard ARR for 2025-Q1 through Q3 yields a frozen Q4 point prediction near 215.27 million JPY versus a displayed 216. E042 later limits the authority of that point gap to reporting-resolution consistency. The same law fails on other components, so component identity and event annotations remain the durable result.

[Read the E038 ODD](ODD_E038.md)

## E039 — Rolling KPI observation lag

**Question:** can the KPI definition itself delay observation of an abrupt business-state change?

Yes. Informetis ARR uses a trailing six-month average MRR. An abrupt MRR end can leave 50% legacy signal in the reported ARR three months later. Warning lead-time accounting must include the metric measurement window.

[Read the E039 ODD](ODD_E039.md)


## E040 — Rolling KPI current-state non-identifiability

**Question:** does one six-month rolling ARR uniquely determine current MRR?

No. Exact enumeration finds 338 monotone integer MRR paths with the same ARR=60, while current MRR spans 0–5.

[Read the E040 ODD](ODD_E040.md)

## E041 — Minimal observability checkpoint

**Question:** what is the smallest extra state needed to reconstruct the newest MRR from consecutive rolling ARR values?

One outgoing boundary MRR is sufficient. Without it, multiple incoming/outgoing pairs remain compatible; with it, the rolling-sum identity reconstructs newest MRR exactly.

[Read the E041 ODD](ODD_E041.md)


## E042 — Reporting-resolution self-attack

**Question:** can integer-million-JPY chart values support E038's apparent sub-1% point-error claim?

No. Propagating nearest-million display intervals through the same model produces an overlapping prediction/holdout interval. The component model remains consistent with the rounded holdout, but sub-1% precision authority is revoked.

[Read the E042 ODD](ODD_E042.md)

## E043 — Decision-sufficient observability

**Question:** when rounded measurements only identify a hidden-state interval, can that still be enough for a specific decision?

Yes. The reference interval certifies `MRR > 0` while leaving `MRR >= 2` ambiguous. Observability authority becomes predicate-scoped.

[Read the E043 ODD](ODD_E043.md)

## E044 — Robust abstention

**Question:** should a controller force a midpoint decision when the compatible-state interval crosses a threshold?

No. The midpoint has a compatible counterexample. The robust controller returns ABSTAIN until evidence makes every compatible state agree.

[Read the E044 ODD](ODD_E044.md)

## E045 — Predicate-scoped active sensing

**Question:** after ABSTAIN, what extra evidence should be requested?

Search candidate observations by declared collection cost and predicate resolution. The reference chooses cheaper predicate-native evidence over expensive full-state recovery.

[Read the E045 ODD](ODD_E045.md)


## E046 — Authority-constrained active sensing

**Question:** can minimum-cost sensing choose evidence that is not authorized?

Yes. A cheap raw-ledger predicate query wins naive cost search but is inadmissible. Authorization becomes a hard filter before predicate-resolution and cost optimization.

[Read the E046 ODD](ODD_E046.md)

## E047 — Freshness and metric-generation alignment

**Question:** is authorized predicate-resolving evidence enough for a current decision?

No. Stale evidence and old metric generations are rejected before cost optimization. The selected observation must be authorized, resolving, fresh, and generation-aligned.

[Read the E047 ODD](ODD_E047.md)
