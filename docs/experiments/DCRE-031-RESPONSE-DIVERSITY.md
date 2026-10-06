# DCRE-031 — Response diversity damps but does not eliminate oscillation

## Trigger

DCRE-030 shows that a lagged congestion signal plus synchronized flexible demand produces a two-slot oscillation.

A common intuition is that heterogeneous actors may stabilize the market naturally because not everyone reacts at the same time.

DCRE-031 tests a minimal form of heterogeneity: **different update cadences**.

## Frozen actors

Four actors each control 10 flexible task-units.

```text
A0, A1 update on even epochs
B0, B1 update on odd epochs
```

Actors that do not update retain their previous allocation. Updating actors move toward the cheaper slot using the same lagged price rule as DCRE-030.

## Synchronized baseline

DCRE-030 full response:

```text
flexible A = 0,40,0,40,0,40
peak load = 80
movement = 200
```

## Staggered cadence

Frozen aggregate sequence:

```text
flexible A = 10,20,30,10,20,30
```

which produces:

```text
peak load = 70
movement = 60
```

## Result

```text
response diversity
-> lower synchronized movement
-> lower peak amplitude
!= convergence
```

Cadence diversity materially damps the frozen oscillation but does not eliminate cycling. The market moves through a three-state loop rather than converging to a fixed allocation.

This matters for control design: heterogeneity can be a stabilizing ecological feature without being a proof of dynamic stability.

## Boundary

Update phases are exogenous and perfectly balanced. There is no strategic timing, stochastic arrival, actor entry/exit, learning, or heterogeneous resource utility. The experiment does not claim that real-world heterogeneity has this exact effect.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_RESPONSE_DIVERSITY_DAMPING
```

## Next falsifier

DCRE-032 should add a large common shock. A diverse cadence may damp ordinary oscillation yet still synchronize under a sufficiently strong event if every actor crosses its response threshold at once. The next question is whether diversity provides graceful degradation or merely delays common-mode synchronization.
