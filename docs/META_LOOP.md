# Meta-improvement loop

The inner loop improves ecosystem policy. The outer loop improves the inner loop.

## Objects the meta-loop may change

- observation/sampling strategy;
- causal estimator;
- candidate generator;
- search algorithm;
- simulation budget allocation;
- planning horizon;
- uncertainty model;
- stress-test generator;
- metric estimator;
- experiment stopping rule.

## Objects it may not silently change

- accounting conservation;
- run/replay identity semantics;
- held-out isolation;
- protected hard constraints;
- promotion evidence requirements.

Those belong to the Root of Trust. They can evolve only as a separately versioned constitutional change, after re-evaluating historical baselines.

## Meta-loop health metrics

Track:
- oracle regret;
- false-promotion rate;
- false-rejection rate where measurable;
- discovery rate of real improvements;
- sample efficiency;
- time-to-diagnosis;
- generalization gap;
- calibration error of predicted intervention effects;
- robustness under adversarial scenario generation;
- reproducibility rate.

## Meta-pressure-knee experiments

Treat the improvement loop itself as an ecosystem. Sweep search aggressiveness, observation compression, simulation budget, promotion alpha, and horizon. Locate knees where faster adaptation suddenly increases false promotion or collapse risk.

The target is not maximal loop speed. It is maximal trustworthy improvement throughput.


## Implemented stress-curriculum meta-loop

E012 treats the evaluation-world distribution itself as mutable improvement machinery.

Candidate evaluators train/select mechanisms on different pressure curricula, then their selected mechanisms are compared on a common isolated stress holdout. This prevents a neutral benchmark from being treated as sufficient merely because every candidate survives it.

The current implementation explicitly prices search cost into tie-breaking, so a wider curriculum is not automatically preferred when a smaller curriculum generalizes equally well.


## Implemented experiment-cost meta-improvement

E015 treats the experimenter's query strategy as mutable meta-level machinery.

The exhaustive E014 interaction surfaces act as verifier truth. A monotone staircase sampler competes on fidelity and cost, with promotion requiring exact cell classification, exact frontier recovery, exact interaction-only counts, zero observed monotonicity violations, and at least 50% query savings.

The promoted E015 candidate reduced 882 pair-surface queries to 205, a 76.8% reduction, while reproducing the exhaustive truth exactly on all 18 tested surfaces.

This creates two distinct planes:

- **adaptive exploration plane** — cheaper boundary discovery under a certified monotonicity assumption;
- **exhaustive certification plane** — periodic reference audit and re-certification.

The adaptive sampler may not certify its own structural assumption. A world, transition, viability, or evaluator-generation change invalidates the previous certificate and requires an exhaustive audit before the cheaper path can be trusted again.


## Revocable meta-improvement authority

E016 adds the missing negative half of meta-improvement: a promoted optimization can lose authority.

Adaptive authorization is scoped to a structural/evaluation generation fingerprint. A relevant code or contract change invalidates the certificate before the optimized path may be used.

E016 also demonstrates that a hidden non-monotone island can evade sparse staircase queries while leaving the first frontier unchanged. The adaptive evaluator therefore cannot use frontier agreement as self-certification.

The allowed lifecycle is:

promote → certify → use adaptively → invalidate or audit → revoke if needed → fall back to exhaustive → re-certify.

A self-improvement system without explicit revocation is incomplete.


## Evidence-age audit scheduler

E017 makes verifier scheduling an explicit part of the meta-loop.

The scheduler may save evaluation cost by using a certified adaptive evaluator between authoritative audits, but it cannot weaken the audit requirement itself.

The current deterministic policy audits every three evidence epochs and hard-expires after six epochs without a successful audit. In the stable 12-epoch benchmark this cuts pair-surface queries by 51.2%. A generation drift at epoch 5 forces immediate exhaustive recertification and still retains 44.8% savings across the full schedule.

Evidence age therefore acts on **authority**, not on truth: older evidence reduces permission to use the optimized evaluator until authoritative verification refreshes it.


## Audit portfolio optimization

E018 treats authoritative verifier budget allocation as another meta-level control problem.

The laboratory does not allow a plausible local ranking rule to become authoritative merely because each per-certificate score is sensible. A value-per-cost greedy scheduler is tested against an exact subset oracle and has a fixed failure case.

The promoted bounded-DP scheduler reproduces the exact audit portfolio optimum across the deterministic generated suite while reducing scheduler search work by 87.3%.

Mandatory audits are constitutional constraints, not soft objective terms. If they cannot fit inside the declared audit budget, the portfolio fails closed instead of silently optimizing around them.


## Externally anchored provenance

E019 makes the meta-loop's own certification history an explicit trust object.

Certificate events are append-only and hash-linked so local corruption, deletion, and reordering are detectable. But the experiment also demonstrates the stronger failure mode: a rewritten history can recompute every downstream hash and remain internally self-consistent.

Therefore the meta-loop may maintain and replay its ledger, but it may not be the sole authority that authenticates that ledger. A trusted checkpoint outside the mutable history fixes the accepted head hash, event count, final certificate state, and generation fingerprint.

This creates another two-plane separation:

- **mutable provenance plane** — append-only event history and deterministic replay;
- **anchor plane** — independently trusted evidence that decides which history head is authoritative.

The history can explain authority. It cannot grant itself authority.
