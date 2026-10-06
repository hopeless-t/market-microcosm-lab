# DCRE-035 — Reserve procurement: system option value can disappear privately

## Trigger

DCRE-034 shows that reserve capacity can have positive system option value when shock probability and shortfall consequence exceed idle holding cost.

That result assumes the system can simply choose the reserve quantity.

DCRE-035 endogenizes a minimal provider incentive: reserve capacity earns no active-use revenue unless it receives an explicit capacity payment.

## Frozen providers

Two providers can each hold:

```text
reserve = 10
holding cost = .1 per unit
```

The DCRE-034 high-risk world remains:

```text
shock probability = .20
shock size = 20
shortfall penalty = 1 per unit
```

At system level, aggregate reserve 20 minimizes the frozen expected cost.

## NO_CAPACITY_PAYMENT

```text
payment = 0
private net/provider = 10 * (0 - .1) = -1
```

Neither provider enters reserve service.

```text
aggregate reserve = 0
system expected cost = 4
```

The socially valuable reserve disappears because the provider cannot capture the avoided-shortfall value.

## PRIVATE PAYMENT KNEE

A provider enters only with strictly positive private net:

```text
payment_per_unit > holding_cost_per_unit
```

so the frozen private knee is:

```text
payment = .1 / unit
```

At exactly `.10`, the model uses a strict entry rule and no provider enters.

At `.11`:

```text
P1 + P2 enter
aggregate reserve = 20
system expected cost = 2
total capacity payment = 2.2
```

## Result

```text
system option value
!= provider-capturable revenue
```

A competitive market can underprovide resilience even when reserve has positive modeled system value, because the benefit appears as avoided future loss rather than present active-use revenue.

The experiment does **not** promote a capacity market. It only constructs the incentive gap that any procurement mechanism would have to address.

## Boundary

Providers are identical, payment is certain, entry is binary, and capacity payments are treated as transfers rather than resource costs. There is no auction, market power, financing, strategic bidding, reserve failure, or regulatory model.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_RESERVE_PRIVATE_INCENTIVE_GAP
```

## Next falsifier

DCRE-036 should attack the capacity-payment fix. If payments are too generous or based only on nameplate reserve, they may procure idle overcapacity or attract low-reliability reserve. The next question is **procurement quality and over-reserve**, not whether payment can induce entry.
