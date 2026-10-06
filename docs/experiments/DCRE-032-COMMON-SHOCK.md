# DCRE-032 — Response diversity can collapse under a common shock

## Trigger

DCRE-031 shows that heterogeneous update cadence lowers peak amplitude and total movement in a lagged-price oscillation.

That result may tempt a stronger claim: diversity itself stabilizes the market.

DCRE-032 attacks that claim with a shared shock large enough to cross every actor's response threshold.

## Frozen actors

Four actors each control 10 flexible task-units and begin from a balanced split.

```text
T05 threshold = 5
T10 threshold = 10
T15 threshold = 15
T20 threshold = 20
```

If slot A becomes more expensive than slot B by more than an actor's threshold, that actor moves its A-half to B.

## Moderate shock

```text
price gap = 12
```

Only `T05` and `T10` react.

```text
active responders = 2 / 4
flexible A = 10
load A = 50
load B = 70
peak = 70
```

Threshold diversity limits synchronized motion.

## Large common shock

```text
price gap = 25
```

Every threshold is crossed.

```text
active responders = 4 / 4
flexible A = 0
load A = 40
load B = 80
peak = 80
```

The diversity that damped the moderate event disappears at the response surface induced by the larger shared shock.

## Result

```text
heterogeneous thresholds
!= independent failure domains
```

Diversity can be state-dependent. Actors that behave differently under ordinary conditions can become perfectly synchronized when the same large event crosses all of their local thresholds.

This is the physical-market analogue of hidden common-mode dependence: apparent heterogeneity is not enough; the system must ask what perturbations make the population respond in the same direction at once.

## Boundary

The shock is one-dimensional, actors are identical except for thresholds, and all responses have the same direction and size. There is no stochastic learning, strategic anticipation, geography, or real tariff model.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_COMMON_SHOCK_DIVERSITY_COLLAPSE
```

## Next direction

Do not recursively build another diversity controller. The next higher-information branch should return to the market's external resource environment: shocks to grid/water availability, provider adaptation, and cross-region substitution under correlated stress.
