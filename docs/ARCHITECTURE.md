# Architecture: closed improvement with an independent truth boundary

## Planes

### 0. Root of Trust
Minimal contracts that cannot be rewritten by a candidate in the generation in which that candidate is evaluated: ledger conservation, legal state transitions, deterministic replay semantics, evaluation split rules, and promotion protocol.

### 1. World
The authoritative simulated ecosystem. It owns ground-truth state and transition dynamics. During a run, a world version is frozen.

### 2. Oracle
Has full simulator state and may compute exact counterfactuals in tractable worlds. It exists only for upper bounds, diagnosis, and verification.

### 3. Observer
Produces the information available to a deployable policy. Observation may be delayed, sampled, noisy, aggregated, or missing.

### 4. Governor
Chooses interventions: payout rules, survival floors, ecosystem funds, recommendation exposure, platform take, prices, grants, or other mechanism parameters.

### 5. Experimenter
Runs shadow counterfactuals, Monte Carlo sweeps, stress tests, ablations, and challenger-vs-incumbent comparisons.

### 6. Verifier / Promotion Gate
Independently checks invariants, held-out performance, uncertainty bounds, replayability, leakage, and robustness. It is not the same module as the optimizer.

### 7. Meta-Governor
Improves the improvement machinery: observation design, search algorithm, horizon, uncertainty sets, candidate generation, and experimental allocation.

## Inner loop

Observe -> diagnose -> propose intervention -> shadow simulate -> verify -> promote/reject -> observe again.

A promoted governor version becomes the incumbent only after the verifier accepts it.

## Meta loop

Measure inner-loop quality -> propose a new observer/search/evaluation configuration -> evaluate it on held-out meta-scenarios -> verify false-promotion/generalization behavior -> promote/reject.

The meta-loop may improve how improvement is performed, but it cannot silently rewrite the Root of Trust that judges the same proposal.

## Why the split matters

A self-improving controller that can also edit its own scoreboard can improve the score without improving the ecosystem. The architecture therefore separates optimizer, world, oracle, and verifier and records versioned provenance for all four.

## Oracle gap

For a deployable policy \(\pi\) and oracle policy \(\pi^*\):

\[
R_{oracle}=J(\pi^*)-J(\pi).
\]

The meta-loop tries to reduce this gap by better observation, modelling, and control rather than by leaking oracle state into the policy.
