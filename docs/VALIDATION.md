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
