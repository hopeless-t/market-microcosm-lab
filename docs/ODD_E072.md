# ODD addendum — E072 marginal priors do not identify joint policy

E069/E070 use axis-level failure probabilities.

E072 keeps **every one of those marginals unchanged** and changes only the joint dependence structure.

The finite joint world contains:

- all safe: 0.37
- funnel only bad: 0.18
- headroom only bad: 0.05
- headroom + strategic-exit bad: 0.25
- delivery-margin only bad: 0.10
- cash-gap only bad: 0.05

The resulting marginals are exactly:

```text
cash gap       0.05
delivery       0.10
headroom       0.30
funnel         0.18
strategic exit 0.25
```

which matches E069.

But headroom and strategic exit now co-fail with probability 0.25 rather than the independent product 0.075.

The frozen E069 safe-path order:

```text
GTM → strategy → finance
```

costs **9.20** under this joint world.

A joint-aware exact DP chooses:

```text
GTM → finance → strategy
```

at **8.45**.

Regret is **0.75** despite identical marginals.

The reason is conditional information: after GTM is observed safe, strategic-exit risk changes because the axes are dependent.

Promotion: `sequential-acquisition-requires-joint-failure-model-not-marginals-only-v1`.
