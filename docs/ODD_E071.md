# ODD addendum — E071 minimax prior-set acquisition

E070 shows that one-prior E069 authority is brittle under distribution shift.

E071 does not guess which of the three admitted prior generations will occur. Instead, every permutation of the three E067 evidence bundles is evaluated across all three priors.

There are exactly six fixed safe-path orders.

The minimax order is:

```text
signed-strategy-gap-attestation
→ finance-pack
→ gtm-pack
```

Its worst-case expected cost is **11.315** and worst-case regret versus a per-scenario oracle is **2.2925**.

The frozen E069 order has worst-case expected cost **12.57375** and worst-case regret **3.7005625**.

Robustness is not free. Under the original reference prior, the minimax order costs 11.315 versus E069's 9.0225.

The trade-off is explicit:

```text
single-prior efficiency
vs
prior-set robustness
```

The all-safe realized collection cost remains 14 in either order.

Promotion: `uncertain-prior-sequential-acquisition-uses-minimax-order-v1`.
