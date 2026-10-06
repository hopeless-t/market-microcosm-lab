# DCRE-013 — Endogenous provider investment and scarcity pricing

## Trigger

DCRE-012 shows that unit-efficiency savings can be reinvested into capacity until the old resource ceiling is filled again.

DCRE-013 removes the exogenous capacity choice. A synthetic provider chooses capacity from a discrete grid to maximize modeled profit.

## Frozen provider world

```text
efficiency ratio e       = .60
demand elasticity eta    = 1.50
baseline capacity         = 100
verification capacity     = 120
capacity choices          = 100,120,...,220
task revenue              = 1.0
capacity cost             = .15 per added capacity unit
fixed resource unit price = .20
```

The scarcity-price arm adds a quadratic congestion charge above synthetic resource use 72:

```text
resource bill = .20 R + .03 * max(0, R - 72)^2
```

These are synthetic coefficients chosen to produce a small falsifiable world, not empirical estimates.

## Arm A — fixed resource price + volume revenue

The provider earns revenue for every served task and faces a flat resource price.

The exact choice on the frozen grid is:

```text
capacity ~= 220
served   ~= 215.166
resource ~= 129.099
verified = 120
```

Unit efficiency improved, yet profit-seeking capacity expansion drives total resource use above the original baseline resource level 100.

This is a synthetic Jevons backfire with endogenous investment.

## Arm B — scarcity resource price + volume revenue

With congestion pricing above resource 72:

```text
selected capacity = 160
resource          = 96
verified          = 120
```

Scarcity pricing suppresses the race below baseline resource use, but the provider still builds beyond the independent verification capacity.

## Arm C — scarcity price + verified-output revenue

When revenue is earned only for independently verified output:

```text
selected capacity = 120
resource          = 72
verified          = 120
```

The same verified output is produced as Arm B with less physical capacity and resource use.

## Result

```text
resource pricing
!= capacity-purpose alignment
```

A dynamic physical-resource price can internalize one externality while leaving another scarcity invisible. If revenue still rewards raw served volume, capacity can expand beyond the system's ability to verify useful output.

The constructive lesson is not that verified-output billing is universally correct. DCRE-002 already showed that verification itself can be Goodharted. The point is that a price signal only governs the scarcity represented in that price.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_ENDOGENOUS_PROVIDER_INVESTMENT
```

No coefficient is an estimate of real provider margins, electricity prices, capital costs, demand, or data-center economics.

## Next physical falsifier

DCRE-014 should introduce a second physical resource. If electricity and water have different technology trade-offs, pricing one scarce resource may displace pressure into the other rather than improving total ecological viability.
