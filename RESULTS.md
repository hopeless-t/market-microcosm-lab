# Current results

Status: synthetic research evidence only. These results describe the declared repository models and seed banks; they are not empirical estimates for a named market.

## E000 — exact self-improvement kernel

The finite reference world continues to pass its exact viability checks and closed inner/meta-loop CI.

A representative v0.2 CI run converged the inner policy loop to reserve-balancer-t1. The outer machinery loop remained capable of changing search configuration.

## E010 — circulating ecological market

Neutral baseline:

- mechanisms: usage-only, light-floor, balanced, diversity-heavy, creator-heavy, platform-heavy;
- horizon: 60 months;
- neutral reporting seeds: 40;
- observed full-horizon survival: 1.0 for every mechanism.

This is an important negative result: the neutral world is too easy to reveal the viability boundary.

The E010 inner loop selected platform-heavy under its declared discovery/promotion design. The meta configuration selected long-compact.

## E011 — pressure knee

Composite pressure simultaneously reduces subscription price, raises platform operating cost, and raises baseline churn.

Preliminary first level with observed survival below 90%:

| Mechanism | Knee |
| --- | ---: |
| balanced | 4 |
| platform-heavy | 4 |
| usage-only | 3 |
| light-floor | 3 |
| diversity-heavy | 3 |
| creator-heavy | 3 |

Normalized survival-area across the tested pressure ladder:

| Mechanism | Survival AUC |
| --- | ---: |
| platform-heavy | 0.364 |
| balanced | 0.355 |
| light-floor | 0.282 |
| diversity-heavy | 0.273 |
| usage-only | 0.273 |
| creator-heavy | 0.268 |

Failure biopsy identified different collapse modes:

- balanced: platform insolvency;
- creator-heavy: platform insolvency;
- light-floor: platform insolvency;
- usage-only: platform insolvency;
- diversity-heavy: service quality below floor;
- platform-heavy: publisher population below floor plus service quality below floor.

This is the first direct evidence inside the model of the intended ecological trade-off: protecting one trophic layer can move failure into another layer.

## E012 — meta-improvement of evaluation design

Design selections:

| Evaluation curriculum | Mechanism selected |
| --- | --- |
| neutral-only | balanced |
| mild-curriculum | platform-heavy |
| boundary-curriculum | platform-heavy |

On the isolated outer stress holdout, mild-curriculum was the winning evaluation design and selected platform-heavy.

The wider boundary curriculum did not earn automatic preference. Search cost is an explicit tie-breaker, so extra evaluation pressure must buy additional generalization to justify itself.

## E013 — one-dimensional pressure decomposition

E013 held two E011 pressure components at baseline while sweeping the third.

Preliminary knees:

| Axis | usage-only | light-floor | balanced | diversity-heavy | creator-heavy | platform-heavy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| subscription price ↓ | 8 | 8 | 7 | 6 | 7 | 7 |
| platform operating cost ↑ | 9 | 10 | 10 | 10 | 6 | >10 |
| baseline churn ↑ | 6 | 6 | 6 | 6 | 6 | 6 |

Failure biopsy separated the mechanisms cleanly:

- churn alone eventually drives **user population below the floor** for every mechanism; diversity-heavy can also cross the service-quality floor;
- platform-cost pressure mostly causes **platform insolvency**; creator-heavy is especially fragile at level 6, while platform-heavy showed no knee through level 10;
- price pressure propagates through both sides of the ecosystem: some mechanisms end in platform insolvency, while balanced/diversity-heavy can lose service quality and platform-heavy can lose publishers plus service quality.

The strongest result is comparative: E011's composite pressure produced knees at levels 3–4, but no E013 single axis produced a knee before level 6. Inside the declared synthetic world, simultaneous moderate stresses therefore interact to advance collapse substantially.

## E014 — pairwise pressure interactions

E014 evaluated three 7×7 pairwise surfaces for every mechanism:

- subscription price × platform cost;
- subscription price × churn;
- platform cost × churn.

A cell is **interaction-only** when the pair falls below 90% survival while both matched single-axis interventions remain at or above 90%.

Across all 882 evaluated pair/mechanism cells, **155 were interaction-only**.

Selected first failing frontiers:

| Mechanism | Price × Cost | Price × Churn | Cost × Churn |
| --- | ---: | ---: | ---: |
| usage-only | 4+5 ★ | 0+6 | 0+6 |
| light-floor | 4+5 ★ | 0+6 | 0+6 |
| balanced | 4+5 ★ | 0+6 | 0+6 |
| diversity-heavy | 6+0 | 3+3 ★ | 0+6 |
| creator-heavy | 2+4 ★ | 0+6 | 3+3 ★ |
| platform-heavy | 6+6 ★ | 0+6 | 0+6 |

★ marks a frontier where the pair itself is interaction-only.

The corresponding interaction-only cell counts were especially large for creator-heavy (17 on price × cost, 15 on price × churn, 14 on cost × churn) and diversity-heavy on price × churn (15).

Frontier failure biopsy showed distinct channels:

- price × cost interaction frontiers primarily fail through **platform insolvency**;
- price × churn can create **service-quality collapse** even when matched single axes survive, as seen for diversity-heavy at 3+3;
- cost × churn exposes creator-heavy platform insolvency at 3+3;
- platform-heavy is unusually resistant to cost × churn interaction in the tested region, with zero interaction-only cells there.

The strongest strict metric also reached its maximum: for many mechanism/pair surfaces, observed pair survival loss exceeded the sum of matched single-axis survival losses by as much as 1.0 in the tested grid.

## E015 — adaptive boundary sampling

E015 treats the exhaustive E014 surfaces as verifier truth and benchmarks a monotone staircase sampler as a candidate improvement to the experiment machinery.

Aggregate result:

| Metric | Exhaustive | Adaptive |
| --- | ---: | ---: |
| Pair-surface queries | 882 | 205 |
| Mean queries per surface | 49.00 | 11.39 |
| Cell classification accuracy | 100% | 100% |
| Exact frontier recovery | 100% | 100% |
| Monotonicity violations | — | 0 |

The candidate reduced pair-surface query cost by **76.8%** while exactly recovering all 882 survival/failure classifications, all 18 first frontiers, and all interaction-only counts.

All five promotion gates passed, so monotone-staircase-boundary-sampler-v1 is promoted for exploratory boundary search.

The trust boundary remains asymmetric:

- adaptive sampling is the cheaper exploratory path;
- exhaustive E014 remains the periodic audit/reference path;
- any future monotonicity violation must fail closed or trigger exhaustive fallback.

## E016 — generation-scoped adaptive guard

E016 tests whether the promoted E015 optimization safely loses authority when its premises no longer hold.

The same-generation certificate fingerprint authorizes the adaptive path. Changing only the evaluation horizon from 60 to 61 changes the generation fingerprint and automatically forces **exhaustive** mode.

The adversarial test then mutates creator-heavy / Price × Cost at cell (6,6) from failure to survival, creating a hidden non-monotone island that the staircase does not query directly.

Result:

| Check | Result |
| --- | --- |
| Same generation | adaptive allowed |
| Horizon 60 → 61 | exhaustive fallback |
| Naive adaptive accuracy on adversarial surface | 97.96% |
| Monotonicity violations detected by exhaustive audit | 23 |
| Post-audit mode | exhaustive |
| Guard contract | PASS |

The first frontier happened to remain unchanged in this adversarial case, which is itself useful evidence: exact frontier recovery alone would not have detected the hidden classification error. Full-surface audit therefore remains necessary for certificate renewal.

## E017 — certificate lifecycle and audit cadence

E017 operationalizes E016's revocable authorization as a deterministic evidence-epoch state machine.

Default policy:

- periodic exhaustive audit every 3 evidence epochs;
- hard expiry after 6 epochs without a successful audit;
- adaptive use only while the certificate is ACTIVE.

For a 12-epoch stable generation:

| Schedule | Queries | Savings |
| --- | ---: | ---: |
| Always exhaustive | 10,584 | 0% |
| E017 lifecycle | 5,168 | 51.2% |

The stable lifecycle uses 8 adaptive epochs and 4 exhaustive epochs (initial issuance plus audits at epochs 3, 6, and 9).

With a structural/evaluation generation drift at epoch 5, the old certificate is rejected and epoch 5 becomes exhaustive recertification. Total cost rises to 5,845 queries but still saves **44.8%** versus always exhaustive.

Negative paths remain fail-closed:

- failed exhaustive audit → **REVOKED / exhaustive** on the following epoch;
- no successful audit through epoch 6 → **EXPIRED / exhaustive**.

## E018 — exact audit portfolio scheduling

E018 extends E017 from one certificate over time to multiple certificates competing for a bounded authoritative-audit budget.

A deterministic suite of 48 generated portfolios contains eight certificates each, with integer audit costs, restoration values, and up to two mandatory audits.

Aggregate scheduler result:

| Scheduler | Exact match | Search work |
| --- | ---: | ---: |
| exhaustive subset oracle | 100% | 12,288 |
| bounded-DP | 100% | 1,558 |
| greedy value/cost | 79.2% | heuristic |

The bounded dynamic program reduces search work by **87.3%** while reproducing the exhaustive optimum on every generated portfolio.

The fixed greedy trap makes the failure mode concrete:

- greedy selects A+B for restoration value **160**;
- exact oracle and DP select B+C for **220**.

A separate mandatory-over-budget case is infeasible by construction. Oracle, DP, and greedy all fail closed instead of silently dropping a mandatory authoritative audit.

## E019 — durable certificate provenance ledger

E019 persists certificate authority transitions as an append-only SHA-256 hash chain and replays the resulting authority state.

The reference ledger contains eight events spanning issuance, adaptive use, authoritative audit, generation mismatch, recertification, and renewed adaptive use. Internal chain verification and the external checkpoint both pass, and replay ends **ACTIVE / adaptive** on the recertified generation.

Adversarial result:

| Mutation | Internal chain | External checkpoint |
| --- | --- | --- |
| payload edit without rehash | FAIL | not needed |
| event deletion | FAIL | not needed |
| event reorder | FAIL | not needed |
| full rewrite + downstream rehash | PASS | FAIL / detected |

The strongest test rewrites the final adaptive-use event into a forged REVOKE and recomputes every downstream hash. Internal chain verification still reports a valid chain and replay ends **REVOKED / exhaustive**. The original out-of-ledger checkpoint rejects it through a head-hash mismatch.

This is an important negative result: a hash chain is tamper-evident only relative to an independently trusted anchor. It is not self-authenticating history.

Append-only extension also preserved every prior event hash.

## E020 — checkpoint rotation and anchor continuity

E020 extends E019 from one external checkpoint to a rotating checkpoint chain.

The reference ledger has 10 events. Checkpoints anchor prefixes after event counts 2, 4, 6, and 8, deliberately leaving a two-event unanchored tail.

Reference result:

- honest checkpoint rotation: **PASS**;
- independently pinned checkpoint continuity: **PASS**;
- replay remains **ACTIVE / adaptive**;
- anchored prefix: **8/10 events**;
- unanchored tail: **2 events**.

Adversarial result:

| Attack | Result |
| --- | --- |
| checkpoint deletion | rejected |
| checkpoint reorder | rejected |
| checkpoint fork | detected |
| rewrite old prefix + forge latest-only checkpoint | weak latest-only verifier accepts |
| same rewritten history with pinned rotation | rejected |

The latest-only attack is the important negative result. If the verifier forgets older trusted anchors, a rewritten ledger plus a newly self-consistent checkpoint can look valid. Keeping continuity to a previously pinned checkpoint rejects the same history through a ledger-prefix mismatch.

## E021 — multi-witness checkpoint quorum

E021 distributes checkpoint authority across five synthetic witnesses with a 3-of-5 acceptance threshold.

Exact quorum geometry:

| Threshold | Quorum sets | Quorum pairs | Minimum intersection | Disjoint pairs |
| --- | ---: | ---: | ---: | ---: |
| 3-of-5 | 10 | 45 | 1 | 0 |
| 2-of-5 | 10 | 45 | 0 | 15 |

The 3-of-5 threshold is therefore the smallest strict-majority threshold in this five-witness world that guarantees any two quorums intersect.

Compromise boundary:

- 1 compromised witness → forged checkpoint rejected;
- 2 compromised witnesses → forged checkpoint rejected;
- 3 compromised witnesses → forged checkpoint reaches quorum.

The fixed split-view test produces two individually valid 3-of-5 quorums over conflicting checkpoint hashes:

- view A: witnesses 0, 1, 2;
- view B: witnesses 2, 3, 4.

Both verify, but witness 2 appears in the intersection and has signed both checkpoint hashes. Retained attestations therefore expose explicit equivocation evidence.

The result does not claim 3-of-5 prevents all split views. It shows that quorum intersection converts a successful conflicting-view attack into an attributable witness contradiction unless enough evidence is suppressed.

## Theory update

The working theory after E010–E021 is:

1. neutral survival can saturate and become uninformative;
2. useful allocation comparisons require locating the viability boundary;
3. the location of the knee is not enough — failure time and failure mode also matter;
4. platform and creator protection form a genuine dynamic trade-off in the current model;
5. the evaluation curriculum is itself part of the control system and should be meta-optimized;
6. more stress testing is not monotonically better when a smaller curriculum generalizes equally well;
7. churn pressure is largely mechanism-insensitive once it dominates user population dynamics;
8. platform-cost pressure strongly exposes the platform-take trade-off;
9. revenue pressure can propagate from platform solvency into publisher/catalog/service-quality collapse;
10. the early E011 composite knee is not explained by any single component alone;
11. pairwise interaction-only regions are large rather than rare artifacts in the current synthetic world;
12. the interaction topology depends on the allocation mechanism — creator-heavy is fragile across all three pair surfaces, while platform-heavy is much more resistant to cost × churn;
13. the first failing frontier and the dominant failure mode are separate objects and both matter;
14. full-grid interaction mapping is informative but expensive enough to become a target for meta-improvement;
15. the current E014 failure surfaces are monotone on all 18 tested mechanism/pair surfaces;
16. monotone structure can be exploited without losing classification or frontier fidelity in the current model;
17. adaptive exploration and exhaustive certification should remain separate planes;
18. an optimization certificate must be scoped to the exact structural/evaluation generation that earned it;
19. frontier agreement alone is insufficient evidence of full-surface correctness;
20. adaptive machinery needs an explicit revoke path, not only a promote path;
21. sparse exploration cannot certify its own global structural assumption;
22. verifier cost is itself a schedulable resource, but audit scheduling must be downstream of authority constraints;
23. evidence age should reduce optimization authority before it reduces verifier strictness;
24. structural drift and evidence expiry are distinct invalidation channels and both should force exhaustive mode;
25. scarce audit budget creates a separate combinatorial control problem;
26. locally efficient value-per-cost ordering can be globally suboptimal even when every individual score is correct;
27. exact small-world portfolio oracles can validate faster budget schedulers before deployment;
28. replayable certification history is a separate trust object from the current certificate state;
29. hash-link integrity detects local mutation but cannot detect a fully recomputed rewrite without an independent anchor;
30. provenance authority must therefore be external to the mutable history it authenticates;
31. replacing an anchor is not equivalent to extending trust — rotation must preserve continuity to previously trusted anchors;
32. latest-only verification can forget historical trust and accept a self-consistent rewritten past;
33. anchored and unanchored ledger regions should be explicitly distinguished;
34. checkpoint forks are a first-class provenance conflict rather than a normal alternate history;
35. distributing anchor authority requires a threshold whose quorum geometry is itself verified;
36. strict-majority quorum intersection does not prevent threshold compromise, but it makes conflicting accepted views overlap;
37. retained authenticated attestations can turn that overlap into equivocation evidence;
38. the compromise threshold and availability threshold are explicit parameters, not hidden security assumptions.

Next work should move from in-process synthetic witness keys to a stronger signed/transparency-log model or multiple independent publication channels, then return to richer endogenous recommendation, pricing, and bargaining controllers.
