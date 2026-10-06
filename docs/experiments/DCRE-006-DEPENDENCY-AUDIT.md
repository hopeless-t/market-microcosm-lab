# DCRE-006 — Pricing a hidden-dependency audit

## Trigger

DCRE-005 separates nominal witness count from independent evidence domains, but it still assumes domain identity is known.

E023 already provides a synthetic hidden-common-mode adversary. DCRE-006 does not invent a new dependency model; it reuses E023's exact forge probabilities and asks an economic question:

> When is it worth paying to audit dependency structure?

## Reused E023 risks

With the frozen E023 shock probability 0.01:

```text
nominal independent forge risk ~= 0.0000098506
hidden common-mode forge risk  ~= 0.0100097521
risk delta                     ~= 0.0099999015
```

These are synthetic model probabilities, not empirical infrastructure risks.

## Audit decision

Let:

```text
L = modeled loss if the forged state occurs
A = dependency-audit cost
```

The unaudited expected cost is:

```text
C_unaudited = hidden_risk * L
```

A perfect audit is modeled as removing the hidden-common-mode excess risk while leaving nominal risk:

```text
C_audited = A + nominal_risk * L
```

Audit is preferred when:

```text
A < (hidden_risk - nominal_risk) * L
```

Therefore the exact synthetic loss knee is:

```text
L* = A / risk_delta
```

For `A=1`:

```text
L* ~= 100.000985
```

Frozen examples:

```text
L=50  -> UNAUDITED
L=100 -> UNAUDITED
L=101 -> AUDIT
L=200 -> AUDIT
```

## Market interpretation

The result rejects two symmetric slogans:

```text
"always audit independence"
"dependency audits are overhead"
```

The value of the audit depends on the modeled risk reduction multiplied by the modeled consequence of failure.

This makes dependency knowledge itself a priced information good inside the resource ecology.

## Important boundary

The audit is unrealistically perfect in DCRE-006. Real audits can have false negatives, false positives, delay, partial coverage, strategic disclosure failures, and their own shared dependencies. Those are deliberately excluded here.

The failure loss is also synthetic. DCRE-006 proves only the existence and location of a decision knee in the frozen model.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_EXPECTED_COST_KNEE_REUSING_E023
```

## Next falsifier

DCRE-007 should make the audit imperfect and adversarial. The market must then compare another witness, another failure domain, a partial audit, or abstention under uncertain audit quality.
