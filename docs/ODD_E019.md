# ODD addendum — E019 certificate provenance ledger

## Purpose

Persist optimized-evaluator authority decisions as a deterministic, tamper-evident provenance chain.

## Time

The ledger uses evidence epochs inherited from E017. Wall-clock time is not required for replay.

## Event identity

Each entry has an integer sequence starting at zero. Sequence and evidence epoch may not move backward.

## Hash chain

The genesis previous hash is 64 zero characters.

For each entry:

    event_hash = SHA256(canonical_json(entry_without_event_hash))

The next entry stores that hash as previous_hash.

## Evidence binding

Each authority event carries SHA-256 of the complete source experiment report that justified the decision.

The reference lineage binds evidence from E015, E016, E017, and E018.

## Verification

The verifier checks:

- ledger version;
- sequence continuity;
- non-decreasing evidence epoch;
- allowed event type;
- generation/evidence digest format;
- previous-hash linkage;
- recomputed event hash.

## Adversarial tests

The experiment mutates one middle payload, deletes one middle event, and swaps two adjacent events. All must invalidate verification.

## Limitation

Hash chaining provides tamper evidence only relative to a trusted chain tip. It does not provide authorship or protect against an attacker who can replace the entire ledger and its trusted tip.

Independent signing or transparency anchoring is intentionally left as the next trust-layer problem.
