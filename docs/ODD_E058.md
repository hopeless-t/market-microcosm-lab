# ODD addendum — E058 minimum-cost recursive-lineage repair

## Purpose

E057 discovers that three E056 measurement roots share one hidden super-root.

That discovery revokes E056 authority because one super-root fault can corrupt six certified channels.

E058 repairs the topology without weakening the two-bit error budget.

## Repair actions

The five measurement roots each own two certified channels.

Three roots currently share `shared-observability-plane`:

```text
root-0 migration cost 4
root-1 migration cost 2
root-2 migration cost 3
```

Roots 3 and 4 are already on distinct providers.

A migration moves a selected root onto a fresh independent provider.

## Exact synthesis

Every migration subset is enumerated.

The repaired topology must satisfy:

```text
maximum channels under one provider <= 2
```

The exact minimum-cost repair migrates:

```text
root-1
root-2
```

with total declared cost 5.

Root-0 can remain on the original provider because it is then the only measurement root under that provider.

## Verification

After repair, five providers each own exactly one two-channel measurement root.

Every single-provider fault therefore flips exactly two certified channels, which remains inside the E055 correction budget.

## Consequence

A discovered common mode does not automatically justify raising the threat tolerance.

The preferred lifecycle is:

```text
discover common mode
→ revoke old topology authority
→ synthesize minimum-cost structural repair
→ verify original robustness contract again
```

## Promotion rule

`recursive-lineage-common-mode-repair-by-minimum-cost-repartition-v1`

## Limitation

Real provider migrations are not free independent slots. Capacity, latency, geography, vendor identity, and hidden shared infrastructure must also be admitted.
