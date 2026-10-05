# ODD addendum — E048 predicate-evidence witness quorum

## Purpose

Attack E047's assumption that one fresh, authorized, generation-aligned predicate attestation is sufficient.

A single attestation can still be wrong, compromised, or equivocated.

E048 reuses the E021–E023 trust lesson on the empirical sensing plane.

## Reference topology

Five predicate witnesses are placed in five declared failure domains.

Four attest TRUE and one compromised witness attests FALSE.

A single-witness consumer that happens to select the compromised witness receives the wrong result.

A 3-of-5 verifier instead requires:

- at least three matching predicate votes;
- at least three distinct declared failure domains;
- every counted witness authorized, fresh, and metric-generation aligned.

The TRUE view is accepted despite one false witness.

## Conflict behavior

A separate 2-TRUE / 2-FALSE reference has no 3-vote quorum.

The correct output is not tie-breaking.

It is **ABSTAIN**.

## Consequence

Predicate-native sensing no longer ends at one signed observation.

The acceptance path becomes:

```text
authorized
→ fresh
→ generation aligned
→ independent witness domains
→ matching quorum
→ predicate authority
```

No quorum means no predicate authority.

## Promotion rule

`predicate-attestation-requires-independent-witness-quorum-v1`

## Limitation

Declared witness domains do not prove upstream data independence. Distinct attesters can still consume one common data source and fail together.
