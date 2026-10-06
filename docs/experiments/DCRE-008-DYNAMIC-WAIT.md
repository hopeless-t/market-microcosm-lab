# DCRE-008 — Dynamic abstention and the value of waiting

## Trigger

DCRE-007 introduced `ABSTAIN` as a fixed-cost alternative to acting under imperfect dependency information. A fixed abstention cost hides an important market option: **wait for more information before deciding**.

Waiting is not free. It can preserve option value, but it can also consume time, queue capacity, deadline slack, and foregone utility.

DCRE-008 adds one explicit waiting step.

## Reused machinery

The immediate-action surface comes from DCRE-007. Nominal dependency risk still comes from E023. No new dependency-risk model is introduced.

## Frozen waiting contract

```text
probability useful dependency information arrives while waiting = 0.60
delay cost = 0.25
penalty if information fails to arrive before the decision point = 0.20
abandonment cost = 5.00
hidden prior = 0.50
mitigation cost = 0.50
```

If information arrives, the actor learns whether the hidden dependency exists and pays mitigation only in that branch. If information does not arrive, the actor reaches the next decision point with the best immediate active policy plus the deadline penalty.

The waiting cost is therefore:

```text
WAIT
 = delay_cost
 + q * perfect_information_action_cost
 + (1-q) * (best_immediate_active_cost + deadline_penalty)
```

The candidate actions are:

```text
ACT_NOW
WAIT
ABANDON
```

## Frozen regimes

```text
failure loss = 100     -> ACT_NOW
failure loss = 200     -> WAIT
failure loss = 20,000  -> WAIT
failure loss = 30,000  -> ABANDON
```

The result is qualitative rather than empirical: a waiting option creates an intermediate region where buying time for information is cheaper than immediate action or permanent abandonment.

At sufficiently high modeled downside, however, the residual risk and delay cost make waiting itself unattractive and abandonment dominates.

## Market interpretation

Time is another scarce input in the resource ecology.

```text
abstention
!= permanent abandonment
!= free safety
```

A market decision can consume:

- compute/resource budget;
- verification budget;
- exploration budget;
- evidence-independence budget;
- dependency-audit budget;
- **deadline / waiting budget**.

This also creates a new externality: many actors waiting for better evidence can accumulate queue pressure even when waiting is individually rational.

## Boundary

The information-arrival probability, costs, and one-step horizon are synthetic. Information is assumed perfect when it arrives. There is no queue interaction yet.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_ONE_STEP_WAIT_OPTION_COUNTEREXAMPLE
```

## Next falsifier

DCRE-009 should couple multiple waiting actors through a finite queue or deadline surface. Individually rational waiting may then create congestion, stale evidence, or deadline cascades, turning the value-of-wait option into another ecosystem-level externality.
