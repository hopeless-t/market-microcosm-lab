# Root of Trust

This file defines the minimum constitution for one evaluation generation.

## R1 — Conservation
All money/resource creation and destruction must be explicit external source/sink events. Internal transfers conserve the ledger.

## R2 — Causality
State at time t+1 may depend only on allowed state/history, current action, declared stochastic input, and declared exogenous input.

## R3 — Oracle isolation
Deployable policy code may not consume oracle-only state or future information.

## R4 — Reproducibility
Every scored run has an immutable manifest containing code revision, model/policy/verifier versions, scenario, parameters and seed.

## R5 — Independent promotion
The candidate generator cannot directly mark itself promoted. Promotion is produced by a verifier from persisted evidence.

## R6 — Held-out isolation
Promotion scenarios/seeds are not available to candidate optimization.

## R7 — Constitutional versioning
Changing any Root-of-Trust rule or the hard viability constraints creates a new evaluation generation. Incumbent and challengers are re-evaluated under the new generation.

## R8 — Evidence-bounded optimization authority
An optimized or approximate verifier may operate only under a certificate tied to the exact evaluation generation that earned it. Certificate age, generation mismatch, expiry, or failed authoritative audit must remove optimized authority and fail closed to the authoritative verifier.

## R9 — Externally anchored provenance
A mutable certificate/audit history may not authenticate itself solely from internally recomputable hashes. Authoritative provenance must be bound to an independently trusted checkpoint, signature, transparency anchor, or equivalent evidence outside the mutable history being authenticated. A checkpoint mismatch fails closed.

## R10 — Anchor continuity
Rotating or replacing provenance anchors must preserve verifiable continuity to previously trusted checkpoints. A newer anchor may extend trust but may not silently erase older pinned trust. Missing links, rewritten anchored prefixes, or conflicting checkpoint forks fail closed.

## R11 — Witness quorum integrity
When provenance authority is distributed across witnesses, the acceptance threshold and compromise boundary must be explicit and independently testable. The chosen quorum geometry must preserve the declared intersection property, authenticated attestations must be retained, and conflicting accepted views must surface equivocation evidence or fail closed rather than silently choosing one history.

These rules are intentionally small. The meta-loop may improve almost everything else.
