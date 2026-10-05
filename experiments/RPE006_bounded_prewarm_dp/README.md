# RPE-006 — Bounded DP for finite prewarm scheduling

## Question

RPE-005 established exact small-world scheduling and showed that value-, density-, and arrival-greedy policies each have counterexamples.

RPE-006 asks the next machinery question:

> Can a bounded dynamic program reproduce the exact oracle while doing materially less search work on a deterministic portfolio suite?

## Generated suite

The protocol generates 32 deterministic portfolios from fixed seeds.

Each portfolio contains:

- 10 prewarm jobs;
- a six-epoch warm-up surface with capacity one per epoch;
- release times, deadlines, durations of one or two slots, and integer decision values.

The exhaustive reference checks all `2^10 = 1024` job subsets per portfolio and then verifies temporal feasibility.

The candidate scheduler uses memoization over:

```text
(job index, occupied-slot bitmask)
```

with a declared state-space ceiling of:

```text
(10 + 1) × 2^6 = 704 states
```

per portfolio.

## Promotion obligations

The bounded DP receives only candidate status if all of the following hold:

- exact total decision value matches the exhaustive oracle on 32/32 portfolios;
- the deterministic selected job set also matches on 32/32;
- aggregate counted search work falls by at least 60%;
- every individual portfolio reduces counted work by at least 50%;
- visited DP states remain inside the declared bounded state space.

## Synthetic result encoded by the fixture

Across the 32 generated portfolios:

- exhaustive subset work: **32,768 units**;
- bounded-DP visited states: **11,744 units**;
- aggregate reduction: **64.16015625%**;
- worst portfolio reduction: **51.5625%**;
- exact value match: **32/32**;
- exact selected-set match: **32/32**.

The work metric is deliberately narrow: exhaustive work counts candidate subsets while DP work counts memoized states. It does **not** claim wall-clock, token, API, or Human-attention savings.

## Candidate scheduler

```text
bounded-slot-mask-dp
```

This is still a small-horizon mechanism. Its state space grows exponentially with the number of time slots, so successful RPE-006 qualification must not be generalized into a claim of production scalability.

## Theory update

The RPE chain now has the following shape:

```text
RPE-001  do not suppress curiosity; gate materialization
RPE-002  canonicalization itself can destroy meaning
RPE-003  dormant meaning needs a wake path
RPE-004  wake signals need evidence/health guards
RPE-005  finite wake capacity makes local greedy policies unsafe
RPE-006  bounded exact-state machinery can recover the small-world optimum more cheaply
```

The optimizer still does not certify itself: exhaustive enumeration remains the oracle for these generated small worlds.

## Next falsifiers

RPE-007 should attack the time dimension rather than the solver:

- jobs can become semantically stale while waiting;
- a successfully scheduled wake can reveal that the stored meaning needs re-observation;
- re-observation consumes capacity and may invalidate the remaining schedule;
- rescheduling should preserve mandatory safety/verification jobs.

This would connect Research Portfolio Ecology to the durable-work / re-observation / recovery line already present elsewhere in the ecosystem.

## Claim ceiling

`DETERMINISTIC_GENERATED_SMALL_WORLDS_ONLY_NO_SCALABLE_PRODUCTION_SCHEDULER_CLAIM`
