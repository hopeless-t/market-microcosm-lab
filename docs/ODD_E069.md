# ODD addendum — E069 sequential evidence acquisition

E068 proves a decision-information lower bound but knows the reference world's failing axis.

E069 removes that oracle advantage.

Each warning axis receives a synthetic prior failure probability. Authorized evidence actions come from E067, including the finance and GTM bundles.

The controller may stop as soon as any acquired direct feature certifies WARN. If an action observes only safe axes, acquisition continues. SAFE is emitted only after all five axes are directly observed safe.

Exact dynamic programming over the set of already-safe axes selects:

```text
gtm-pack
→ if safe: signed-strategy-gap-attestation
→ if safe: finance-pack
```

Initial expected cost is **9.0225**.

A simple collection-cost bundle order:

```text
gtm-pack
→ finance-pack
→ signed-strategy-gap-attestation
```

has expected cost **9.32385**.

The static E067 full portfolio always costs **14**.

On the all-safe path the exact sequential policy still spends exactly 14, so SAFE authority is unchanged; savings come only from early WARN termination.

Promotion: `sequential-warning-acquisition-minimizes-expected-decision-cost-v1`.
