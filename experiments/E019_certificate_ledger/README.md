# E019 — Durable certificate provenance ledger

E015–E018 can promote, certify, renew, revoke, expire, and schedule optimized evaluator authority. E019 makes that authority history replayable.

## Ledger format

The ledger is append-only JSONL.

Each event records:

- format version;
- monotonic sequence;
- deterministic evidence epoch;
- event type;
- evaluation generation fingerprint;
- authority decision;
- digest of the source experiment evidence;
- structured details;
- previous event hash;
- current event hash.

The event hash is SHA-256 over canonical JSON for all fields except the event hash itself.

## Reference lineage

The reference E019 ledger records:

1. E015 adaptive sampler promotion;
2. E016 certificate issue;
3. E017 successful audit renewal;
4. E016 generation drift;
5. E017 exhaustive recertification;
6. E018 bounded-DP audit scheduler promotion;
7. E018 mandatory-audit fail-closed evidence.

## Tamper probes

E019 must detect:

- payload mutation in the middle of the chain;
- deletion of an intermediate entry;
- reordering of adjacent entries.

The same source reports must also deterministically rebuild the same JSONL and ledger tip hash.

## Trust limitation

A local hash chain is not a signature.

It detects mutations relative to a trusted tip. An attacker able to rewrite every entry and replace the trusted tip can recompute the full chain.

Future work should anchor ledger tips in an independent signature, transparency log, release artifact, or external witness.
