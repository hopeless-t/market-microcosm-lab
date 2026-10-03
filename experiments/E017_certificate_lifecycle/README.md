# E017 — Certificate lifecycle and audit cadence

E016 proved that adaptive authorization can be revoked. E017 turns that capability into an explicit lifecycle.

## State machine

The certificate moves through evidence-driven states:

- ACTIVE — adaptive exploration permitted;
- AUDIT_DUE — exhaustive verification required;
- EXPIRED — audit evidence is too old; exhaustive mode required;
- GENERATION_MISMATCH — structural/evaluation generation changed; exhaustive recertification required;
- REVOKED — a failed exhaustive audit removed adaptive authority.

## Deterministic evidence epochs

The lifecycle uses integer evidence epochs rather than wall-clock time so experiment replay remains deterministic.

Default policy:

- periodic exhaustive audit every 3 epochs;
- hard expiry after 6 epochs without a successful audit.

## Cost benchmark

The query costs come from E015:

- exhaustive pair-surface evaluation: 882 queries;
- adaptive evaluation: 205 queries.

E017 compares:

1. always-exhaustive baseline;
2. stable generation with periodic audits;
3. a generation-drift schedule where the fingerprint changes at epoch 5.

## Fail-closed cases

Two additional tests are mandatory:

- a failed audit must remain REVOKED and exhaustive on the next epoch;
- skipping audits until the hard TTL must become EXPIRED and exhaustive.

The lifecycle is promoted only if all safety gates and the stable-schedule cost gate pass.
