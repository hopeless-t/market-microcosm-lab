# Threats to validity

This document is part of the laboratory, not an appendix. A self-improving simulator is especially vulnerable to producing convincing evidence for its own mistakes.

## 1. Objective capture / Goodhart failure

A Governor may learn to improve a proxy without improving ecosystem health.

Controls:
- hard viability constraints precede scalar welfare;
- protected metrics are not traded away for score;
- multiple welfare dimensions remain visible;
- later experiments must include explicit mechanism-gaming agents.

## 2. Evaluator capture

An optimizer that can rewrite the evaluator can certify itself.

Controls:
- candidate generator and verifier are separate modules;
- Root of Trust is immutable within an evaluation generation;
- constitutional changes require re-certification.

## 3. Oracle leakage

A policy can appear excellent if simulator-only latent state leaks into its inputs.

Controls:
- full world state and ToyObservation are separate types;
- the Oracle is passed only to evaluation for disagreement measurement;
- deployable PolicySpec acts only on observations.

## 4. Scenario overfitting

Repeated optimization on the same random worlds turns the benchmark into training data.

Controls:
- discovery, promotion, and meta-holdout seed sets are disjoint;
- the meta-loop is judged on scenarios unused by every inner loop;
- future work should rotate sealed scenario banks and adversarial generators.

## 5. Model misspecification

Exact optimization of the wrong world is still wrong.

Controls:
- exactness claims apply only to the declared finite world;
- model version and assumptions are explicit;
- empirical calibration and external validation remain separate stages;
- parameter ensembles and structural alternatives are required before real-world claims.

## 6. Stochastic false confidence

Rare collapses can be missed by averages.

Controls:
- survival is protected before welfare;
- future large-world experiments must report failure distributions and upper confidence bounds;
- failure trajectories are retained for biopsy instead of discarded.

## 7. Hidden non-conservation

Economic simulations can accidentally create money, users, content, or capacity.

Controls:
- internal ledger transfers have conservation tests;
- external sources/sinks must be explicit model transitions;
- optimized engines must be differentially checked against a slow reference implementation.

## 8. Meta-loop runaway

Faster search may increase false promotions or evaluation leakage.

Controls:
- meta search has its own held-out evidence;
- search cost is explicit;
- meta pressure-knee experiments measure where aggressiveness harms trustworthiness;
- the meta-loop cannot silently change the constitution judging it.

## 9. False realism

Adding detail can make the simulation look realistic while reducing identifiability and auditability.

Control:
- preserve an exact small-world hierarchy alongside every larger model;
- realism is added only with a declared question that requires it.

## 10. Single-world monoculture

A rule can be robust in one structural model and fragile under another.

Future control:
- world ensembles with different demand, substitution, entry, financing, recommendation, and shock dynamics;
- promote only mechanisms that survive declared structural uncertainty sets.
