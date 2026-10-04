# E020 — Checkpoint rotation and anchor continuity

E019 shows that a mutable ledger cannot authenticate a fully rewritten version of itself. E020 extends the external anchor from one checkpoint to a rotating chain.

## Rotating checkpoint

Each checkpoint records:

- checkpoint sequence;
- ledger ID;
- anchored ledger event count;
- anchored ledger head hash;
- previous checkpoint hash;
- current checkpoint hash.

The checkpoint hash is SHA-256 over canonical checkpoint content.

## Reference rotation

The extended reference ledger has 10 events.

Checkpoints are emitted after event counts:

- 2;
- 4;
- 6;
- 8.

That intentionally leaves a 2-event unanchored tail so the report distinguishes durable anchored history from recent mutable history.

## Pinned anchor

Checkpoint sequence 1 is treated as independently pinned outside the mutable bundle.

The rotation verifier must reproduce the checkpoint chain and prove that the pinned checkpoint still exists at the same sequence and still matches the corresponding ledger prefix.

## Adversarial tests

E020 tests:

1. deleting a checkpoint;
2. reordering checkpoints;
3. rewriting an old ledger prefix and forging a self-consistent latest-only checkpoint;
4. presenting two different child checkpoints for the same parent.

The latest-only forgery is expected to pass a verifier that sees only the rewritten ledger and forged latest checkpoint.

The same rewritten ledger must fail the rotation verifier because its prefix no longer matches the independently pinned checkpoint history.

## Promotion

The rotation contract is promoted only if:

- honest rotation verifies;
- pinned continuity verifies;
- checkpoint deletion and reorder are detected;
- latest-only forgery demonstrates the danger of forgetting old anchors;
- pinned rotation rejects the rewritten prefix;
- checkpoint forks are detected.

## Limitation

This still assumes that at least one external checkpoint is trustworthy.

If the external anchoring authority itself can mint replacement anchors, cryptographic signatures or an independent transparency service are needed.
