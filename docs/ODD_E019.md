# ODD addendum — E019 durable provenance ledger

## Purpose

Persist certificate issuance, use, audit, invalidation, recertification, expiry, and revocation as replayable append-only evidence.

## State

Each ledger event contains:

- index;
- type;
- certificate ID;
- evaluation-generation fingerprint;
- deterministic evidence epoch;
- payload;
- previous event hash;
- event hash.

## Hash construction

The event hash is:

    SHA256(canonical_json(event_body))

where event_body includes the previous event hash.

The first event points to a fixed all-zero genesis hash.

## Integrity checks

Internal verification checks:

1. contiguous event indexes;
2. exact previous-hash linkage;
3. recomputed event hash equality.

This detects accidental corruption and local mutation, deletion, or reordering.

## External checkpoint

A hash chain does not protect against an attacker who rewrites history and recomputes every downstream hash.

Therefore E019 models a checkpoint stored outside the mutable ledger. The checkpoint fixes:

- ledger ID;
- event count;
- head hash;
- expected final certificate state;
- expected generation fingerprint.

A fully rehashed ledger can remain internally consistent while failing the checkpoint.

## Replay

The verifier reconstructs certificate authority from ledger history. A replay mismatch relative to the checkpoint is a provenance failure.

## Append-only property

Extending a valid ledger must leave every existing event hash unchanged.

## Threat boundary

The experiment assumes the checkpoint is independently trusted. If both ledger and checkpoint can be rewritten by the same actor, this construction alone does not provide non-repudiation.

Cryptographic signatures and external transparency publication remain future work.
