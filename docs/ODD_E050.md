# ODD addendum — E050 upstream evidence-lineage roots

## Purpose

Attack E049's immediate-source diversity.

Three source labels can look independent while all three are derived from one master warehouse, vendor dataset, or upstream computation.

E050 therefore moves from source labels to an evidence-lineage graph.

## Hidden-root reference

Witnesses span five failure domains.

The false view is supported by:

```text
domain-a / source-a / master-warehouse
domain-b / source-b / master-warehouse
domain-c / source-c / master-warehouse
```

All three immediate source labels are distinct.

An E049-style verifier that checks domains and immediate sources accepts the FALSE view.

But the accepted quorum has only one upstream root.

## Root-aware verifier

Add:

```text
accepted predicate quorum
must span >= 3 independent upstream lineage roots
```

The false view loses authority.

The two TRUE witnesses are insufficient for quorum, so the correct result is ABSTAIN.

## Diversified repair

A repaired TRUE topology uses:

```text
source-a / root-a
source-b / root-b
source-c / root-c
```

and regains predicate authority.

## Consequence

Evidence independence becomes graph-structured:

```text
witness
→ immediate source
→ upstream transforms
→ warehouse/vendor/root dataset
```

A flat source-name list is not independence proof.

The relevant resilience quantity is the minimum independent upstream roots whose failure can manufacture or suppress quorum.

## Promotion rule

`predicate-quorum-must-audit-upstream-lineage-roots-v1`

## Limitation

The lineage graph is declared in the reference. Real dependencies can remain hidden and require active discovery, exactly as hidden common-mode infrastructure did in E023.
