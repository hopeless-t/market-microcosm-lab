# DCRE-037 — Reserve providers are not independent reserve domains

## Trigger

DCRE-036 distinguishes nominal reserve capacity from expected usable reserve by adding reliability.

A further trap remains: two or three individually reliable providers can still share the same physical failure domain.

DCRE-037 does **not** build another correlation model. It reuses the already-qualified E022 `WitnessTopology` / domain-subset machinery and projects reserve modules onto that abstraction.

## Frozen reserve quorum

Three 10-unit reserve modules exist and at least two must remain available to preserve the 20-unit reserve target.

This maps to a synthetic 2-of-3 availability quorum.

### CONCENTRATED

```text
module domains = grid-x, grid-x, grid-y
quorum = 2 of 3
```

One `grid-x` outage removes two modules at once.

```text
minimum domains to break reserve availability = 1
```

At independent per-domain outage probability `.10`, E022 exact subset enumeration gives:

```text
availability-loss probability = .10
```

### INDEPENDENT

```text
module domains = grid-a, grid-b, grid-c
quorum = 2 of 3
```

One domain outage leaves two modules, so two independent domain outages are required.

```text
minimum domains to break reserve availability = 2
availability-loss probability at q=.10 = .028
```

## Result

```text
provider count
!= module count
!= independent reserve-domain count
```

Procurement quality cannot be inferred from the number of vendors alone. Reserve diversity matters only to the extent that the relevant physical dependencies are actually separated.

This is a direct physical-market projection of E022/E023 rather than a new reliability subsystem.

## Boundary

Domain labels and `.10` outage probability are synthetic. The experiment does not infer real grid, watershed, fuel, network, cloud-region, or vendor independence.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_RESERVE_FAILURE_DOMAIN_PROJECTION
```

## Next direction

The reserve chain has now covered quantity, private incentive, quality, and domain diversity. Do not extend it into auction/governance recursion yet.

The next foreground branch should return to **adaptive ecosystem recovery after shock**: how quickly providers, workload placement, and reserve rebuild toward a viable state, and when aggressive recovery creates a second rebound wave.
