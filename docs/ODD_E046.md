# ODD addendum — E046 authority-constrained active sensing

## Purpose

Attack E045's cost objective.

E045 correctly avoids maximal state recovery, but a cost-only optimizer can still choose evidence that is not authorized to be queried.

E046 connects active sensing back to E024's evidence-authority plane.

## Candidate reference

The decision predicate still needs additional evidence.

Candidate observations include:

| Candidate | Cost | Resolves? | Authorized? |
| --- | ---: | --- | --- |
| raw customer-ledger boolean | 1 | yes | no |
| cheap partial aggregate refinement | 1 | no | yes |
| signed predicate attestation | 3 | yes | yes |
| authorized exact current MRR | 5 | yes | yes |

A naive cost-only search chooses the raw customer-ledger query.

That result is inadmissible.

## Authority-first search

The corrected optimization is lexicographic:

```text
1. reject unauthorized evidence
2. reject evidence that does not resolve the requested predicate
3. among the remaining candidates, minimize declared collection cost
```

The selected observation becomes the signed predicate attestation.

## Why authority is not a soft cost

If unauthorized evidence were represented merely as "very expensive," a sufficiently large downstream benefit could still cause the optimizer to select it.

Authorization is therefore a hard admissibility constraint rather than another utility term.

## Promotion rule

`active-sensing-optimizes-only-within-authorized-evidence-set-v1`

## Consequence

The uncertainty-aware evidence loop is now:

```text
observe
→ propagate uncertainty
→ decision predicate
→ certify or ABSTAIN
→ enumerate possible observations
→ filter by authority
→ filter by predicate resolution
→ minimize cost
→ acquire
→ re-evaluate
```

## Limitation

The reference authorization/privacy labels are synthetic. Real policy must be supplied by the actual system, user consent, data controller, and access mechanism.
