# DCRE-026 — Invalidation risk can erase reuse amortization

## Trigger

DCRE-025 finds an exact reuse-count knee: on its frozen scalarized surface, a prepared compact representation becomes cheaper from the third use onward.

That result assumes the prepared representation remains valid.

DCRE-026 adds an independent probability `q` that the representation is invalidated between uses and must pay the preparation cost again.

## Frozen expected-cost model

Reuse the DCRE-025 synthetic costs:

```text
RAW cost per use          = 25
initial preparation cost  = 30
prepared cost per use     = 12
```

For `N` uses, expected rebuild count is:

```text
q * (N - 1)
```

so:

```text
RAW(N) = 25N
PREPARED(N,q) = 30 + 12N + 30q(N-1)
```

## Three-use world

Break-even invalidation probability:

```text
75 = 66 + 60q
q = .15
```

Examples:

```text
q=.10 -> PREPARED=72 < RAW=75
q=.20 -> PREPARED=78 > RAW=75
```

A representation that wins under stable reuse loses once invalidation crosses 15% per reuse boundary in this small world.

## Eight-use world

```text
200 = 126 + 210q
q = 74/210 ~= .35238
```

Examples:

```text
q=.30 -> PREPARED=189 < RAW=200
q=.40 -> PREPARED=210 > RAW=200
```

More reuse can tolerate more churn because the fixed preparation cost is spread over more successful services.

## Result

```text
reuse count
x stability
-> preparation viability region
```

Reuse alone is not enough. Durable/canonical/prepared representations are economically attractive only inside a joint **reuse × invalidation** region.

This also explains why lifecycle and revalidation triggers belong next to caching/materialization decisions: stale representations can turn an apparent communication optimization into repeated rebuild work.

## Boundary

The invalidation events are independent and homogeneous, and the expected-cost model ignores stale-use damage, detection latency, partial refresh, and differentiated atom-level invalidation.

The scalar cost weights remain synthetic.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_REUSE_STABILITY_KNEE
```

## Next physical falsifier

DCRE-027 should move from one prepared object to a finite cache/storage portfolio. With bounded resident storage, which reusable projections should stay near the workload, and when does request-frequency greedy lose to an exact value-per-storage allocation?
