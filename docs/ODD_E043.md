# ODD addendum — E043 decision-sufficient observability

## Purpose

Repair E041 after E042 introduces reporting-resolution uncertainty.

E041 showed that one outgoing boundary MRR restores exact one-step reconstruction when the rolling ARR values are exact.

With rounded empirical ARR values, that reconstruction becomes an interval rather than a point.

E043 asks a more useful question:

```text
Do we need the exact hidden state,
or only enough information to make the downstream decision?
```

## Rounded reference

Use the E041 displayed values:

```text
previous ARR = 60
current ARR = 44
outgoing boundary MRR = 10
```

Treat the ARR values as nearest-unit displays:

```text
previous ARR in [59.5, 60.5]
current ARR in [43.5, 44.5]
```

If the boundary checkpoint is exact, interval propagation gives:

```text
newest MRR in [1.5, 2.5]
```

If the boundary itself is also rounded to the nearest unit:

```text
outgoing MRR in [9.5, 10.5]
newest MRR in [1.0, 3.0]
```

Exact state recovery is no longer authorized.

## Predicate-scoped authority

Now ask different decisions.

### Is the component active?

```text
newest MRR > 0
```

Both compatible-state intervals are entirely above zero.

The decision is therefore **CERTIFIED_TRUE** despite point-state uncertainty.

### Is newest MRR at least 2?

```text
newest MRR >= 2
```

Both intervals straddle the threshold.

The decision is **AMBIGUOUS**.

## Consequence

Observability is not one global property.

It is relative to the downstream predicate.

The correct contract is:

```text
uncertainty set
+ decision predicate
→ same answer for every compatible state?
    yes: decision-authoritative
    no: ambiguous / obtain more evidence
```

This lets the system avoid both failure modes:

- inventing a precise latent state that the evidence does not support;
- collecting unnecessary full-state detail when a coarse decision is already certified.

## Promotion rule

`observability-authority-is-decision-predicate-scoped-v1`

## Limitation

The reference uses simple independent rounding intervals. More complex measurement noise or changing metric definitions enlarge the compatible-state set and can revoke a previously certified predicate.
