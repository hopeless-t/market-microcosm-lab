# ODD addendum — E016 adaptive guard and certificate invalidation

## Purpose

Prevent the E015 optimization from silently becoming a self-certifying oracle.

## Certificate

A certificate records:

- a structural generation fingerprint;
- a digest of the exhaustive E014 source report;
- the certification contract;
- the issuing verifier identity.

The structural fingerprint hashes the relevant world, evaluator, pressure, interaction, adaptive-sampling, guard, and runner source files together with the evaluation contract.

## Authorization decision

The adaptive path is authorized only when:

    certificate.generation_fingerprint == current_generation_fingerprint

Otherwise the mode is exhaustive.

## Adversarial test

E016 mutates one unqueried failing cell into a surviving island on an otherwise monotone E014 surface.

The mutation is selected so that:

- global monotonicity is violated;
- the naive staircase does not query the changed cell;
- inferred full-surface classification is no longer exact.

This demonstrates why the adaptive path cannot prove its own monotonicity premise.

## Revocation

When exhaustive audit observes any monotonicity violation, the adaptive path is revoked for that generation and the required mode becomes exhaustive.

## Evidence hierarchy

1. exact structural-generation match allows use of an existing certificate;
2. adaptive sampling accelerates exploration;
3. exhaustive audit remains authoritative;
4. a new generation or failed monotonicity audit removes adaptive authorization.

## Limitation

A certificate establishes empirical validity for its declared model/evaluator generation and tested domain. It does not prove monotonicity for arbitrary future model changes or untested domains.
