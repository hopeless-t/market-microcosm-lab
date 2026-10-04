# ODD addendum — E070 prior-drift revocation

E069 earns a sequential evidence policy under one declared independent failure prior.

E070 attacks that prior.

The frozen E069 safe-path order is:

```text
gtm-pack
→ signed-strategy-gap-attestation
→ finance-pack
```

Under the reference prior it remains optimal.

Under a finance-heavy shift, the frozen policy costs **12.57375** in expectation, while recompilation selects finance first and reaches **8.8731875**. Regret is about **3.70**.

Under a strategy-heavy shift, recompilation selects the strategy attestation first. Frozen-policy regret is about **1.51**.

With a declared regret revocation threshold of 1.0, both shifted generations revoke E069 policy authority.

The result is not that E069 was wrong. Its certificate was scoped too broadly.

```text
policy authority
=
policy
+
cost model
+
authorization generation
+
prior generation
```

Promotion: `sequential-acquisition-policy-authority-is-prior-generation-scoped-v1`.
