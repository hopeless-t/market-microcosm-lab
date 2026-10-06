# DCRE-007 — Imperfect dependency audit and abstention

## Trigger

DCRE-006 treated dependency audit as perfect. That makes the audit decision a simple expected-cost knee.

DCRE-007 weakens the audit itself. The audit can miss a hidden common mode, can raise false positives, can incur mitigation cost, and the system may abstain instead of proceeding.

The hidden/nominal risk models are still reused from E023.

## Frozen parameters

```text
hidden prior        = 0.50
audit sensitivity   = 0.90
false-positive rate = 0.05
audit fixed cost    = 0.50
mitigation cost     = 0.50
abstention cost     = 5.00
shock probability   = 0.01
```

The costs are synthetic model units.

## Actions

### UNAUDITED

Proceed using the mixture of nominal and hidden-common-mode risk.

### AUDIT

Pay the audit cost. When hidden dependency exists, the audit detects it with probability equal to sensitivity and mitigation reduces risk to the nominal model. Missed hidden dependencies retain hidden risk. False positives on nominal worlds trigger unnecessary mitigation cost.

### ABSTAIN

Pay the fixed opportunity cost of not proceeding.

## Frozen regimes

```text
failure loss = 100    -> UNAUDITED
failure loss = 200    -> AUDIT
failure loss = 8,000  -> AUDIT
failure loss = 10,000 -> ABSTAIN
```

The important result is qualitative: once the audit is imperfect, risk management has at least three regimes rather than a single audit/no-audit threshold.

## Market interpretation

Dependency information has its own quality and failure modes. Buying more evidence can be rational over an intermediate loss range, while sufficiently catastrophic downside can make abstention cheaper than either unaudited action or imperfectly audited action.

```text
more evidence
!= safe enough to act
```

The market must price:

- action risk;
- information quality;
- audit cost;
- mitigation cost;
- and the option value/cost of abstention.

## Boundary

The prior, audit quality, costs, and abstention value are synthetic. This experiment does not estimate real infrastructure audit effectiveness or real incident loss.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_THREE_REGIME_IMPERFECT_AUDIT_COUNTEREXAMPLE
```

## Next falsifier

DCRE-008 should make abstention itself dynamic rather than a fixed cost. Delaying action can preserve option value but can also accumulate queue pressure, foregone utility, and deadline risk.
