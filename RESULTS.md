# Current results

Status: synthetic research evidence only. These results describe the declared repository models and seed banks; they are not empirical estimates for a named market.

## E000 — exact self-improvement kernel

The finite reference world continues to pass its exact viability checks and closed inner/meta-loop CI.

A representative v0.2 CI run converged the inner policy loop to reserve-balancer-t1. The outer machinery loop remained capable of changing search configuration.

## E010 — circulating ecological market

Neutral baseline:

- mechanisms: usage-only, light-floor, balanced, diversity-heavy, creator-heavy, platform-heavy;
- horizon: 60 months;
- neutral reporting seeds: 40;
- observed full-horizon survival: 1.0 for every mechanism.

This is an important negative result: the neutral world is too easy to reveal the viability boundary.

The E010 inner loop selected platform-heavy under its declared discovery/promotion design. The meta configuration selected long-compact.

## E011 — pressure knee

Composite pressure simultaneously reduces subscription price, raises platform operating cost, and raises baseline churn.

Preliminary first level with observed survival below 90%:

| Mechanism | Knee |
| --- | ---: |
| balanced | 4 |
| platform-heavy | 4 |
| usage-only | 3 |
| light-floor | 3 |
| diversity-heavy | 3 |
| creator-heavy | 3 |

Normalized survival-area across the tested pressure ladder:

| Mechanism | Survival AUC |
| --- | ---: |
| platform-heavy | 0.364 |
| balanced | 0.355 |
| light-floor | 0.282 |
| diversity-heavy | 0.273 |
| usage-only | 0.273 |
| creator-heavy | 0.268 |

Failure biopsy identified different collapse modes:

- balanced: platform insolvency;
- creator-heavy: platform insolvency;
- light-floor: platform insolvency;
- usage-only: platform insolvency;
- diversity-heavy: service quality below floor;
- platform-heavy: publisher population below floor plus service quality below floor.

This is the first direct evidence inside the model of the intended ecological trade-off: protecting one trophic layer can move failure into another layer.

## E012 — meta-improvement of evaluation design

Design selections:

| Evaluation curriculum | Mechanism selected |
| --- | --- |
| neutral-only | balanced |
| mild-curriculum | platform-heavy |
| boundary-curriculum | platform-heavy |

On the isolated outer stress holdout, mild-curriculum was the winning evaluation design and selected platform-heavy.

The wider boundary curriculum did not earn automatic preference. Search cost is an explicit tie-breaker, so extra evaluation pressure must buy additional generalization to justify itself.

## E013 — one-dimensional pressure decomposition

E013 held two E011 pressure components at baseline while sweeping the third.

Preliminary knees:

| Axis | usage-only | light-floor | balanced | diversity-heavy | creator-heavy | platform-heavy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| subscription price ↓ | 8 | 8 | 7 | 6 | 7 | 7 |
| platform operating cost ↑ | 9 | 10 | 10 | 10 | 6 | >10 |
| baseline churn ↑ | 6 | 6 | 6 | 6 | 6 | 6 |

Failure biopsy separated the mechanisms cleanly:

- churn alone eventually drives **user population below the floor** for every mechanism; diversity-heavy can also cross the service-quality floor;
- platform-cost pressure mostly causes **platform insolvency**; creator-heavy is especially fragile at level 6, while platform-heavy showed no knee through level 10;
- price pressure propagates through both sides of the ecosystem: some mechanisms end in platform insolvency, while balanced/diversity-heavy can lose service quality and platform-heavy can lose publishers plus service quality.

The strongest result is comparative: E011's composite pressure produced knees at levels 3–4, but no E013 single axis produced a knee before level 6. Inside the declared synthetic world, simultaneous moderate stresses therefore interact to advance collapse substantially.

## Theory update

The working theory after E010–E013 is:

1. neutral survival can saturate and become uninformative;
2. useful allocation comparisons require locating the viability boundary;
3. the location of the knee is not enough — failure time and failure mode also matter;
4. platform and creator protection form a genuine dynamic trade-off in the current model;
5. the evaluation curriculum is itself part of the control system and should be meta-optimized;
6. more stress testing is not monotonically better when a smaller curriculum generalizes equally well;
7. churn pressure is largely mechanism-insensitive once it dominates user population dynamics;
8. platform-cost pressure strongly exposes the platform-take trade-off;
9. revenue pressure can propagate from platform solvency into publisher/catalog/service-quality collapse;
10. the early E011 composite knee is not explained by any single component alone, so interaction effects are now a primary target.

Next work should map two-dimensional interaction surfaces around the localized E013 knees, then return to richer recommendation, pricing, bargaining, and causal-attribution controllers.
