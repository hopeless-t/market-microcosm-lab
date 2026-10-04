# ODD addendum — E073 robust order survives, regret bound does not

E072 adds a same-marginal joint-dependence adversary.

E073 inserts that adversary into E071's admitted uncertainty set and reruns all six complete-coverage bundle orders.

The minimax order remains:

```text
strategy
→ finance
→ GTM
```

Worst-case expected cost remains **11.315**.

So the E071 **policy order survives**.

But the new joint scenario costs 11.15 under that order, and its scenario-specific oracle costs 8.45. The expanded worst-case regret becomes **2.70**, up from E071's **2.2925**.

Therefore two authorities separate:

```text
policy identity authority: RETAINED
performance-bound authority: REISSUED
```

A new adversarial scenario does not need to change the winning policy to invalidate its old certificate metrics.

Promotion: `robust-policy-order-and-performance-bound-have-separate-authority-v1`.
