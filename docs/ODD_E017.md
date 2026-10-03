# ODD addendum — E017 certificate lifecycle

## Purpose

Convert E016's generation-scoped guard into an operational certificate lifecycle with explicit audit cadence, expiry, renewal, and revocation.

## Time scale

Time is represented as deterministic evidence epochs.

The default policy is:

    audit_interval_epochs = 3
    expiry_epochs = 6

A certificate can therefore be used adaptively for at most two epochs after a successful exhaustive certification/audit. At the third epoch an exhaustive audit is due. If no successful audit occurs before the sixth audit-age epoch, the certificate is expired.

## Query accounting

E015 supplies the measured reference query costs:

    exhaustive = 882
    adaptive = 205

The E017 schedule accounts for the actual evaluator selected in each epoch.

## Stable schedule

For a 12-epoch stable generation:

- epoch 0 is exhaustive issuance;
- epochs 3, 6, and 9 are exhaustive renewal audits;
- all other epochs use the adaptive evaluator.

This is compared against an always-exhaustive 12-epoch baseline.

## Drift schedule

At epoch 5 the structural/evaluation fingerprint changes.

The old certificate must not be reused. Epoch 5 is exhaustive recertification for the new generation and the audit clock restarts.

## Negative paths

- failed exhaustive audit → REVOKED → exhaustive required;
- skipped audit beyond hard expiry → EXPIRED → exhaustive required.

## Trust boundary

The lifecycle scheduler may decide *when* to request exhaustive verification. It may not redefine what constitutes a passing audit. The exhaustive verifier remains authoritative.
