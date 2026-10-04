# ODD addendum — E062 audit-evidence failure domains

## Purpose

Attack E061's cheapest shared-evidence audit cover.

E061 reduces safe audit cost from 8 to 6 by reusing two evidence bundles across four proof obligations.

That optimization assumes the shared evidence itself is not a dangerous common-mode failure domain.

E062 removes that assumption.

## E061 plan

```text
control-plane-bundle
  covers network + identity

infra-resilience-bundle
  covers power + operator
```

Each obligation has exactly one supporting artifact.

If the control-plane evidence is wrong, two obligations are simultaneously and falsely discharged.

Likewise for the infrastructure bundle.

The maximum proof-obligation blast of one evidence-artifact failure is therefore:

```text
2
```

## Declared evidence-failure budget

Require:

```text
one audit-evidence artifact failure
must falsely discharge at most one proof obligation
```

Every audit-action subset is enumerated again under this constraint.

## Exact robust cover

The minimum-cost safe plan is not fully independent. Exact search finds a partially reused, corroborated plan:

```text
control-plane-bundle cost 2
identity-targeted    cost 1
power-deep           cost 3
operator-targeted    cost 2
```

Total:

```text
8
```

The control-plane bundle covers network + identity, while identity also has independent support. If the bundle fails, only network loses its sole support; proof blast is therefore 1. The optimizer keeps useful evidence reuse where corroboration makes it safe.

## Consequence

```text
minimum cost-only cover
!=
minimum failure-domain-safe cover
```

Evidence reuse is itself a topology decision.

## Authority change

E061's cost-6 plan loses evidence-failure-domain authority and is marked:

`REVOKED`

The E061 set-cover result remains mathematically correct for its original cost-only model. E062 does not ban evidence reuse; it requires enough overlapping support that one artifact failure stays within the declared proof-blast budget.

## Promotion rule

`audit-evidence-reuse-must-model-proof-obligation-failure-blast-v1`

## Limitation

The reference uses binary artifact failure and a one-obligation blast budget. Partial or correlated evidence corruption requires richer audit-evidence quorum models.
