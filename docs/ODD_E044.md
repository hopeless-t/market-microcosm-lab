# ODD addendum — E044 robust abstention at decision boundaries

## Purpose

Turn E043's predicate ambiguity into an explicit control behavior.

E043 shows that the same uncertainty interval can be sufficient for one predicate and insufficient for another.

The dangerous next step would be to collapse the interval to a midpoint and force a binary answer anyway.

E044 tests that shortcut.

## Reference

For the E043 exact-boundary case:

```text
newest MRR in [1.5, 2.5]
decision threshold = 2
```

The interval contains compatible states on both sides of the threshold.

A midpoint proxy is 2.0 and therefore a naive `midpoint >= 2` rule returns TRUE.

But MRR=1.5 is also compatible with the evidence and gives FALSE.

The forced midpoint decision is therefore unsound.

## Robust rule

For an uncertainty interval (I) and threshold (T):

```text
if every x in I satisfies x >= T:
    CERTIFIED_TRUE

elif every x in I satisfies x < T:
    CERTIFIED_FALSE

else:
    ABSTAIN
```

The E043 interval correctly returns **ABSTAIN**.

Clearly separated intervals still produce ordinary decisions.

## Control consequence

ABSTAIN is not a failure mode.

It is an authorized output indicating that the current evidence plane cannot support the requested predicate.

The next observation request should be targeted only at resolving that predicate, rather than collecting arbitrary additional state.

## Promotion rule

`boundary-straddling-uncertainty-must-abstain-v1`

## Limitation

This reference uses one scalar threshold and symmetric consequence semantics. Real control systems may require asymmetric loss, multiple objectives, or explicit hysteresis bands.
