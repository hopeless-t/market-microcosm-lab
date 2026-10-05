# E024 — Cross-loop decision-relevance holdout

Status: **HOLDOUT ADAPTER / REQUIRES LIVE E014→E017 REPLAY**

## Question

Can the already-qualified E015/E016/E017 adaptive-evaluation lineage serve as an
independent repository holdout for the Catfood cross-loop principle:

```text
PRUNE_PROVEN_DECISION_IRRELEVANT_WORK
```

without weakening the original Market Microcosm safety contract?

## Mapping

E015 establishes the positive case.

On the current qualified generation:

```text
exhaustive classification
== adaptive classification
```

while the adaptive evaluator performs fewer pair-surface queries.

E016 establishes counterfactual relevance and revocation.

A generation change falls back to exhaustive evaluation. A hidden non-monotone island
makes the naive adaptive result imperfect, and exhaustive audit detects the violated
assumption and revokes the adaptive path.

E017 establishes lifecycle behavior.

A certificate is not permanent authority. Audit failure, generation drift, or expiry
requires exhaustive work again.

## Generic proof mapping

The E024 adapter emits:

```text
decision_irrelevance_proven
skip_preserves_admissible_decision
relevant_counterfactual_changes_decision
zero_false_pruning_on_holdout
proof_fail_closed
```

Only when all E015/E016/E017 gates remain satisfied.

## Important interpretation

The skipped E015 queries are called decision-irrelevant only **inside the exact
generation-scoped certificate**. They are not globally useless.

```text
irrelevant under certified assumptions
!= globally irrelevant
!= delete the exhaustive verifier
```

E016 proves this distinction matters: once monotonicity/generation assumptions fail,
the omitted queries become relevant again and exhaustive evaluation is restored.

## Qualification plan

The dedicated E024 workflow does not trust hand-written fixture numbers. It reruns:

```text
E014 exhaustive surfaces
 -> E015 adaptive sampler
 -> E016 adversarial guard
 -> E017 certificate lifecycle
 -> E024 normalized certificate
```

on a GitHub-hosted runner and uploads the E024 certificate as evidence.

## Authority

- research observation only
- no external execution authority
- no production mutation
- no policy auto-apply
- `authority_effect = NONE`

## Claim ceiling

`MARKET_MICROCOSM_E015_E016_E017_AS_THIRD_INDEPENDENT_PROOF_CARRYING_WORK_REDUCTION_HOLDOUT_ONLY`
