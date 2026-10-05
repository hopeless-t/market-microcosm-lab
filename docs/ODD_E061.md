# ODD addendum — E061 coupled dependency-audit bundles

## Purpose

E060 optimizes audit depth independently per dependency branch.

That is still suboptimal when one audit action can discharge multiple proof obligations.

E061 models shared evidence explicitly.

## Unsafe obligations

After the E060 reference classification, these branches need additional proof:

```text
network
identity
power
operator
```

Vendor is already inside the two-channel blast budget.

## Candidate audit actions

Independent actions reproduce E060's total cost 8.

Two shared bundles are also available:

```text
control-plane-bundle
  cost 2
  covers network + identity

infra-resilience-bundle
  cost 4
  covers power + operator
```

A full-platform bundle costs 7 and covers all four obligations.

## Exact set-cover search

Every audit-action subset is enumerated.

The minimum-cost complete cover is:

```text
control-plane-bundle
infra-resilience-bundle
```

with:

```text
total cost = 6
```

This saves 2 cost units versus E060's branch-separable optimum and also beats the cost-7 monolithic full-platform audit.

## Consequence

Shared audit evidence couples proof obligations.

The allocation problem is therefore closer to weighted set cover / evidence portfolio selection than independent branch minimization.

## Promotion rule

`dependency-audit-allocation-must-model-shared-evidence-bundles-v1`

## Limitation

Coverage is deterministic and all-or-nothing. Real evidence can be partial, uncertain, sequential, and reusable across future audit epochs.
