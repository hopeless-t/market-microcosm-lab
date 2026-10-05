# ODD addendum — E075 marginal intervals × arbitrary dependence

E074 fixes the E069 marginals exactly and allows arbitrary dependence.

E075 also makes the marginals uncertain:

```text
cash gap       [0.03, 0.08]
delivery       [0.07, 0.15]
headroom       [0.20, 0.40]
funnel         [0.12, 0.25]
strategic exit [0.15, 0.35]
```

For evidence-collection cost, the adversarial direction is counterintuitive.

Higher failure probability often makes WARN appear earlier and **reduces** collection cost.

The worst SAFE-path continuation therefore uses the **lower failure bounds**.

For any observed prefix (S):

```text
max P(all S safe)
=
1 - max(lower failure probability in S)
```

A nested bad-event construction at the lower marginals attains the bound, so it is tight.

All six bundle orders are evaluated. Both GTM-first orders tie at tight worst-case expected cost **12.0**.

Reference-prior efficiency again breaks the tie in favor of:

```text
GTM -> strategy -> finance
```

Promotion: `interval-marginal-dependence-ambiguity-uses-lower-risk-frechet-bound-v1`.
