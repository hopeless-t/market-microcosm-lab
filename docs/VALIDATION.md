# Validation and independent checking

The model must be checkable by mechanisms that are not identical to the mechanism that produced the result.

## Verification ladder

### 1. Conservation and state invariants
Every transfer is represented as a ledger movement. Money cannot appear or disappear except through explicitly modelled external sources/sinks. Population/content creation and removal must use declared transitions.

### 2. Exact small-world oracle
Maintain a tiny finite ecosystem in which states/actions can be exhaustively enumerated. Exact dynamic programming or exhaustive rollout provides a gold reference for:
- viability membership;
- optimal/near-optimal interventions;
- exact Shapley values when contribution allocation is studied;
- boundary cases.

Approximate large-world algorithms must first reproduce the small-world answers within tolerance.

### 3. Deterministic replay
A run is identified by model version, policy version, scenario, seed, configuration and code revision. Re-running the manifest must reproduce the trajectory or an explicitly versioned stochastic tolerance.

### 4. Property-based testing
Generate many valid and adversarial states and check invariants independent of individual examples.

### 5. Differential testing
Keep a slow, obvious reference implementation and compare it to optimized/vectorized implementations.

### 6. Held-out worlds
Separate discovery seeds/scenarios from promotion seeds/scenarios. Add adversarial shocks and structural parameter shifts that candidate generation never sees.

### 7. Statistical uncertainty
Report distributions and confidence/credible intervals, not only point estimates. Rare collapse events receive explicit upper bounds.

### 8. Empirical calibration and external validity
When real data is introduced, separate calibration targets from validation targets and document identification limits. Reproducing stylized facts is evidence, not proof that the causal mechanism is correct.

## Anti-self-deception rules

- Optimizer and verifier are separate modules.
- Oracle-only state is tagged and blocked from deployable-policy inputs.
- Candidate code cannot alter its own promotion thresholds during the same evaluation.
- A changed verifier/root contract creates a new evaluation generation and forces re-evaluation of incumbent and challenger.
- Failed scenarios are retained, not discarded.
- All promoted decisions carry provenance and a replay manifest.

## Model documentation

Each model version should maintain an ODD-style description: purpose, entities/state/scales, scheduling, design concepts, initialization, input data, and submodels. This makes reimplementation and review part of the model lifecycle rather than an afterthought.


## Adaptive evaluator certification

E015 adds an optimized boundary-search path, but optimization does not weaken the verifier.

A promoted adaptive sampler must be checked against an exhaustive reference generation for:

- monotonicity of the declared fail/survive surface;
- exact full-surface classification;
- exact first-frontier recovery;
- exact derived interaction-only counts;
- declared minimum cost reduction.

The certificate is generation-scoped. Any change to the world transition function, pressure mapping, viability definition, stochastic evaluation contract, or relevant evaluator semantics invalidates the certificate.

When certification is absent or a monotonicity violation is observed, the system fails closed to the exhaustive evaluator. Exhaustive evaluation therefore remains a permanent audit path rather than being removed after optimization.


## Revocation and adversarial guard

E016 validates the negative path of evaluator optimization.

Two independent conditions force exhaustive mode:

1. **generation mismatch** — the certificate fingerprint does not match the current world/evaluator/contract generation;
2. **audit failure** — exhaustive verification observes a structural premise violation such as non-monotonicity.

The adversarial E016 probe is intentionally chosen so that the naive adaptive sampler misclassifies a hidden cell while preserving the same first frontier. This prevents frontier agreement from being mistaken for proof of full-surface correctness.

Certification must therefore be revocable, generation-scoped, and backed by an audit path that is strictly more informative than the optimized evaluator it certifies.


## Evidence-age lifecycle validation

E017 adds time-like evidence aging without using wall-clock time. Integer evidence epochs keep replay deterministic.

The default lifecycle has two thresholds:

- audit due after 3 epochs since the last successful authoritative audit;
- hard expiry after 6 epochs without a successful authoritative audit.

At audit due, the required mode is exhaustive. At hard expiry, adaptive authority is absent. A failed audit sets REVOKED and remains exhaustive on later epochs.

The generation fingerprint now includes the Root of Trust. A constitutional change therefore invalidates existing optimized-evaluator certificates and forces re-certification under the new evaluation generation.


## Audit portfolio exact-oracle validation

E018 introduces a budget scheduler for multiple authoritative audits.

Before promotion, the candidate scheduler is compared to exhaustive subset enumeration on a deterministic finite suite. Exact agreement includes selected certificate set, total restoration value, total cost, and feasibility.

A separate greedy counterexample is retained permanently so that locally attractive value-per-cost scheduling cannot regress into the authoritative path.

Mandatory audits are hard constraints. If mandatory audit cost exceeds available budget, the only valid result is infeasible/fail-closed; partial satisfaction cannot be reported as a successful optimized schedule.


## Provenance-chain and anchor validation

E019 validates certificate/audit provenance at two separate layers.

Internal hash-chain validation checks contiguous indexes, previous-hash linkage, and recomputed event hashes. This detects direct payload mutation, deletion, and event reordering.

A stronger adversarial rewrite changes historical meaning and then recomputes every downstream hash. Such a chain can remain internally valid. Internal consistency is therefore not sufficient evidence that history is authentic.

The independent checkpoint fixes the accepted event count, head hash, final certificate state, and evaluation generation. The E019 full-rehash attack changes the replayed state while preserving internal chain validity, but fails the checkpoint through a head-hash mismatch.

Root of Trust R9 therefore requires provenance to be anchored outside the mutable history it authenticates. Checkpoint mismatch is a fail-closed condition.


## Checkpoint rotation validation

E020 validates long-lived external provenance anchors.

A rotation is valid only when checkpoint sequence is contiguous, each checkpoint links to the previous checkpoint hash, anchored event counts increase, each checkpoint matches the exact ledger prefix it claims, and any required pinned historical checkpoint remains present at the expected sequence.

The test suite retains a deliberate latest-only weakness: rewriting an old ledger prefix, recomputing all ledger hashes, and minting a new checkpoint over the rewritten head can pass verification if only that latest checkpoint is considered.

Pinned historical continuity rejects the same rewritten ledger because an older anchored prefix no longer matches. Checkpoint deletion, reorder, and multiple children of the same parent are also rejected or surfaced as forks.

Root of Trust R10 therefore makes anchor rotation an extension of prior trust rather than replacement of prior trust.


## Witness quorum validation

E021 validates a synthetic 3-of-5 checkpoint witness threshold.

All exact-size quorum subsets are enumerated. For five witnesses, every pair of 3-of-5 quorums intersects in at least one witness, while 2-of-5 admits disjoint quorum pairs. This makes quorum intersection an experimentally checked property rather than an assumed slogan.

The compromise boundary is also explicit: one or two compromised witness keys cannot satisfy the threshold for a forged checkpoint; three can.

A fixed split-view attack gives two conflicting checkpoint hashes valid 3-of-5 attestations. Both views verify independently, but the quorum intersection witness signs both hashes. Retained attestations therefore expose a concrete equivocation record.

The current HMAC witnesses are a deterministic research model. Real use requires independent failure domains, protected keys, authenticated publication, and durable attestation retention.
