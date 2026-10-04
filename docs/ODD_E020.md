# ODD addendum — E020 checkpoint rotation

## Purpose

Extend E019's single independent checkpoint into a long-lived rotation protocol while preserving continuity to a previously trusted anchor.

## Entities

RotatingCheckpoint:

- sequence;
- ledger ID;
- event count;
- ledger head hash;
- previous checkpoint hash;
- checkpoint hash.

## Scheduling

The reference ledger has 10 events.

Checkpoint emission occurs at event counts 2, 4, 6, and 8.

The final two ledger events intentionally remain unanchored to expose the distinction between current history and externally fixed history.

## Verification

A valid rotation requires:

1. valid underlying ledger hash chain;
2. contiguous checkpoint sequence;
3. previous-checkpoint hash linkage;
4. strictly increasing anchored event count;
5. checkpoint head matching the exact ledger prefix;
6. recomputed checkpoint hash equality;
7. presence of the independently pinned checkpoint when one is required.

## Latest-only adversary

The attacker rewrites ledger event 1 and recomputes every downstream ledger hash.

A newly forged checkpoint over that rewritten ledger is internally consistent and passes a latest-only verifier.

The historical rotation verifier retains an older independently pinned checkpoint. Because the rewritten prefix no longer matches the old anchored head, the attack fails.

## Fork detection

Two distinct child checkpoints referencing the same non-genesis parent constitute an observable fork.

## Trust boundary

Rotation continuity protects a previously pinned external fact.

It does not solve malicious issuance by a compromised anchor authority. Signatures, multiple independent anchors, or transparency-log publication remain separate mechanisms.
