# Strata v0.1.39 as a resource-allocation microcosm — 2026-10-05

## Microcosm interpretation

Strata can be modeled as a tiny market in which scarce fast memory, compute and transfer bandwidth are allocated among competing objects and requests.

## Agents / goods

- goods: VRAM bytes, RAM bytes, SSD bandwidth, PCIe bandwidth, compute slots, queue time;
- consumers: experts, prompt chunks, sessions, verification windows;
- utility: tokens/s, latency reduction, cache-hit probability, verified work completed;
- externalities: one session can evict hot state needed by another; one placement can consume bandwidth needed elsewhere.

## Candidate price signal

```text
shadow_price(resource) ~= marginal verified utility lost when one unit is removed
```

This suggests experiments around dynamic shadow prices rather than fixed tier rankings.

## Research hooks

1. Compare static priority allocation with pressure-sensitive pricing.
2. Measure congestion externalities from concurrency.
3. Model hot-set promotion as investment under uncertain future demand.
4. Model fallback hardware as lower-quality but still productive supply rather than zero supply.
5. Study whether local greedy placement converges toward globally efficient throughput or creates thrashing.

## Cross-project bridge

Results could inform `finite-ram-lab` placement heuristics, `mvca-runtime` worker admission, and `next-generation-github` context budgeting.

## Boundary

This is an analytical projection of Strata's mechanisms, not a claim that its implementation intentionally uses market economics.
