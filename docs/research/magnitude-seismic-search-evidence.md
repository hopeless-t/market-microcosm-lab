# Magnitude / Seismic lessons for market-microcosm-lab

## Why it maps

Magnitude's solver and compiler make a sharp distinction between a legal candidate, a proved optimum, an incomplete search, and an infeasible model. That distinction is directly useful for closed-economy and allocation experiments, where a locally attractive allocation is often mistaken for a globally justified one.

## 1. Separate candidate quality from proof status

Use explicit result classes:

```text
Feasible      complete legal allocation
Optimal       globally proved best allocation under the model
Incomplete    legal candidates exist, but proof/coverage is unfinished
Infeasible    no legal allocation exists under the declared constraints
Error         the model, arithmetic, or invariant handling failed
```

A simulation timing out is not evidence that the economy has no solution. A high-scoring allocation is not an optimum merely because no better one was sampled.

## 2. Keep local evidence local

Neighborhood search, Monte Carlo exploration, and heuristic repairs can generate valuable candidates, but their evidence must remain scoped.

```text
local improvement != global proof
sampled stability != universal stability
good incumbent != optimal allocation
```

Every candidate promoted into the main comparison should be rechecked against the original model and all active constraints.

## 3. Model resources and side effects explicitly

A market microcosm should make shared constraints first-class:

- finite capital
- inventory
- attention
- labor/time
- compute/API budget
- liquidity
- platform capacity
- dependency bottlenecks
- shared infrastructure

If a resource relation crosses two submarkets, those submarkets cannot be treated as independently optimizable merely because their internal state is disjoint.

## 4. Preserve occurrence identity

Repeated agents, transactions, jobs, or products should not be merged simply because they share a template.

A compact repeated representation is valid only when the recurrence/reset semantics and independence conditions are proved. Otherwise repeated occurrences need distinct identity because shared resources, state, timing, or path dependence may couple them.

This gives a useful rule for GamePass/Netflix/STRATS-style closed ecosystem modeling: identical participant classes do not imply independent economic occurrences.

## 5. Search as an incremental durable process

Treat optimization as resumable:

```text
Model
  -> search state
  -> incumbent
  -> lower/upper evidence
  -> budget stop
  -> resume
```

Preserve:

- best known feasible allocation;
- unresolved regions;
- proof bounds;
- restart history;
- failure reasons;
- resource usage.

This is a better substrate for the lab's meta/self-improvement loops than starting every experiment from zero.

## 6. Distinguish policy from mechanism

The economic policy being tested should remain stable while implementation mechanics vary.

Examples of mechanisms:

- exact solver
- Monte Carlo
- local search
- pseudo-Council proposals
- heuristic repair
- replay from historical traces

They are search backends, not alternate definitions of the market.

## 7. Proposed experiment

Take one existing closed-ecosystem distribution model and run four search modes over the same canonical constraints:

1. greedy;
2. Monte Carlo;
3. neighborhood repair;
4. exact search on a reduced instance.

Record separately:

```text
best feasible score
proof status
search coverage
resource usage
constraint violations rejected
sensitivity to seed
```

Then compare how often a heuristic winner is later displaced or invalidated.

## Working hypothesis

The strongest transferable idea is:

> Economic simulation should carry both a candidate outcome and an epistemic status describing what has actually been established about that outcome.

That makes the lab safer against over-reading simulations and gives the meta-improvement loop a concrete signal for where more search or model refinement is needed.
