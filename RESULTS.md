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

## E022 — correlated witness failure domains

E022 tests the E021 3-of-5 quorum under correlated witness placement.

All domain subsets are exhaustively enumerated.

| Witness placement | Min domains to forge | Min domains to break availability | Forge probability at p=10% |
| --- | ---: | ---: | ---: |
| concentrated 3-1-1 | 1 | 1 | 10.000% |
| balanced 2-2-1 | 2 | 2 | 2.800% |
| independent 1-1-1-1-1 | 3 | 3 | 0.856% |

The nominal quorum threshold is identical in all three cases. The effective security boundary is not.

Under the declared homogeneous independent-domain model, the fully separated topology reduces modeled forge probability by **91.44%** relative to 3-1-1 concentration. The availability-loss boundary follows the same 1 → 2 → 3 domain geometry.

The result is not evidence that real providers or regions are independent. It shows why independence must be modeled and evidenced separately from witness identity count.

## E023 — hidden common-mode dependency adversary

E023 attacks the strongest E022 topology without changing its nominal witness-domain labels.

The nominal model contains five independent one-witness shocks at p=1%. The hidden model adds one undeclared shared-KMS shock affecting witnesses 0, 1, and 2.

| Model | Min shocks to forge | Exact forge probability |
| --- | ---: | ---: |
| nominal independent | 3 | 0.000985% |
| hidden shared-KMS | 1 | 1.000975% |

The hidden dependency raises modeled forge probability by **1016.16×** and makes a single latent shock sufficient to satisfy the 3-of-5 quorum.

This is a model-error result rather than a claim about KMS products. It demonstrates that independence cannot be established solely from distinct labels, providers, regions, or witness IDs. The causal dependency graph matters.

## E024 — empirical evidence plane

E024 opens the first empirical-evidence plane while preserving the separation between observation, simulation, and causal certification.

The source registry classifies evidence by access and authority rather than treating every documented dataset as equally observable. The exact public-source portfolio covers the declared initial observables while excluding restricted Game Pass values and request-only Spotify values.

Initial anchors:

| Anchor | Published observation | Model consequence |
| --- | --- | --- |
| SARTRAS FY2022 | tax-exclusive receipt components sum to 4,662,378 thousand JPY; allocation components sum to 4,662,379 thousand JPY | conservation closes to a 1-thousand-JPY published-rounding delta |
| SARTRAS sampling | about 1,200 sampled institutions from 35,130 applications; about 46,600 usage reports and 118,600 works | empirical observation must be modeled separately from world truth |
| Netflix Q2 2024 | regional ARM ranges from USD 7.17 (APAC) to USD 17.17 (UCAN) | one global fixed revenue-per-membership value is rejected for empirical calibration |
| Netflix H2 2025 | 96 billion hours watched from July through December 2025 | period-scoped engagement anchor; cross-period normalization is forbidden by default |
| Game Pass Partner Center | title-month-platform usage/purchase schema is documented | schema adapter is allowed, but partner-only values cannot enter the public calibration portfolio |

The Q2 2024 Netflix ARM max/min ratio is greater than 2.3. ARM is not relabelled as posted subscription price; the result only establishes that an empirical Netflix-like world needs regional revenue heterogeneity.

All E024 promotion gates pass, promoting `empirical-evidence-plane-v1` as an evidence-admission rule, not as a calibrated causal market model.

## E025 — regional empirical complexity knee

E025 uses the admitted Netflix regional ARM source to decide how much regional structure an empirical model needs before building a larger calibrated world.

Every set partition of UCAN, EMEA, LATAM, and APAC is enumerated exactly. Discovery uses Q2 2023 through Q1 2024; Q2 2024 is held out.

At a declared 10% maximum-relative-error tolerance:

| ARM groups | Best discovery worst max-relative error | Status |
| ---: | ---: | --- |
| 1 | >50% | reject |
| 2 | >20% | reject |
| 3 | <9% | admit |
| 4 | 0% | exact but unnecessary |

The minimum admissible complexity is therefore **3 groups**. The exact selected topology is `{UCAN}`, `{EMEA}`, `{LATAM, APAC}`.

For a stronger temporal check, the selected topology is calibrated on Q1 2024 and those centroids are frozen for Q2 2024. The one-quarter-forward holdout remains below the 10% maximum-relative-error threshold.

This is a compression and model-family rejection result, not a causal geographic segmentation claim. ARM remains average revenue per membership rather than posted subscription price.

All E025 gates pass, promoting `regional-arm-complexity-knee-k3-v1`.

## E026 — sampled-observation assumption audit

E026 uses the admitted SARTRAS FY2022 sample counts to test how much observation confidence can be justified from sample size alone.

The empirical anchor contains 35,130 applications and approximately 1,200 sampled institutions. In a **hypothetical simple-random-sampling reference world**, exact without-replacement detection gives:

| Detection target | Minimum carrier institutions | Population fraction |
| ---: | ---: | ---: |
| 50% | 20 | ~0.057% |
| 90% | 67 | ~0.191% |
| 95% | 87 | ~0.248% |
| 99% | 133 | ~0.379% |

A one-per-thousand phenomenon (35 institutions after rounding) is detected only about 70.4% of the time in that SRS reference.

The meta-loop then attacks its own assumption. If the selection mechanism is unconstrained, the same 1,200-institution sample can avoid all 87 carrier institutions, so the worst-case detection lower bound is **0%**. The published sample count therefore cannot, by itself, certify prevalence uncertainty or representativeness.

E026 keeps the SRS calculation as a mathematical reference world but revokes its authority as an empirical calibration. All gates promote `sampling-design-metadata-required-before-prevalence-inference-v1`.

## E027 — Game Pass metric-definition drift guard

E027 tests whether two official public membership headlines automatically form a valid time series.

Microsoft reported **more than 25 million Game Pass subscribers** in January 2022. Xbox later reported **34 million Game Pass members** in February 2024. Between those observations, Xbox Live Gold members were automatically converted to Game Pass Core.

The mechanically tempting calculation is (34 / 25 - 1 = 36\%\). E027 retains that ratio only as an illustrative anti-pattern.

The earlier observation is a strict lower bound rather than an exact 25M point. The later observation is a rounded headline. Most importantly, the two observations are assigned different metric-definition generations because a membership-scope event occurs between them.

The growth-authority guard therefore rejects a precise cross-headline growth calculation and promotes `metric-definition-version-required-for-time-series-growth-v1`.

The empirical identity of a metric now includes value semantics and definition generation, not only numeric value, unit, and date.

## E028 — Japanese negative-evidence corpus

E028 adds a deliberately heterogeneous Japanese failure/withdrawal corpus so empirical calibration cannot learn only from surviving systems.

The initial corpus includes:

- **BBD Initiative** — portfolio pruning with published ARR/churn/ARPA/contract KPIs, plus later restructuring and impairment;
- **RickCloud** — planned sunset under platform substitution and long-run infrastructure/engineering burden;
- **Leaner** — prior product withdrawal after roughly one year without sales and later concern that customers would not succeed and the company would not scale;
- **SalesNow pre-2022 portfolio** — complete pivot after management estimated a roughly 2–3 billion JPY ARR ceiling, despite large advertising spend and multiple upsell products;
- **TDB software-industry context** — 195 bankruptcies through February FY2025, 84.6% under 100 million JPY of debt, plus labor-cost and cash-conversion pressure.

The declared negative-evidence mechanism set adds ten dimensions not represented by the original price/cost/end-user-churn stress core: acquisition burn, cash-conversion lag, customer-success non-scalability, data-compounding misalignment, engineering-maintenance burden, labor-cost pressure, market ceiling, platform substitution, portfolio pruning, and product sprawl.

All E028 gates pass, promoting `negative-evidence-corpus-required-for-market-calibration-v1`.

## E029 — strategic exit before insolvency

E029 tests the E010 simplification that actor exit occurs through negative cash.

The Japanese corpus contains multiple orderly withdrawals whose published decision logic is strategic or structural rather than an explicit insolvency trigger. A finite reference grid then provides a constructive witness:

```text
cash = +100
expected monthly net = -10
horizon = 12
redeployment value = 50
sunset cost = 10

continue value = -120
exit value = +40
```

Strategic exit dominates while cash remains positive.

E029 therefore promotes `separate-strategic-exit-from-insolvency-v1`: forced financial failure remains a state transition, while voluntary exit becomes an explicit governance/control action with migration, sunset, and redeployment consequences.

## E030 — churn semantics counterexample

BBD's published FY2024 Q3 portfolio KPIs provide a real sign counterexample to generic "churn up = system worse" reasoning.

From FY2023 Q4 to FY2024 Q3:

| Metric | Start | End | Change |
| --- | ---: | ---: | ---: |
| Churn | 1.15% | 2.33% | +1.18 pt / +102.6% relative |
| ARR | 1,593m JPY | 1,607m JPY | +0.88% |
| ARPA | 437,545 JPY | 466,303 JPY | +6.57% |
| Contracts | 3,641 | 3,416 | -6.18% |

The same official disclosure attributes higher churn partly to unprofitable-service exits and migration from low-price customers toward higher-price plans.

E030 does not invalidate E013's synthetic **end-user** churn pressure. It rejects untyped transfer across layers. B2B account/logo/MRR churn, end-user churn, supplier exit, intentional pruning, and plan migration require separate identities.

All gates promote `churn-must-be-layer-and-cause-typed-v1`.

## E031 — short-run signal / PMF proxy guard

E031 triangulates three Japanese SaaS/startup postmortems to test whether locally positive signals can certify PMF.

- **Srush** reports paying/high-value/enthusiastic customers during a period that management later characterized as false PMF: customer attributes were inconsistent, human effort was high, and people sometimes solved the problem instead of the product. The founder describes an initial PLG SaaS as withdrawn soon after launch and roughly four years from founding to the later repeatable STP/PMF state.
- **Leaner** reports that revenue eventually existed for the prior product, yet the company still withdrew it because expected customer success and company scalability were inadequate.
- **SalesNow** reports deep customer pain and an operating prior business, but management estimated a roughly 2–3 billion JPY ARR ceiling and chose complete withdrawal/pivot.

A finite reference witness then gives the higher-current-revenue candidate poor repeatability, customer-success, scalability, and market-headroom values, while a lower-current-revenue candidate is strong on all four. Ranking by revenue and ranking by viability select different candidates.

E031 therefore promotes `short-run-positive-signals-cannot-certify-pmf-v1`.

Revenue, ACV, engagement, and enthusiastic users remain observations. Promotion authority requires independent evidence for repeatability, customer success, product-vs-human delivery burden, scalability, and market headroom.

## E032 — booked revenue / cash-conversion lag

TDB's software-industry reports identify a useful failure mechanism: demand can remain strong while package-software firms face a delay between earning revenue and turning it into cash, during which labor and fixed costs continue.

E032 creates a finite witness:

```text
initial cash = 100
booked revenue/month = 100
cash cost/month = 80
collection lag = 2 months
```

Booked margin is +20 per month, yet cash is +20 after month 1 and -60 after month 2. Cumulative booked profit at failure is already +40.

Exact integer search finds the minimum initial cash required to survive the six-month reference horizon is **160**.

A booked-margin warning stays silent at time zero; a lag-aware liquidity guard warns immediately.

All gates promote `separate-booked-revenue-from-cash-arrival-v1`.

## E033 — upstream KPI / downstream value attenuation

Leaner provides two empirical proxy-gap observations:

- historical appointment KPI attainment 150% versus order KGI attainment 20%;
- later lead-acquisition attainment 300% versus order attainment 80%.

The downstream/upstream attainment ratios are roughly 0.133 and 0.267 respectively.

A finite funnel witness then gives the higher-volume policy weak qualification, close, and customer-success rates. The lower-volume policy produces more successful customers, reversing the upstream ranking.

All gates promote `upstream-kpi-cannot-certify-downstream-value-v1`.

## E034 — hidden human-delivery cost

Srush's false-PMF postmortem explicitly identifies high unit price plus substantial human work as a misleading success signal.

E034 constructs:

| Candidate | Apparent software-only GM | Fully-loaded GM |
| --- | ---: | ---: |
| human-heavy high ACV | 80% | 10% |
| product-led lower ACV | 75% | 62.5% |

The software-only winner loses once recurring human delivery cost is included.

All gates promote `fully-loaded-human-delivery-cost-required-v1`.

## E035 — negative-evidence early-warning tournament

E035 compiles E028-E034 into seven exact reference scenarios: healthy scalable, liquidity lag, human-delivery burden, market ceiling, funnel-quality failure, strategic exit, and healthy intentional pruning with elevated churn.

Three warning rules compete:

| Rule | Key failure |
| --- | --- |
| revenue-only | misses positive-growth failure archetypes |
| churn-only | misses non-churn failures and false-alarms on healthy pruning |
| multi-signal | exact match on the declared reference suite |

The promoted warning vector contains:

- cash collection gap;
- fully-loaded delivery margin;
- market headroom;
- downstream funnel success;
- strategic-exit value gap.

The multi-signal rule reaches 100% precision/recall on this **hand-constructed exact reference suite**. This is not production predictive validation; it proves that the empirically motivated failure mechanisms can be compiled into a machine-checkable warning representation.

All gates promote `negative-evidence-multi-signal-early-warning-v1`.

## Theory update

The working theory after E010–E035 is:

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
38. the compromise threshold and availability threshold are explicit parameters, not hidden security assumptions;
39. witness-count diversity and failure-domain diversity are separate quantities;
40. correlated placement can collapse nominal 3-of-5 security to a single-domain failure;
41. minimum domains to forge is a more informative resilience metric than witness count alone;
42. declared independence requires external evidence because topology labels do not prove causal independence;
43. a hidden dependency hyperedge can dominate the nominal failure-domain topology;
44. model misspecification can inflate estimated trust failure by orders of magnitude even when the quorum rule is unchanged;
45. dependency discovery and failure-domain assignment must therefore be separate verification tasks;\n46. empirical observations need a separate admission plane from synthetic and certification evidence;\n47. public schema visibility does not imply public observation visibility;\n48. real regional revenue heterogeneity can invalidate a synthetic single-price assumption before any parameter fitting begins;\n49. period, unit, sampling design, and source authority are part of an empirical value's identity, not optional metadata;\n50. admitted empirical data can select simulator/model-family complexity before full calibration;\n51. for the five-quarter Netflix ARM window, a one-global-parameter or two-group regional family is too coarse at 10% tolerance, while a three-group family crosses the fidelity knee;\n52. structural compression should earn promotion on a temporal holdout rather than on the discovery quarters alone;\n53. sample count alone does not identify an observation model or certify representativeness;\n54. optimistic sampling assumptions should be retained as reference worlds but lose empirical authority when an admissible selection adversary can overturn them;\n55. prevalence inference from sampled market observations requires sampling-frame and weighting metadata, not only n/N;\n56. a public scalar is not a time-series datum until its bound/rounding semantics and metric-definition generation are tracked;\n57. product taxonomy or membership-scope changes can create apparent growth from definition drift;\n58. time-series estimators should fail closed across unbridged metric generations instead of silently normalizing incompatible headlines;
59. success-only empirical calibration is structurally incomplete when withdrawal, sunset, pivot, and bankruptcy evidence expose additional failure mechanisms;
60. actor exit is not synonymous with insolvency: strategic exit can dominate continuation before cash crosses zero;
61. churn direction is not globally monotone across metric layers because deliberate pruning can raise measured churn while ARR and ARPA improve;
62. empirical state variables need layer identity, causal/operational mechanism identity, and exit semantics before entering the simulator;
63. locally positive business signals such as revenue, high ACV, or enthusiastic users can coexist with non-repeatability, human-service burden, poor customer success, low scalability, or insufficient market headroom;
64. PMF is therefore a multi-constraint certification problem rather than a scalar revenue threshold;
65. the empirical meta-loop should attack success proxies with the same adversarial discipline used for failure assumptions;
66. booked revenue and cash arrival are separate state variables, and collection lag can kill a positive-margin actor before receivables arrive;
67. upstream funnel attainment cannot certify downstream orders or customer success;
68. software-only gross margin can materially overstate scalability when recurring human delivery is excluded;
69. early warning should be a vector over empirically distinct failure mechanisms rather than one revenue or churn scalar;
70. exact success on a hand-constructed warning suite is only a compilation check — thresholds still require Monte Carlo stress, holdouts, and real longitudinal validation.

Next work should add a regionalized empirical calibration world and a sampled-observation calibration world while continuing heterogeneous dependency discovery. Stronger signed/transparency publication and endogenous economic controllers remain parallel targets.
