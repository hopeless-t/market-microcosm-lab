# Experiments

## E000 — exact finite reference world

Purpose: verify the laboratory machinery against an exhaustively enumerable market.

Key property: the robust viability kernel is computed exactly as a greatest fixed point. The Oracle can therefore identify actions that keep every declared disturbance successor inside the kernel.

E000 is a checksum for future approximate algorithms.

## E010 — ecological subscription market

Purpose: close the first economically meaningful cycle.

The model includes:

- mainstream and niche users;
- subscription revenue;
- platform cash and operating cost;
- publisher cash and cost;
- developer cash and production cost;
- content quality and catalog availability;
- usage-proportional payout;
- survival floors;
- ecosystem diversity funds;
- endogenous entry and exit;
- utility-sensitive churn/acquisition.

Every step checks cash conservation against explicit external sources and sinks.

## Evidence split

Every experiment should distinguish:

1. discovery evidence;
2. promotion evidence;
3. meta-evaluation evidence;
4. neutral reporting evidence when useful.

Do not tune on the same scenarios used for certification.


## E011 — pressure knee

Neutral E010 scenarios were too easy: every initial mechanism survived. E011 therefore raises pressure by lowering subscription revenue while increasing platform cost and baseline churn.

Preliminary knees in the current synthetic world:

- balanced: 4
- platform-heavy: 4
- usage-only: 3
- light-floor: 3
- diversity-heavy: 3
- creator-heavy: 3

Failure biopsy shows distinct collapse modes rather than one universal failure mechanism.

## E012 — evaluator meta-improvement

Three evaluation curricula compete:

- neutral-only;
- mild-curriculum (mild stress);
- boundary-curriculum (boundary stress).

Each curriculum selects a mechanism. The selected mechanisms are then evaluated on a separate, longer, unseen stress holdout.

Current result: mild-curriculum evaluation wins the outer comparison and selects platform-heavy. The result demonstrates that the laboratory can improve how it tests policies, not only the policies themselves.


## E013 — pressure decomposition

E013 splits the E011 composite stress into three independent interventions: subscription-price pressure, platform-cost pressure, and churn pressure.

Current preliminary knee matrix:

- price: usage-only 8, light-floor 8, balanced 7, diversity-heavy 6, creator-heavy 7, platform-heavy 7;
- platform cost: usage-only 9, light-floor 10, balanced 10, diversity-heavy 10, creator-heavy 6, platform-heavy no knee through level 10;
- churn: all six mechanisms reach a knee at level 6.

Failure modes also separate: churn primarily removes the user population, platform cost attacks platform solvency, and price pressure can propagate into publisher/catalog/service-quality failure.

The most important comparison is E011 vs E013: joint pressure collapses at levels 3–4 while no single axis collapses before 6. The next experiment should therefore map interaction surfaces rather than continue one-dimensional escalation.


## E014 — pairwise interaction surfaces

E014 recombines the E013 axes two at a time on 7×7 grids.

An interaction-only cell means the pair is below 90% survival while each matched single-axis intervention is still at or above 90%.

The current run found 155 interaction-only cells across all pair/mechanism surfaces.

Important frontiers include creator-heavy price × cost at 2+4, diversity-heavy price × churn at 3+3, creator-heavy cost × churn at 3+3, and balanced/light-floor/usage-only price × cost at 4+5.

Failure biopsy shows that pair identity matters: price × cost tends to attack platform solvency, while price × churn can attack service quality. Platform-heavy had no interaction-only cost × churn cells in the tested range.

The exhaustive E014 surfaces now act as an oracle for the next meta experiment: recover the same boundary with fewer evaluations.


## E015 — adaptive boundary sampling

E015 uses exhaustive E014 as a verifier and asks whether the same 18 pairwise boundaries can be reconstructed with fewer expensive pair-cell evaluations.

The promoted monotone staircase sampler reduced the query count from 882 to 205 (76.8% savings) while preserving 100% cell classification, 18/18 first-frontier recovery, and exact interaction-only counts. The current E014 surfaces had zero monotonicity violations.

This does not replace exhaustive verification. The promoted architecture is two-plane: adaptive sampling for exploration and periodic exhaustive sampling for certification/audit. A world or evaluator generation change should invalidate the monotonicity certificate and force re-certification.


## E016 — adaptive guard and certificate revocation

E016 attacks the E015 optimization rather than assuming its premise stays true.

A certificate is bound to the exact structural/evaluation generation. Changing only the horizon from 60 to 61 changes the fingerprint and automatically requires exhaustive mode.

The adversarial surface inserts a hidden survival island at creator-heavy Price × Cost (6,6). The naive staircase does not query that cell and drops to 97.96% classification accuracy, while the first frontier remains unchanged. Exhaustive audit detects 23 monotonicity violations and revokes adaptive authorization.

The lesson is explicit: frontier agreement alone is not enough, and sparse adaptive sampling cannot certify its own global monotonicity assumption.


## E017 — certificate lifecycle and audit cadence

E017 converts E016 revocation into an operational lifecycle over deterministic evidence epochs.

The default certificate policy requires exhaustive audit every 3 epochs and hard-expires after 6 epochs without a successful audit.

Across 12 stable epochs, always-exhaustive evaluation would cost 10,584 pair-surface queries. The lifecycle uses 5,168 queries, a 51.2% reduction, with exhaustive issuance/audits at epochs 0, 3, 6, and 9.

When the generation changes at epoch 5, that epoch is exhaustive recertification. The drift schedule still saves 44.8%.

A failed audit remains REVOKED/exhaustive; skipped audits eventually become EXPIRED/exhaustive. Evidence age therefore removes adaptive authority rather than relaxing verification.


## E018 — audit portfolio scheduling

E018 extends E017 from one certificate lifecycle to many certificates competing for bounded authoritative-audit budget.

An exhaustive subset enumerator is the small-world oracle. The promoted bounded-DP scheduler matches the exact optimum on all 48 generated 8-certificate portfolios while reducing scheduler search work from 12,288 to 1,558 units (87.3%).

A plausible value-per-cost greedy scheduler matches the oracle only 79.2% of the time. The fixed A/B/C trap yields value 160 for greedy and 220 for exact/DP.

If mandatory audits alone exceed the budget, the scheduler marks the portfolio infeasible and fails closed rather than silently dropping an authority requirement.


## E019 — durable certificate provenance ledger

E019 stores certificate events in an append-only SHA-256 hash chain and replays certificate authority from history.

The clean eight-event chain and its independent checkpoint both pass, ending ACTIVE/adaptive on the recertified generation.

Payload mutation, deletion, and reorder attacks break internal chain verification. A stronger full-history rewrite can recompute every downstream hash and still pass internal verification; in the fixed attack the forged final state becomes REVOKED/exhaustive.

The previously anchored checkpoint detects the forged head hash. Therefore the mutable ledger cannot be its own final source of provenance authority.


## E020 — checkpoint rotation and anchor continuity

E020 rotates external provenance checkpoints across a 10-event ledger at event counts 2, 4, 6, and 8.

Honest rotation and the independently pinned sequence-1 checkpoint verify. Checkpoint deletion, reorder, and fork attacks are detected.

A rewritten old ledger prefix plus a forged latest-only checkpoint is self-consistent and passes weak latest-only verification. The same rewritten ledger fails verification when continuity to the older pinned checkpoint is required.

The final two ledger events remain explicitly unanchored, making the boundary between externally fixed history and recent mutable history visible rather than implicit.


## E021 — multi-witness checkpoint quorum

E021 distributes checkpoint authority across five synthetic witnesses with a 3-of-5 acceptance threshold.

Exact enumeration shows all 10 three-witness quorums intersect pairwise: across 45 quorum pairs the minimum intersection is one and there are zero disjoint pairs. The weaker 2-of-5 threshold has 15 disjoint quorum pairs.

One or two compromised witnesses cannot forge a checkpoint quorum; three define the compromise boundary.

The fixed split-view experiment gives valid conflicting quorums to witness sets {0,1,2} and {2,3,4}. Both verify, but witness 2 signed both hashes, leaving explicit equivocation evidence when attestations are retained.


## E022 — correlated witness failure domains

E022 tests the E021 3-of-5 quorum after grouping witnesses into correlated failure domains.

The concentrated 3-1-1 topology needs only one compromised domain to forge a quorum. Balanced 2-2-1 needs two domains. Fully separated 1-1-1-1-1 needs three.

At the declared synthetic 10% independent domain-event probability, exact enumeration gives forge probabilities of 10.0%, 2.8%, and 0.856% respectively.

The result makes failure-domain independence a separate trust property from witness identity count. Domain labels themselves remain hypotheses until supported by external dependency evidence.


## E023 — hidden common-mode dependency adversary

E023 keeps the nominal E022 fully separated witness labels but adds an undeclared shared-KMS dependency affecting witnesses 0, 1, and 2.

The nominal model needs three independent shocks and has exact synthetic forge probability 0.000985% at p=1%. The hidden-dependency model needs one shock and reaches 1.000975%, a 1016.16× inflation.

The experiment treats declared failure-domain independence as a hypothesis that can be falsified by a latent dependency hyperedge.
