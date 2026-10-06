# DCRE-011 — Goodharting protected access claims

## Trigger

DCRE-010 constructs a price-exclusion counterexample: a low-budget but high-consequence ESSENTIAL actor can lose a scarce waiting slot to a higher-budget actor.

A natural correction is protected access for essential actors.

Protection labels are themselves incentives.

DCRE-011 attacks the assumption that `essential=true` is trustworthy.

## Frozen claims

```text
PREMIUM
  arrival=0
  true_essential=false
  claimed_essential=true
  evidence=.20
  system wait value=.08

ESSENTIAL
  arrival=1
  true_essential=true
  claimed_essential=true
  evidence=.90
  system wait value=.50

ROUTINE
  arrival=2
  true_essential=false
  claimed_essential=false
  evidence=.80
  system wait value=.06
```

All values are synthetic.

## Policies

### TRUST_CLAIM

Take the first actor claiming protected status.

```text
selected = PREMIUM
true essential = false
system wait value = .08
```

The protected lane is Goodharted by the incentive to self-classify as essential.

### EVIDENCE_GATE

Require `claimed_essential=true` and evidence score at least `.80`, then choose the highest frozen system value among qualified claims.

```text
selected = ESSENTIAL
system wait value = .50
```

In this frozen world, the gate matches the truth oracle.

### TOO_STRICT_GATE

At threshold `.95`, no protected actor qualifies. The implementation fails closed rather than silently reclassifying a claimant.

## Result

```text
protected status
!= truthful status
!= evidence-qualified status
```

Distributional safeguards create their own attack surface. A policy that fixes price exclusion by trusting self-reported urgency can simply move the scarcity contest into label acquisition.

## Important boundary

The evidence score is itself an oracle-like synthetic input. Real evidence can be correlated, forgeable, delayed, politically defined, or systematically harder for disadvantaged actors to produce.

DCRE-011 therefore closes this information/allocation mini-chain rather than recursively inventing another governance layer. The unresolved evidence-production problem remains explicitly open, but foreground research returns to physical resource ecology.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_PROTECTED_LABEL_GOODHART_COUNTEREXAMPLE
```

## Chapter handoff

DCRE-001–011 established a recurring pattern:

```text
resource control
 -> allocation rule
 -> local success
 -> new proxy / distribution / information failure
```

The next foreground experiment is **DCRE-012 capacity race**: return to physical capacity and test whether efficiency savings are reabsorbed when providers expand capacity up to an old resource ceiling.
