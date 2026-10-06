# DCRE-024 — Transfer frontier: network, encode compute, and semantic fidelity

## Trigger

DCRE-023 shows that a cheaper remote-transfer path can reopen a spatial placement that raw transfer makes infeasible.

That result treats `COMPACT_TRANSFER` as a free primitive.

DCRE-024 decomposes it into three resources:

```text
network traffic
local encode/transform compute
preserved semantic fidelity
```

The question is whether making the payload smaller simply moves scarcity into compute or semantic loss.

## Frozen remote workload

```text
remote tasks = 50
network ceiling = 20
encode-compute ceiling = 20
preserved-semantic floor = 45 task-equivalents
```

## Modes

### RAW

```text
network/task = .50
encode compute/task = 0
fidelity = 1.00

network = 25  -> fails
compute = 0   -> passes
semantic = 50 -> passes
```

### COMPACT_BALANCED

```text
network/task = .30
encode compute/task = .20
fidelity = .95

network = 15
compute = 10
semantic = 47.5
```

All three frozen constraints pass.

### OVERCOMPRESSED

```text
network/task = .15
encode compute/task = .40
fidelity = .80

network = 7.5
compute = 20
semantic = 40 -> fails semantic floor
```

Maximum byte reduction destroys too much modeled meaning.

### HEAVY_LOSSLESS

```text
network/task = .25
encode compute/task = .50
fidelity = 1.00

network = 12.5
compute = 25 -> fails compute ceiling
semantic = 50
```

Preserving all modeled semantics can also be too expensive locally.

## Result

Only `COMPACT_BALANCED` is jointly viable among the four frozen modes.

```text
minimum transfer
!= minimum compute
!= maximum fidelity
!= viable projection
```

The useful object is a constrained transfer frontier, not a scalar compression ratio.

This gives a physical-market interpretation to minimum-sufficient projections: a representation can change the feasible region only when network savings are not bought with excessive local compute or decision-relevant semantic loss.

## Boundary

All values and the linear fidelity model are synthetic. `semantic_fidelity` is not a measured quality score and must not be projected as one.

The experiment also does not identify an encoding scheme. RAW/COMPACT/OVERCOMPRESSED/HEAVY are abstract mechanisms.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_TRANSFER_RESOURCE_FRONTIER
```

## Next falsifier

DCRE-025 should add reuse. A compact representation can have an up-front preparation cost that is irrational for one transfer but becomes attractive when reused across many requests. The next question is the reuse-count knee where canonical/cached preparation amortizes its fixed cost.
