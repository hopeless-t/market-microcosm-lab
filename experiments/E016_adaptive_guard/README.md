# E016 — Generation-scoped adaptive guard

E015 promoted a cheaper adaptive boundary sampler for the current E014 surfaces. E016 asks the safety question that promotion creates:

> When must the adaptive certificate stop being trusted?

## Certificate scope

The adaptive certificate is bound to a fingerprint of:

- market-world transition code;
- ecological evaluation code;
- pressure-axis semantics;
- pairwise interaction evaluator;
- adaptive sampling implementation;
- guard implementation;
- E014/E015/E016 runner semantics;
- declared evaluation contract.

The contract includes pressure pairs, grid size, survival threshold, horizon, and evaluation/biopsy seed banks.

## Fail-closed generation change

E016 mutates the certified horizon from 60 to 61 without changing the certificate.

Expected behavior:

- original generation → adaptive path allowed;
- changed generation → certificate mismatch → exhaustive path required.

## Adversarial non-monotone island

The experiment takes a certified monotone E014 surface and inserts a hidden survival island inside a region that the staircase sampler would infer as failure without directly querying the cell.

This deliberately breaks the monotonicity assumption.

The expected result is:

- naive adaptive classification becomes imperfect;
- exhaustive audit detects monotonicity violations;
- the adaptive certificate is revoked;
- the post-audit path falls back to exhaustive evaluation.

## Important limitation

Sparse adaptive queries cannot prove global monotonicity. E016 does not pretend otherwise.

The trust architecture is therefore asymmetric:

adaptive exploration → cheap, certificate-dependent

exhaustive audit → authoritative, certificate-issuing/revoking

A structural generation change invalidates the certificate before use. Hidden within-generation assumption violations are detected by periodic exhaustive audit, not by wishful inference.
