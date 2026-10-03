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
