# Changelog

## Unreleased

### Presentation and research UX

- deterministic live research dashboard generated from E011/E012/E013/E014/E015/E016/E017/E018/E019/E020/E021/E022/E023 JSON;
- CI freshness check for visual result surfaces and Actions job summary;
- dashboard page and social-preview artwork source;

- product-style README hero and status badges;
- GitHub Pages research dashboard;
- contribution and governance guides;
- research-hypothesis and failure-biopsy issue forms;
- evidence-oriented pull request template;
- citation metadata.

### Research

- E013 one-dimensional decomposition of subscription-price, platform-cost, and churn pressure;
- axis-specific knee matrix and failure biopsy;
- interaction hypothesis from the gap between E011 composite knees (3–4) and E013 single-axis knees (6+);
- E014 exhaustive pairwise interaction surfaces;
- 155 interaction-only cells and frontier failure biopsy;
- survival-loss super-additivity metrics for pairwise stress;
- E015 monotone staircase boundary sampler promoted against exhaustive E014;
- pair-surface query cost reduced from 882 to 205 (76.8%) with exact cell/frontier recovery;
- adaptive-exploration / exhaustive-audit trust separation;
- E016 generation-scoped certificate fingerprint;
- fail-closed fallback on generation mismatch;
- adversarial hidden survival island demonstrating 97.96% naive accuracy despite unchanged frontier;
- exhaustive audit detection of 23 monotonicity violations and adaptive revocation;
- E017 certificate lifecycle with periodic audit, hard expiry, renewal, and revocation;
- stable 12-epoch verification cost reduced from 10,584 to 5,168 queries (51.2%);
- drift-at-epoch-5 schedule retains 44.8% savings while forcing immediate exhaustive recertification;
- Root of Trust R8 adds evidence-bounded optimization authority;
- Root of Trust is now included in optimized-evaluator generation fingerprints;
- E018 exact audit-portfolio oracle and bounded-DP scheduler;
- 48/48 generated portfolio exact recovery with 87.3% less scheduler search work;
- explicit greedy audit-allocation counterexample (160 vs exact 220);
- mandatory-audit over-budget portfolios fail closed;
- E019 append-only certificate provenance ledger with deterministic replay;
- direct payload mutation, deletion, and reorder attacks detected internally;
- full history rewrite + downstream rehash shown to defeat internal-only chain validation;
- independent checkpoint detects fully rehashed rewrite through head-hash mismatch;
- Root of Trust R9 requires externally anchored provenance;
- E020 rotating checkpoint chain over a 10-event ledger with 8-event anchored prefix;
- latest-only rewritten-history forgery shown to pass weak verification;
- pinned checkpoint continuity rejects the same rewritten prefix;
- checkpoint deletion, reorder, and fork detection;
- Root of Trust R10 requires anchor continuity across rotation;
- E021 synthetic 3-of-5 checkpoint witness quorum;
- exact enumeration of 10 quorum sets / 45 quorum pairs with zero disjoint 3-of-5 pairs;
- 2-of-5 counterexample exposes 15 disjoint quorum pairs;
- explicit forge boundary at three compromised witnesses;
- conflicting accepted views retain witness equivocation evidence;
- Root of Trust R11 requires explicit witness quorum integrity;
- E022 correlated witness failure-domain model;
- exact domain-subset enumeration for 3-1-1, 2-2-1, and 1-1-1-1-1 witness placement;
- minimum domains to forge measured as 1, 2, and 3 respectively;
- modeled p=10% domain-event forge probabilities 10.0%, 2.8%, and 0.856%;
- independent placement reduces modeled forge probability 91.44% vs concentrated;
- Root of Trust R12 separates witness identity count from failure-domain independence;
- E023 hidden common-mode dependency adversary;
- nominal five-domain witness topology challenged by an undeclared shared-KMS dependency;
- minimum shocks to forge collapse from 3 to 1;
- exact synthetic forge probability inflates from 0.000985% to 1.000975% (1016.16×);
- Root of Trust R13 makes independence claims explicitly falsifiable and generation-changing when common modes are discovered.

## v0.2 — Ecological market dynamics

- E010 circulating synthetic market;
- user utility, churn/acquisition, developers, publishers, content, entry/exit;
- survival floors and ecosystem funds;
- E011 composite pressure-knee scan and collapse biopsy;
- explicit collapse-cause classification and resilience area;
- E012 stress-curriculum meta-improvement of the evaluator;
- Pages and Wiki source documentation;
- RESULTS.md theory update.

## v0.1 — Self-improving kernel

- exact finite reference world;
- robust viability kernel;
- Oracle / Observer / Governor / Verifier separation;
- closed policy-improvement loop;
- closed meta-improvement loop;
- Root of Trust and deterministic run identity;
- executable E000 experiment and CI.
