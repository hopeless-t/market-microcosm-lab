# ODD addendum — E057 recursive measurement-lineage discovery

## Purpose

Attack E056's repaired five-root topology.

E056 proves that one declared measurement-root fault flips at most two certified channels.

That is sufficient only if the five roots are actually independent.

E057 recursively probes the roots themselves.

## Hidden super-root reference

The five declared measurement roots each own two channels:

```text
root-0 -> 2 channels
root-1 -> 2 channels
root-2 -> 2 channels
root-3 -> 2 channels
root-4 -> 2 channels
```

But the first three secretly depend on one shared infrastructure layer:

```text
root-0 ┐
root-1 ├─> shared-observability-plane
root-2 ┘
```

A fault in that super-root corrupts six certified channels.

That exceeds E056's two-bit operational budget.

## Recursive probe

A bounded probe targeted at the shared observability plane simultaneously perturbs three declared measurement roots.

Local probes against root-3 or root-4 remain local.

The common-mode fingerprint therefore discovers the hidden super-root and revokes E056's independence authority.

## Consequence

Failure-domain independence is recursive.

```text
channel
→ measurement root
→ super-root
→ deeper infrastructure
```

A certificate at one layer is conditional on the independence claims below it.

## Promotion rule

`measurement-root-independence-requires-recursive-lineage-discovery-v1`

## Limitation

The reference uses a finite candidate super-root catalog and noiseless intervention fingerprints. Real systems need a stopping rule so recursive dependency discovery does not become unbounded.
