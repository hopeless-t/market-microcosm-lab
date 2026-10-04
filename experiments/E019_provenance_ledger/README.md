# E019 — Durable certificate provenance ledger

E018 can decide which certificate should receive scarce audit budget. E019 makes the certificate's history replayable and tamper-evident.

## Ledger

Each event records:

- sequence index;
- event type;
- certificate ID;
- generation fingerprint;
- evidence epoch;
- event payload;
- previous event hash;
- current event hash.

The event hash is SHA-256 over canonical JSON for the event body.

## Replay

The ledger can reconstruct certificate state from events such as:

- ISSUE;
- ADAPTIVE_USE;
- AUDIT_PASS;
- GENERATION_MISMATCH;
- RECERTIFY;
- AUDIT_FAIL / REVOKE;
- EXPIRE.

The reference ledger crosses from the E016 certified generation into the changed generation and ends ACTIVE on the recertified generation.

## Adversarial tests

E019 intentionally tests four mutation classes:

1. payload mutation without rehash;
2. event deletion;
3. event reordering;
4. a stronger attack that rewrites an event and recomputes every downstream hash.

The first three must fail internal chain verification.

The fourth is more important: a self-consistent rewritten hash chain can pass its own internal check. Therefore the ledger also requires a trusted out-of-ledger checkpoint of event count, head hash, expected final state, and generation.

The rehashed attack changes the final replayed state to REVOKED. Internal chain verification still passes, but the original checkpoint no longer matches.

## Promotion rule

The contract is promoted only if:

- clean chain and checkpoint verification pass;
- clean replay reaches the expected generation/state;
- direct mutation/deletion/reorder are detected;
- append-only extension preserves all previous event hashes;
- the fully rehashed rewrite demonstrates the weakness of internal-only checking;
- the external checkpoint detects that rewrite.

## Limitation

A SHA-256 chain plus trusted checkpoint is tamper-evidence relative to the checkpoint. It is not author identity, non-repudiation, or a public transparency log.

Future work can add signatures or independently published transparency anchors.
