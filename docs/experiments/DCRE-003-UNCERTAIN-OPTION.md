# DCRE-003 — Uncertain option value and exploration knee

## Why DCRE-002 still had an oracle

DCRE-002 preserved exploratory probes by assigning each probe an explicit synthetic option value. That is useful as a constructive counterexample, but an exact scheduler that knows true option value in advance has an information advantage unavailable to a real decision-maker.

DCRE-003 removes that advantage.

A probe now consumes the current period and only reveals whether a higher-value future opportunity exists.

## Two-period world

Frozen values:

```text
safe utility now    = 4
safe utility later  = 4
high-state utility later = 12
p = prior probability of the high state
```

Policies:

### SAFE

Do not explore.

```text
SAFE = 4 + 4 = 8
```

### EXPLORE

Spend the current period on the probe. If the hidden state is high, receive 12 later; otherwise fall back to 4.

```text
EXPLORE = p*12 + (1-p)*4
        = 4 + 8p
```

### ORACLE

A benchmark with perfect state information and no probe cost:

```text
ORACLE = 4 + p*12 + (1-p)*4
       = 8 + 8p
```

The oracle is not an attainable policy. It is only a regret ceiling.

## Exact exploration knee

Compare SAFE and EXPLORE:

```text
4 + 8p > 8
p > 0.5
```

Therefore:

- `p < 0.5`: exploring destroys expected utility in this frozen world;
- `p = 0.5`: exploration and safe exploitation tie;
- `p > 0.5`: refusing to explore destroys expected utility.

The result is deliberately symmetric and simple. Its role is to prove that `preserve option value` cannot mean `always explore`.

## Frozen prior grid

```text
p=0.00 -> SAFE
p=0.25 -> SAFE, SAFE=8, EXPLORE=6
p=0.50 -> TIE,  SAFE=8, EXPLORE=8
p=0.75 -> EXPLORE, EXPLORE=10, ORACLE=14
p=1.00 -> EXPLORE, EXPLORE=12, ORACLE=16
```

## Market interpretation

After cheap generation creates abundant candidate work, the ecosystem has at least three scarce resources:

```text
compute / generation
verification
actionable information about future value
```

DCRE-001 constrained the first two. DCRE-002 showed that verification cannot safely stand in for utility. DCRE-003 adds a third scarcity: learning which currently-unverified directions are worth preserving.

This creates a genuine exploration/exploitation market rather than a static admission gate.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = EXACT_TWO_PERIOD_SYNTHETIC_INFORMATION_VALUE_BOUNDARY
```

The prior and utilities are synthetic. The result does not estimate real R&D returns, AI-agent exploration value, or data-center policy.

## Next falsifier

DCRE-004 should remove the single known prior. Competing actors should hold different, possibly miscalibrated beliefs and update from delayed noisy observations. The key question becomes whether a market of heterogeneous beliefs preserves useful diversity or burns resources through correlated over-exploration.
