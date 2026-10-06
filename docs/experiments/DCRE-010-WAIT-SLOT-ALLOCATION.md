# DCRE-010 — Scarce waiting slots: cap, price, and essential exclusion

## Trigger

DCRE-009 turns waiting into a congestible shared resource. The obvious controls are a capacity cap or a congestion price.

Both can preserve the queue while allocating the scarce slot badly.

DCRE-010 freezes one waiting slot and four heterogeneous actors.

## Frozen actors

```text
PREMIUM
  arrival=0, budget=.20, private wait benefit=.08, system wait value=.08

ESSENTIAL
  arrival=1, budget=.03, private wait benefit=.02, system wait value=.50
  essential=true

ROUTINE
  arrival=2, budget=.10, private wait benefit=.06, system wait value=.06

BATCH
  arrival=3, budget=.08, private wait benefit=.05, system wait value=.05
```

All numbers are synthetic model units.

## Allocation rules

### FIFO_CAP

Take the first arrival until the one-slot cap is full.

```text
selected = PREMIUM
system wait value = .08
```

The queue is protected, but allocation ignores consequence.

### POSTED_PRICE

Set waiting-slot price `.05`. Actors whose budget is below the price cannot buy the slot; among eligible actors choose highest private wait benefit.

```text
ESSENTIAL budget .03 < price .05 -> excluded
selected = PREMIUM
system wait value = .08
```

The congestion price preserves scarcity but treats purchasing power/private benefit as the selection surface.

### SYSTEM_VALUE

Use the synthetic system-level wait value directly as an oracle benchmark.

```text
selected = ESSENTIAL
system wait value = .50
```

This is not offered as an implementable policy. It is a counterfactual showing that cap/price can miss a low-budget high-consequence actor.

## Result

```text
queue viability
!= allocation quality
private willingness/ability to pay
!= system value
```

A resource price can internalize congestion while simultaneously creating a distributional failure. This mirrors the original DCRE research note's `resource-price exclusion` failure biopsy.

## Important boundary

`system_wait_value` is known to the synthetic oracle. Real systems do not observe social value perfectly. The `essential` label can itself be strategic, noisy, political, or stale.

Therefore DCRE-010 does not authorize system-value scheduling or free essential access. It only constructs a world where price-only allocation is not sufficient for viability.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_PRICE_EXCLUSION_COUNTEREXAMPLE
```

## Next falsifier

DCRE-011 should attack the oracle `system_wait_value` / `essential` declaration. If actors can exaggerate urgency or if classification is noisy, protected allocation can be Goodharted just as verification was in DCRE-002.
