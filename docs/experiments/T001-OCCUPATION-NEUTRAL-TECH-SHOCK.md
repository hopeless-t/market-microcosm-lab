# T001 — Occupation-neutral technology shock with human-viability divergence

## Trigger

The technology-shock / human-ecology program starts from a simple separation:

```text
occupation loss != aggregate contraction
aggregate expansion != human viability
```

T001 builds the smallest exact synthetic world that can demonstrate both inequalities at once.

The technology is deliberately unnamed. It can stand in for word processing, digital imaging, spreadsheets, industrial automation, AI, or another production-frontier shift.

## Frozen population

```text
total workers               = 100
legacy occupation workers   = 60
complement/incumbent workers= 40
baseline output             = 100 synthetic units
baseline household income   = 100 synthetic income units
```

Human viability requires:

```text
employment rate >= 90%
household income >= 90
```

These are synthetic thresholds, not empirical welfare recommendations.

## Frozen technology shock

The same shock is used in both transition worlds:

```text
legacy task cost after shock       = 10% of baseline
legacy human substitution rate     = 80%
legacy human demand                = 60 -> 12
technology-enabled legacy output   = 90 units
potential new human roles          = 50
```

The old occupation therefore loses 80% of its human headcount in **both** shock worlds.

Only one variable changes:

```text
transition / matching capacity
```

## Arm A — fast reallocation

All 48 displaced legacy workers can move into new/rebundled roles.

```text
legacy workers        = 12
transitioned workers  = 48
unemployed            = 0
employment rate       = 100%
household income      = 100
aggregate output      = 178
human viability       = PASS
```

The historical occupation largely disappears, yet the protected human population remains viable in this frozen world.

## Arm B — frictional transition

Only 20 of the 48 displaced workers can cross the retraining/matching bottleneck during the modeled horizon.

```text
legacy workers        = 12
transitioned workers  = 20
unemployed            = 28
employment rate       = 72%
household income      = 72
aggregate output      = 150
human viability       = FAIL
```

Aggregate output still rises by 50% relative to baseline, even while the protected human population falls outside the declared viability region.

## Exact counterexample

The two shock worlds share:

```text
same technology
same 80% legacy-task substitution
same automated output
same potential new-role surface
same population
```

but differ in transition capacity.

Therefore T001 constructs all of the following simultaneously:

```text
legacy occupation collapses in both worlds = TRUE
aggregate output expands in both worlds     = TRUE
human viability passes in only one world    = TRUE
```

So neither of these implications is valid:

```text
occupation collapse -> aggregate economic collapse
aggregate output growth -> successful human transition
```

## Why this matters

The relevant ecological object is not the historical job title. It is the human population moving through a changing task-production graph.

T001 therefore validates the core Market Microcosm framing:

> protect population viability and transition capability, not the continued existence of every historical occupation.

This is also why AI need not be represented as a synthetic person. The technology shock acts on task cost and substitution; humans then respond through a separate transition process.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = EXACT_SYNTHETIC_COUNTEREXAMPLE_ONLY
```

The output numbers, substitution rate, income floor, employment floor, and transition capacities are frozen synthetic values. T001 makes no claim about current AI employment effects, historical typists, photographers, or any real occupation.

## Next falsifier

T002 should attack T001’s easiest assumption: that new roles already exist and merely need workers to transition into them.

The next world should endogenize **demand expansion and role creation**. A productivity shock can lower prices and expand demand, but whether that expansion creates enough complementary human tasks should depend on demand elasticity and augmentability rather than being granted exogenously.

That creates the next boundary:

```text
productivity gain
+ potential complementarity
!=
guaranteed human-role creation
```
