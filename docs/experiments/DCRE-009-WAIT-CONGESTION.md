# DCRE-009 — Waiting congestion as a market externality

## Trigger

DCRE-008 gives a single actor a dynamic waiting option. At the frozen `failure_loss=200`, waiting is individually cheaper than acting immediately:

```text
base WAIT cost ~= 0.816970
ACT_NOW cost  ~= 0.839469
```

If many actors share the same decision surface, however, waiting can consume a shared queue, deadline, or review surface.

DCRE-009 adds one deliberately simple congestion externality.

## Frozen market

```text
actors = 4
failure loss = 200
congestion penalty = 0.05 per other waiter
```

For `w` simultaneous waiters:

```text
per_waiter_cost = base_wait_cost + 0.05 * (w - 1)
```

Actors who do not wait pay the DCRE-008 `ACT_NOW` cost.

## Exact allocation sweep

```text
waiters=0 -> total cost ~= 3.357877
waiters=1 -> total cost ~= 3.335377
waiters=2 -> total cost ~= 3.412878
waiters=3 -> total cost ~= 3.590378
waiters=4 -> total cost ~= 3.867879
```

The exact minimum is **one waiter**.

Yet if every actor independently evaluates only the uncongested single-actor comparison, every actor prefers WAIT because `0.816970 < 0.839469`. The resulting four-waiter state is collectively worse than all actors acting now.

## Market interpretation

This is a synthetic congestion game:

```text
individually rational wait
 -> common WAIT choice
 -> queue / deadline congestion
 -> waiting cost rises
 -> collective outcome worsens
```

The policy implication is not that waiting should be centrally prohibited. The important missing object is the **shadow price of shared waiting capacity**.

A market that exposes congestion cost can make actors internalize the externality, while a market that presents each actor with an uncongested private WAIT price induces herding.

## Boundary

The congestion function is linear and synthetic. There is no strategic anticipation, heterogeneous deadline, queue service process, or stochastic arrival process yet.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_WAITING_CONGESTION_COUNTEREXAMPLE
```

## Next falsifier

DCRE-010 should compare fixed admission caps, congestion prices, and deadline-aware allocation. A static cap may prevent queue collapse but can allocate scarce waiting slots to low-value actors; a price may preserve throughput while excluding low-budget essential actors.
