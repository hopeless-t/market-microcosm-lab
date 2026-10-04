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


## Anchor continuity under rotation

E020 extends E019's anchor plane from a single checkpoint into a rotating chain.

A new checkpoint is not allowed to replace historical trust by fiat. Each rotation links to the previous checkpoint hash and anchors a strictly larger ledger prefix. At least one previously trusted checkpoint can remain pinned outside the mutable bundle.

The adversarial comparison is explicit: a rewritten ledger plus a freshly forged latest-only checkpoint can pass a verifier that has forgotten the past. The same rewrite fails when the verification path must remain continuous with the pinned historical checkpoint.

The meta-loop therefore distinguishes:

- **latest state** — what the newest checkpoint claims;
- **trust continuity** — whether that claim extends previously accepted history without rewriting it.

Optimization may advance the head. It may not reset the root of trust.


## Multi-witness anchor authority

E021 distributes checkpoint acceptance across a synthetic 3-of-5 witness quorum.

The meta-loop may choose or tune witness topology only if the threshold's failure geometry is explicit. In the current five-witness small world, exhaustive enumeration proves that all three-witness quorums intersect while two-witness quorums can be disjoint.

That intersection does not make compromise impossible. Three compromised witnesses can still forge a quorum. Instead, it provides two properties:

- one or two compromised witnesses cannot independently mint an accepted forged checkpoint;
- two conflicting accepted 3-of-5 views must share at least one witness, so retained authenticated attestations can expose equivocation.

The threshold is therefore part of the trust model, not merely a performance parameter.


## Failure-domain-aware witness topology

E022 makes witness placement another meta-level design variable.

Five identities do not imply five independent failures. Under the same 3-of-5 quorum, a 3-1-1 placement lets one domain compromise satisfy quorum, a 2-2-1 placement needs two domains, and one witness per domain needs three.

The meta-loop may therefore optimize witness placement only against explicit domain-level objectives such as minimum domains to forge, minimum domains to break availability, and declared common-mode risk. It may not use nominal witness count as a proxy for independence.

Domain labels remain hypotheses. Provider, region, operator, network, key-store, or jurisdiction separation must be evidenced rather than inferred from naming alone.


## Falsifying declared independence

E023 attacks E022's strongest nominal topology without changing any witness-domain labels.

The only change is a latent dependency hyperedge: one shared KMS shock affects witnesses 0, 1, and 2 simultaneously. This collapses the minimum forge shock count from three to one and increases modeled forge probability by more than three orders of magnitude under the declared synthetic rates.

The meta-loop must therefore distinguish:

- **declared topology** — where components are said to live;
- **causal dependency graph** — which shocks can actually affect them together.

A topology optimizer may not promote independence solely from labels. Hidden-dependency discovery, inventory evidence, fault injection, and dependency-graph revision can invalidate previous trust generations.


## Empirical evidence admission

E024 makes evidence-source admission another meta-level control surface.

The meta-loop may search for, compare, and select external datasets, but it may not silently promote a documented schema, restricted report, request-only dataset, or stale archive into authoritative calibration input.

Every admitted empirical anchor carries source identity, period, unit or metric definition, granularity, access class, and limitations. The current exact source-portfolio oracle only selects sources whose observed values are publicly available under an admitted evidence class.

This creates three explicit planes:

- **synthetic evidence plane** — simulator-generated observations under declared mechanisms;
- **empirical evidence plane** — real-world observations admitted through source/access checks;
- **certification evidence plane** — independent evidence used to authorize research claims or machinery.

The planes may constrain each other, but they may not be conflated. In particular, empirical fit is not causal identification, and public schema visibility is not public observation visibility.

E024 also turns model-assumption rejection into a useful meta-loop output: Netflix's reported regional ARM dispersion is already sufficient to reject one global empirical revenue-per-membership constant before expensive fitting begins. SARTRAS sampling similarly requires future empirical worlds to distinguish latent population state from sampled observation.


## Empirical model-complexity selection

E025 turns admitted empirical structure into a meta-level choice over model complexity.

Rather than immediately fitting every published regional value, the laboratory enumerates every partition of the four Netflix reporting regions and asks for the smallest model family that keeps worst regional ARM error below a declared tolerance.

Discovery and temporal validation are separated. Q2 2023 through Q1 2024 choose the structural partition. Q2 2024 is withheld. After selection, Q1 2024 group centroids are frozen for a one-quarter-forward check.

At a 10% maximum-relative-error threshold, one and two groups fail, while three groups pass with the topology `{UCAN}`, `{EMEA}`, `{LATAM, APAC}`. The frozen one-quarter-forward prediction also remains inside tolerance.

This adds another allowed meta-loop move: **change model complexity when admitted external evidence falsifies a cheaper family**. The loop still may not relabel ARM as subscription price or infer causal regional effects from descriptive aggregates.
