# ODD addendum — E074 tight dependence ambiguity

E072 shows that one same-marginal correlated world can reorder E069.

E074 removes the need to choose one particular joint distribution.

The ambiguity set is:

```text
all joint distributions with the E069 axis marginals
```

For a set of already-observed axes (S), the largest possible probability that every axis in (S) is safe is:

```text
1 - max(p_i for i in S)
```

This Frechet upper bound is tight. A constructive witness uses one shared latent uniform variable and nested bad events: axis (i) is bad whenever (U < p_i).

That construction preserves every E069 marginal and simultaneously achieves the worst-case prefix-safe probability for every observation prefix.

All six complete bundle orders are evaluated.

The two GTM-first orders tie for the minimum tight worst-case expected cost:

```text
GTM -> strategy -> finance = 11.0
GTM -> finance  -> strategy = 11.0
```

Reference-prior efficiency breaks the tie:

```text
GTM -> strategy -> finance = 9.0225
GTM -> finance  -> strategy = 9.32385
```

So the selected dependence-ambiguity policy recovers E069's order, but now with a tight arbitrary-dependence worst-case certificate.

Promotion: `fixed-marginal-dependence-ambiguity-uses-frechet-minimax-order-v1`.
