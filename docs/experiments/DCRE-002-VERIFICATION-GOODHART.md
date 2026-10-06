# DCRE-002 — Verification Goodhart and option value

## Why DCRE-001 is not enough

DCRE-001 showed that a finite verification ceiling can make extra generation consume resource without raising independently checked output. A natural correction is to gate work by verification capacity.

That correction can itself become a proxy trap.

```text
verification capacity
!= verified count
!= verified utility
!= future option value
```

DCRE-002 constructs a tiny exact counterexample.

## Frozen work portfolio

Budgets:

```text
resource budget = 12
verification budget = 8
```

Work items:

```text
E1, E2  mandatory essential work
        resource=3, verification=4, verified utility=12 each

R1..R4 routine easy work
        resource=1, verification=1, verified utility=2 each

P1, P2  exploratory probes
        resource=2, verification=0, immediate verified utility=0,
        explicit synthetic option value=6 each
```

The probe option value is a model variable. It is not a claim that real unverified AI work has a known positive value.

## Policies

### VERIFIED_COUNT_GATE

Admit only verification-requiring work and prefer the lowest verification cost first.

Frozen result:

```text
selected = R1,R2,R3,R4,E1
resource = 7
verification = 8
verified utility = 20
option value = 0
mandatory complete = false
```

The policy produces more verified task count while dropping one mandatory essential item.

### VERIFIED_UTILITY_GATE

Admit only verification-requiring work but rank by verified utility per verification unit.

Frozen result:

```text
selected = E1,E2
resource = 6
verification = 8
verified utility = 24
option value = 0
mandatory complete = true
```

This repairs the mandatory-work failure but treats all non-immediately-verifiable exploration as zero-value.

### OPTION_PRESERVING_EXACT

Enumerate the small portfolio exactly, require all mandatory work, obey both budgets, and maximize:

```text
verified utility + declared option value
```

Frozen result:

```text
selected = E1,E2,P1,P2
resource = 10
verification = 8
verified utility = 24
option value = 12
total modeled value = 36
mandatory complete = true
```

## Result

The experiment is a constructive failure of the rule:

> maximize verified task count

and a narrower failure of:

> admit only work that can produce immediate verified utility

A verification gate is still useful as a safety/evidence boundary, but it must not silently become the ecosystem's utility function.

## Market Microcosm interpretation

Verification is a scarce production factor. If it is priced or scheduled badly, the market can select for work that is easy to verify rather than work that preserves essential service, long-run learning, diversity, or option value.

This creates a second rebound-like loop:

```text
cheap generation expands
 -> verification becomes scarce
 -> scheduler rewards easy-to-certify work
 -> hard but essential work is crowded out
 -> exploration can disappear
 -> measured verified throughput rises while ecosystem viability falls
```

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = CONSTRUCTIVE_SYNTHETIC_COUNTEREXAMPLE
```

The item utilities and option values are intentionally synthetic. DCRE-002 proves only that the proxy failure is possible in the model, not how common or important it is in real AI infrastructure.

## Next falsifier

DCRE-003 should make option value uncertain rather than known. If exact scheduling is given true option values by construction, it has an oracle advantage. The next world should hide probe quality ex ante and compare exploration policies under regret, delayed evidence, and bounded verification.
