# ODD addendum — E049 upstream evidence-source diversity

## Purpose

Attack E048's declared witness independence.

Five attesters in five administrative or infrastructure failure domains do not necessarily represent five independent observations.

Three witnesses can still consume one common upstream source.

E049 moves the E023 hidden-common-mode lesson into the active empirical sensing plane.

## Hidden common-source reference

Witness topology:

```text
w0 / domain-a / shared-feed / FALSE
w1 / domain-b / shared-feed / FALSE
w2 / domain-c / shared-feed / FALSE
w3 / domain-d / independent-d / TRUE
w4 / domain-e / independent-e / TRUE
```

The TRUE value is the reference ground truth.

A verifier that requires only three votes from three distinct witness domains accepts FALSE.

The false quorum spans three domains but only one upstream evidence source.

## Source-aware verifier

Add another hard requirement:

```text
accepted predicate quorum
must span >= 3 upstream evidence sources
```

The false shared-feed view loses authority.

The remaining two TRUE observations do not yet form quorum, so the correct result is ABSTAIN.

## Diversified repair

A second topology gives the TRUE view three independent sources and leaves two FALSE witnesses on one shared bad source.

The source-aware verifier accepts TRUE.

## Consequence

Evidence independence requires at least two graphs:

- witness/failure-domain topology;
- upstream data-lineage/source topology.

Distinct identities or execution domains do not automatically imply independent observations.

## Promotion rule

`predicate-quorum-must-diversify-upstream-evidence-sources-v1`

## Limitation

The source graph is declared here. Hidden, undocumented common dependencies remain possible and must trigger revocation/re-audit if later discovered.
