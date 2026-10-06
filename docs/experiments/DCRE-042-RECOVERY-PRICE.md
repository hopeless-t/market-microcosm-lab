# DCRE-042 — Uniform emergency recovery price can jump from underbuild to overbuild

## Trigger

DCRE-038–041 decompose recovery speed, backlog release, value decay, and finite recovery throughput.

The next foreground question returns to provider investment: how should a damaged market induce rebuilding?

A natural intervention is an emergency payment per restored capacity unit.

DCRE-042 attacks the assumption that one uniform recovery price is enough when multiple providers independently observe the same system capacity gap.

## Frozen market

```text
shocked capacity = 60
target capacity  = 100
shared perceived gap = 40
```

Two identical providers each have:

```text
max build = 40
recovery cost = 1 / unit
```

Each provider independently rebuilds its full perceived gap when payment exceeds recovery cost.

## LOW PAYMENT

```text
payment = .9 < cost1
```

Both providers decline:

```text
builds = 0 + 0
final capacity = 60
shortfall = 40
```

## HIGH PAYMENT

```text
payment = 1.1 > cost1
```

Both providers independently see the same 40-unit gap and each builds 40:

```text
builds = 40 + 40
final capacity = 140
overshoot = 40
```

The price fixes the private incentive gap but duplicates the system need.

## COORDINATED GAP ACCOUNTING

As a counterfactual benchmark, split the one physical gap once:

```text
P1 build20
P2 build20
final capacity100
shortfall0
overbuild0
```

This is not a promoted allocation rule. It only proves that the overshoot comes from duplicated gap accounting rather than unavoidable construction indivisibility.

## Result

```text
recovery price signal
!= shared recovery quantity accounting
```

In the frozen binary response world, there is no uniform price in the tested low/high regimes that produces the desired aggregate 40-unit rebuild: below cost nobody enters; above cost both actors independently rebuild the same gap.

The mechanism is the recovery analogue of DCRE-017 investment herding and DCRE-029 synchronized load shifting.

## Boundary

Provider response is discontinuous and deterministic, both providers have identical costs, and there is no bidding, construction lag, partial investment, strategic anticipation, financing, or real recovery market.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_EMERGENCY_RECOVERY_PRICE_COORDINATION_FAILURE
```

## Next falsifier

DCRE-043 should add heterogeneous provider recovery costs. Heterogeneity may soften the binary jump and create an interior aggregate response, but it can also concentrate rebuilding in the cheapest provider and recreate the provider-concentration / failure-domain problem seen earlier.
