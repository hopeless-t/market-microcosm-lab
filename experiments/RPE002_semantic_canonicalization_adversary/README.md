# RPE-002 — Semantic canonicalization adversary

## Question

RPE-001 assumed that multiple sparks can be canonicalized into the right underlying meaning. RPE-002 attacks that assumption.

The experiment asks:

> When canonicalization itself makes false-merge or false-split errors, can apparent work reduction hide loss of decision-relevant semantics?

## Fixture

Eight synthetic sparks represent five ground-truth meanings. Each spark carries:

- a shallow `surface_topic`;
- a stronger synthetic `invariant_key`;
- one or more downstream decision-value obligations.

The fixture intentionally contains both adversaries:

1. two `working-set` sparks have different surface topics (`memory` vs `cache`), so topic-only grouping falsely splits one meaning;
2. `resource-rebound` and `proof-status` share the surface topic `efficiency`, so topic-only grouping falsely merges two meanings.

The invariant keys are deliberately constructed to separate those cases. They are an experimental oracle-like signal, not a claim that a production system already knows the right invariants.

## Policies

### Ground-truth reference

Groups sparks by declared true meaning. This is the cost and semantic-fidelity reference only.

### Surface-topic canonicalizer

Groups by shallow topical similarity.

It can look efficient because every downstream obligation still has a nominal materialized projection, while an ambiguous merged cluster silently loses verified semantic value.

### No-merge fail-closed

Every spark remains separate. This avoids false merges but duplicates work when multiple sparks truly represent the same meaning.

This is the safety baseline: uncertainty can be handled by refusing to merge, but the price is additional review/materialization cost.

### Invariant-guarded canonicalizer

Groups only when the synthetic invariant key matches. In this fixture it recovers the declared ground-truth grouping.

This is a candidate mechanism for study, not evidence that invariant extraction is solved in real repositories.

## Metrics

- canonical object count;
- downstream materialization count;
- review cost;
- false-merge pair count;
- false-split meaning count;
- duplicate semantic projections;
- nominal decision-value coverage;
- verified decision-value coverage;
- semantic value loss.

The critical distinction is:

```text
nominal projection exists
!=
verified semantic obligation preserved
```

## Expected synthetic result

The topic-only arm should simultaneously produce a false merge and a false split. It should retain 100% nominal decision-value coverage while verified coverage falls below 100%.

The no-merge arm should retain full verified value at a cost premium.

The invariant-guarded arm should match the ground-truth reference in this deliberately constructed fixture.

## Candidate rule

```text
MERGE_ONLY_WITH_SEMANTIC_EQUIVALENCE_EVIDENCE
OTHERWISE_FAIL_CLOSED_TO_SEPARATE_MEANINGS
```

This refines RPE-001:

```text
canonicalize once
```

is not sufficient. The canonicalization boundary itself needs evidence and a reversible split path.

## Claim ceiling

`DETERMINISTIC_SYNTHETIC_SIGNATURE_FIXTURE_ONLY_NO_REAL_CANONICALIZER_ACCURACY_CLAIM`

The experiment does not estimate production clustering accuracy, semantic-embedding quality, or real review savings. The next falsifiers should inject noisy/partial invariants, stale semantic signatures, and sampled real repository history.
