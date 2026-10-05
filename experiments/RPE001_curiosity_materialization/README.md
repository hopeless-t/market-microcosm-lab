# RPE-001 — Curiosity Admission vs Downstream Materialization

## Question

Can a research ecosystem keep curiosity admission unconstrained while reducing downstream review/materialization work without suppressing currently decision-relevant semantic projections?

This experiment deliberately separates two resources:

```text
curiosity supply       -> unconstrained in the fixture
review/materialization -> scarce and explicitly costed
```

The experiment is the first `RPE-*` lane. It does **not** consume the existing `E024+` namespace, which is already contested by several open research branches.

## Fixture

Ten synthetic sparks collapse into seven canonical meanings. Some sparks are semantic duplicates with overlapping candidate repositories. Ten unique meaning/repository edges are currently decision-relevant. One canonical meaning has no current demand and therefore represents dormant option value.

Repository destinations have deterministic synthetic review costs. Demand edges carry deterministic decision values. These values are fixture parameters, not measurements of real hopeless-t repositories.

## Policies

### DIRECT_FANOUT

Every spark materializes work in every candidate repository.

This is intentionally permissive and guarantees current demand coverage if candidate routing is complete, but repeated sparks can materialize the same meaning/repository edge more than once.

### HARD_ONE_PROJECTION_PER_SPARK

Every spark may materialize only its first candidate destination.

This is the naive anti-overload baseline: it reduces work by suppressing materialization rather than separating intake from promotion.

### CANONICAL_ON_DEMAND

All sparks are admitted and canonical meanings are retained, but only unique currently demanded meaning/repository edges materialize.

Dormant meanings remain canonical state rather than becoming downstream work.

### CANONICAL_EXACT_BUDGET

The same canonical demand graph is placed under a bounded synthetic review budget. Exact subset enumeration maximizes declared decision value under that budget while retaining the full canonical meaning set.

This arm tests constrained allocation, not real scheduling performance.

## Metrics

- admitted sparks;
- canonical meanings retained;
- materializations and duplicate materializations;
- synthetic review cost;
- current demand-edge coverage;
- decision-value coverage;
- canonical dormant meanings retained.

## Promotion gate

The fixture supports the candidate rule only if all of these hold:

1. all policies admit the same curiosity supply;
2. canonical on-demand preserves 100% of current demand edges;
3. canonical on-demand costs less than direct fan-out;
4. canonical on-demand removes duplicate materialization;
5. the naive hard cap demonstrates at least one suppression failure;
6. the exact budgeted policy stays inside its declared review budget;
7. canonical storage retains at least one dormant meaning without materializing it.

## Claim ceiling

```text
DETERMINISTIC_SYNTHETIC_FIXTURE_ONLY_NO_REAL_REPOSITORY_PRODUCTIVITY_CLAIM
```

RPE-001 does not establish that Curiosity Intake improves real productivity, that canonicalization overhead is negligible, or that semantic clustering is correct in the wild. Those require measured follow-up experiments against the actual cross-repository corpus.

## Next falsifiers

- charge canonicalization, retrieval, clustering, and stale-projection costs;
- inject wrong semantic merges and wrong semantic splits;
- make decision demand arrive after dormancy and measure wake/revalidation cost;
- replay a sampled subset of the real cross-repository PR/commit corpus;
- compare direct fan-out, Curiosity Intake, and bounded portfolio allocation with measured human/context/API costs;
- test whether excessive central canonicalization creates a common-mode failure domain.

The intended direction is not `centralize everything`. It is to identify a viability region between uncontrolled materialization and over-centralized suppression.
