# ODD addendum — E047 freshness and metric-generation alignment

## Purpose

Attack E046's remaining assumption.

E046 correctly filters unauthorized observations before active-sensing cost optimization.

But authorized evidence can still be inadmissible for the current decision if it is stale or belongs to an older metric-definition generation.

## Reference

Decision context:

```text
decision period = 3
maximum evidence age = 1 period
required metric generation = mrr-v2
```

Candidates include:

- a stale but correctly-versioned signed attestation;
- a fresh but old-generation attestation;
- a fresh current-generation attestation;
- a fresh exact current-state query.

If the optimizer checks only authorization and predicate resolution, it selects the lowest-cost authorized evidence: the fresh old-generation attestation.

That evidence is inadmissible because its metric identity no longer matches the requested decision.

## Correct admission order

```text
authorized?
→ resolves predicate?
→ fresh enough for this decision?
→ same metric-definition generation?
→ then minimize collection cost
```

The selected reference evidence becomes the fresh current-generation predicate attestation.

## Relation to E027

E027 showed that public Game Pass values cannot be forced into one time series across metric-definition changes.

E047 applies the same identity principle to active sensing.

A metric generation is part of evidence identity at acquisition time, not merely a documentation field used later.

## Promotion rule

`active-sensing-evidence-must-be-fresh-and-generation-aligned-v1`

## Limitation

The period scale and one-period freshness budget are synthetic. Real freshness requirements depend on the decision's hazard rate and the provider's update semantics.
