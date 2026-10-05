# Data-center resource ecology — 2026-10-05

## Why this belongs in Market Microcosm Lab

Efficiency can reduce the resource cost of one AI task while increasing the total number of AI tasks. Therefore the ecological object is not "energy per inference" alone but the closed loop among efficiency, price, demand, capacity, resource draw, and useful output.

This is a Jevons/rebound problem in the same sense that cheaper production can expand total consumption.

Primary context:

- IEA, *Energy and AI*: https://www.iea.org/reports/energy-and-ai
- Google Data Centers efficiency: https://datacenters.google/intl/en/efficiency/
- Nebraska data-center reporting: https://dwee.nebraska.gov/data-center-task-force

## Core ecological loop

```text
compute efficiency improves
  -> cost per task falls
  -> AI demand expands
  -> capacity expands
  -> total electricity/water demand may rise
  -> infrastructure/environmental pressure rises
  -> pricing/regulation/supply responses change
  -> demand and investment adapt again
```

The lab should therefore distinguish:

```text
unit efficiency
!=
total resource consumption
!=
verified social/economic utility
```

## Candidate state variables

A synthetic world can add:

```text
AIResourceState {
  useful_task_demand
  speculative_task_demand
  cost_per_verified_task
  compute_capacity
  utilization
  energy_per_task
  total_energy
  water_intensity
  total_water
  network_bytes
  resident_memory_capacity
  verified_semantic_output
  resource_price
  capacity_investment
}
```

The first experiments can keep `water_intensity` synthetic rather than pretending to reproduce a real facility.

## Actors

Candidate actor classes:

- users buying AI-mediated services;
- platforms scheduling work;
- AI workers/models with different cost/quality profiles;
- infrastructure providers;
- electricity/water suppliers represented as bounded resource pools;
- regulators/community constraints represented as external viability limits.

No actor receives hidden Oracle truth merely because the simulator knows it.

## Candidate experiment E024 — Efficiency rebound

### Question

When per-task resource cost falls, under what elasticity and capacity-expansion conditions does total resource use fall, stay flat, or increase?

### Arms

```text
A  no efficiency improvement
B  efficiency improvement only
C  efficiency + fixed total resource budget
D  efficiency + verified-work budget
E  efficiency + dynamic resource price/backpressure
F  efficiency + cheap-first model escalation + resource budget
```

### Important distinction

A fixed resource cap can preserve electricity/water bounds while still allocating the budget badly. A verified-work budget instead asks whether resource spend buys independently checked semantic progress rather than retries, duplicate context processing, speculative generation, or unnecessary large-model escalation.

## Candidate demand model

Let unit resource cost be `c`, demand be `D(c)`, and unit efficiency improvement be `e` where lower `e` means fewer resources per task.

```text
total_resource = e * D(c(e))
```

Efficiency reduces `e`, but if induced demand grows faster than the efficiency gain, total resource consumption increases.

The lab should sweep demand elasticity rather than assume a single rebound response.

## Candidate viability constraints

A resource-aware viability kernel could require simultaneously:

- essential user utility above floor;
- platform/provider solvency above floor;
- verified useful output above floor;
- total electricity draw below declared ceiling;
- water draw below declared ceiling;
- queue/tail-latency below service ceiling;
- no persistent starvation of low-cost/low-priority actors;
- evidence/certification budget remains available.

This lets the lab ask whether an apparently efficient policy merely transfers collapse from finance to infrastructure or from infrastructure to service quality.

## Failure biopsies to retain

- **rebound overshoot** — per-task cost falls but total resource use rises;
- **capacity race** — providers reinvest efficiency gains into more capacity until the old resource ceiling is reached again;
- **verification starvation** — cheap generation scales faster than exact verification;
- **frontier-model saturation** — routing sends too much work to expensive models despite cheap alternatives;
- **resource-price exclusion** — dynamic pricing preserves resource ceilings by pricing essential low-budget users out;
- **water displacement** — an energy-efficient configuration shifts burden toward water-intensive cooling assumptions.

## Cross-project bridge

`next-generation-github` can expose a canonical resource envelope per semantic operation. `finite-ram-lab` can measure working-set/residency mechanisms. Market Microcosm Lab can then study the macro/ecological consequence:

```text
micro efficiency evidence
  -> system cost curve
  -> actor adaptation
  -> rebound / substitution
  -> long-run viability
```

The cross-project north star is not maximum AI throughput.

> **Find governance and allocation rules under which verified useful computation can grow without resource demand escaping the ecosystem's viability region.**

## Boundary

This note proposes a synthetic research program. It is not an empirical estimate of Google, Nebraska, global data-center demand, or real policy effects. Real electricity and water coefficients must remain external evidence with provenance and uncertainty.
