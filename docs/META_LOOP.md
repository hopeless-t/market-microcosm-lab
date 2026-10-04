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


## Sampling-assumption self-attack

E026 demonstrates a meta-loop that improves itself by attacking an assumption introduced only moments earlier.

The published SARTRAS counts make a simple-random-sampling reference mathematically convenient. Under that reference, exact hypergeometric detection has a clear rarity knee. But the laboratory does not promote convenience into empirical authority.

A second-stage adversary removes the unverified random-selection assumption while keeping the same population and sample counts. It can place all carriers outside the selected institutions, collapsing the sample-size-only detection lower bound to zero.

The promoted result is therefore not the optimistic SRS prevalence curve. It is the stricter evidence rule: **sampling-design metadata is required before prevalence inference**.

This is the empirical analogue of E016/E023: when a hidden structural premise can dominate the result, the optimized or convenient path loses authority and the system falls back to a less committal model.


## Metric-definition drift guard

E027 attacks a different empirical shortcut: treating two public numbers as comparable merely because their labels look similar.

The 2022 Game Pass observation is a lower bound (>25M subscribers), the 2024 observation is a rounded 34M member headline, and the Xbox Live Gold → Game Pass Core conversion occurs between them.

A naive 36% ratio is kept in the evidence bundle as a visible counterexample but receives no inferential authority.

The empirical meta-loop now versions metric definitions analogously to simulator generations. Time-series calculations require compatible definition generations and value semantics. A public number may be real and still be inadmissible for a specific estimator.


## Negative evidence and survivorship control

E028 makes failed and withdrawn systems a required empirical input rather than an anecdotal appendix.

The initial Japanese corpus includes deliberate product pivots, portfolio pruning, a planned managed-cloud sunset, strategic restructuring, and industry bankruptcy context. These cases expose failure mechanisms that are absent from a success-only calibration set.

The meta-loop may not declare an empirical model adequate merely because it fits surviving subscription systems. It must also report which admitted negative-evidence mechanisms the model can and cannot represent.


## Strategic exit as a control action

E029 separates voluntary exit from forced failure.

The current ecological world turns developers and publishers inactive when their cash falls below zero. E029 preserves that forced-failure semantics but adds a distinct future action: an operating actor may choose orderly exit when continuation value is worse than sunset plus redeployment.

This matters because voluntary exit can preserve the firm while harming catalog diversity or users. Firm-level rationality and ecosystem-level viability are therefore separate objectives.


## Typed churn semantics

E030 attacks the generic use of the word churn.

BBD's portfolio pruning shows that reported MRR churn can rise while ARR and ARPA rise and contract count falls. The company attributes part of that churn to unprofitable-service withdrawal and low-price-plan migration.

The meta-loop must now bind churn to both a **layer** (end user, account/logo, MRR, supplier/content) and a **cause** (distress/demand loss, intentional pruning, migration). Cross-layer coefficient reuse requires explicit evidence rather than name matching.


## PMF proxy guard

E031 attacks success-side proxy Goodharting.

Srush, Leaner, and SalesNow each provide a different counterexample to the idea that revenue or enthusiastic users certify long-run fit. Positive local signals can coexist with non-repeatable targeting, high human delivery burden, poor customer success, weak scalability, or a market ceiling.

The meta-loop must therefore keep **observation** and **certification** separate on the success side too. Revenue, ACV, engagement, and usage can propose a hypothesis; they cannot promote PMF without separate evidence for repeatability, customer success, product-delivered value, scalability, and market headroom.


## Cash timing and early-warning compilation

E032-E035 turn the Japanese negative-evidence corpus into a first warning architecture.

E032 separates booked revenue from cash arrival. A positive booked margin can coexist with imminent liquidity failure when collection lags behind payroll and fixed costs.

E033 separates upstream funnel activity from downstream value. Large lead or appointment attainment cannot self-certify orders, activation, or customer success.

E034 separates software cost from recurring human-delivery cost. High ACV and software-only margin can hide a service burden that reverses product rankings after fully loaded accounting.

E035 compiles these failure mechanisms together with market-headroom and strategic-exit signals into a finite multi-signal warning tournament. Revenue-only and churn-only proxies have explicit blind spots; the multi-signal vector matches the exact reference oracle.

The meta-loop is **not** allowed to treat that exact match as external predictive validation. The next authority step requires broad generated scenario families, threshold search on discovery sets, untouched holdouts, and eventually real longitudinal company data.


## Generated warning holdout

E036 attacks the possibility that E035 merely memorized its hand-built archetypes.

A broad deterministic generator creates isolated discovery and holdout populations. The meta-loop searches 324 warning-threshold combinations only on discovery, freezes the winner, then evaluates an untouched seed bank.

The selected multi-signal rule keeps greater than 98% precision, recall, and F1 on the generated holdout while revenue-only and churn-only rules retain severe recall blind spots.

Authority remains limited: discovery and holdout still share one structural generator. The next falsification must change the generator itself rather than only the random seed.


## Warning structural-drift revocation

E037 attacks E036's shared-generator assumption.

The frozen E036 warning is moved to a new structural generation with an interaction-only market-headroom × downstream-success failure. Its recall falls below the prior authority threshold and the warning is revoked.

A repaired candidate adds the interaction term and restores greater than 99% precision and recall on the shifted generation.

The empirical warning plane now has the same authority lifecycle as the adaptive experimenter: strong prior evidence is generation-scoped and can be explicitly revoked when the failure topology changes.


## Real longitudinal component holdout

E038 introduces the first real-company quarterly holdout.

Informetis publishes ARR by service family and an event annotation describing the planned end of a major rental-business service, stopped recruitment, and natural subscriber decline. A minimal retention model fit on 2025-Q1 through Q3 Smart Living Standard places its Q4 point prediction within one displayed million-JPY unit of the published Q4 value. E042 later revokes any sub-1% precision interpretation because the chart resolution is coarser than that claim.

The same model does not fit every component. The meta-loop therefore promotes the evidence shape — component identity plus event annotation plus holdout isolation — rather than promoting geometric decay as a universal law.


## Measurement-kernel lag

E039 adds another state layer between reality and evidence.

Informetis ARR is a trailing-six-month average MRR transformed to an annual value. An abrupt underlying service change is therefore spread across six months of reported ARR.

Empirical warning authority must now track:

```text
latent state
→ measurement kernel
→ reported metric
→ publication
→ warning decision
```

Lead-time claims that omit the metric window are not admissible.


## Identifiability-driven checkpoints

E040 demonstrates that a rolling KPI is not merely delayed; it may be fundamentally non-identifying. Hundreds of distinct monotone latent paths can produce one reported ARR while disagreeing materially about current MRR.

E041 then searches for the smallest repair. For consecutive fixed-width rolling windows, storing the single outgoing boundary MRR is enough to reconstruct the incoming/current MRR exactly. The full path is unnecessary for that one-step task.

This promotes a general meta-loop rule:

```text
find where projection loses identifiability
→ identify the missing boundary state
→ preserve only that indispensable checkpoint
→ verify exact reconstruction
```

The goal is neither maximal logging nor maximal compression. It is minimal sufficient observability.


## Precision authority, abstention, and active sensing

E042-E045 make the empirical observation plane self-limiting.

E042 propagates source reporting resolution and revokes E038's sub-1% precision interpretation while retaining interval consistency.

E043 then treats reconstructed hidden state as an uncertainty set and asks whether that set is sufficient for the actual decision predicate. Exact state is no longer the default objective.

E044 authorizes ABSTAIN when compatible states disagree on the requested action. Point proxies such as interval midpoints may not override that ambiguity.

E045 turns ABSTAIN into targeted active sensing: search only for the cheapest authorized observation that makes every compatible state agree on the requested predicate.

The resulting loop is:

```text
observe
→ propagate uncertainty
→ evaluate predicate over every compatible state
→ certify if unanimous
→ otherwise ABSTAIN
→ acquire minimum-cost predicate-sufficient evidence
→ re-evaluate
```

This is minimal sufficient observability under uncertainty, not maximal state collection.


## Authority and temporal admission for active sensing

E046-E047 close two remaining loopholes in minimum-cost observation selection.

E046 demonstrates that a cost-only optimizer can choose unauthorized evidence. Authorization is therefore a hard admissibility filter, not a soft penalty.

E047 shows that authorization alone is still insufficient. Evidence must be fresh enough for the current hazard and aligned with the metric-definition generation required by the decision.

The active-sensing sequence is now:

```text
enumerate observation candidates
→ authority filter
→ predicate-sufficiency filter
→ freshness filter
→ metric-generation filter
→ cost optimization
→ acquire
→ propagate uncertainty
→ re-evaluate predicate
```

This connects the empirical evidence plane directly to the uncertainty-aware control loop.


## Predicate witness quorum and source diversity

E048-E049 reuse the trust-plane machinery inside active empirical sensing.

E048 removes the final-authority role from one signed predicate attestation. Predicate truth requires a matching quorum across declared independent witness domains; unresolved conflicts ABSTAIN.

E049 then attacks the domain map itself. Three administratively distinct witnesses can still consume one shared upstream feed and fail together. The sensing plane therefore tracks both witness/failure-domain topology and upstream data-lineage topology.

The acceptance path becomes:

```text
authorized
→ predicate resolving
→ fresh
→ metric-generation aligned
→ witness quorum
→ failure-domain diversity
→ upstream source diversity
→ predicate authority
```

As in E023, discovered hidden common modes invalidate prior independence authority and require re-evaluation.


## Evidence-lineage root audit

E050 attacks the flat source-diversity model promoted by E049.

Three distinct immediate source labels can still derive from one master warehouse or vendor dataset. A quorum that appears domain-diverse and source-diverse can therefore remain one-root fragile.

The sensing plane now treats evidence independence as a dependency graph rather than a list of names. Accepted predicate authority must expose enough upstream lineage to estimate the minimum independent roots supporting the accepted view.

Discovery of a hidden lineage root is an authority-changing event: prior source-diversity evidence is revoked and the quorum must be re-evaluated.
