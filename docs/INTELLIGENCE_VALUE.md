# Decision-Relevant Intelligence Value

## Status

Research note / candidate experiment design. This document adds no empirical claim and does not change the repository's synthetic-evidence boundary.

## Motivation

A recent counterintelligence case is useful as a structural reminder: individually small observations can become high-value once they reduce uncertainty about an entity, relationship, or future decision. The research lesson for this repository is not surveillance technique. It is the economic structure of **information value under imperfect observation**.

The central distinction is:

```text
information volume != information value
```

A large observation can be useless if it does not change a decision. A tiny observation can be valuable if it resolves a high-leverage uncertainty.

## Candidate value model

For an observation `o` acquired in state `x`, define:

```text
IG(o) = H(X | prior) - H(X | o)
```

where `IG` is information gain.

Information gain alone is insufficient. A candidate decision-relevant value is:

```text
V(o) = IG(o)
       * P(decision changes | o)
       * expected decision impact
       * timeliness
       * confidence
       + future option value
       - acquisition cost
       - verification cost
       - error / contamination risk
```

The multiplicative terms should not be treated as calibrated economics without an explicit experiment. They are a decomposition scaffold.

## Option value

Some observations are valuable even when they do not alter the current action because they can become decision-relevant after a future state transition.

```text
observe now
  -> retain qualified evidence
  -> future shock / state transition
  -> previously dormant observation becomes useful
```

This is naturally modeled as real-option-like value:

```text
V_total = V_current + E[V_future_option]
```

The model must include storage, staleness, provenance, and re-verification costs. Otherwise 'collect everything' wins artificially.

## Connection to the existing lab

The repository already separates world truth, operational truth, and certification truth. This note suggests an additional layer:

```text
World
  -> available observations
  -> candidate observation portfolio
  -> decision-relevance scorer
  -> bounded acquisition
  -> Governor-visible operational truth
  -> action
  -> outcome
  -> update observation policy
```

The Oracle remains isolated. The observation policy may only choose among data sources explicitly available to the operational world.

## Candidate E024 — Observation Portfolio Value

**Question:** Can the lab preserve the same promoted mechanism while evaluating materially fewer observations by selecting observations according to expected decision value?

### Baselines

1. exhaustive observation;
2. random bounded observation;
3. information-gain-only selection;
4. decision-relevant selection;
5. exact small-world oracle for comparison.

### Candidate score

```text
priority_i =
    expected_decision_change_i
    * expected_impact_i
    * confidence_i
    * freshness_i
    / max(acquisition_cost_i + verification_cost_i, epsilon)
```

### Acceptance targets

A candidate policy should not be promoted merely because it uses fewer queries.

It must preserve:

- the same final action as the exhaustive oracle on the exact small world;
- viability classification at the declared confidence threshold;
- replayability and provenance;
- fail-closed fallback when the observation model is out of distribution;
- a bounded false-negative rate for observations that would have changed the decision.

### Failure-biopsy questions

When selective observation disagrees with exhaustive observation, record:

- which omitted observation was decision-changing;
- whether the miss came from bad uncertainty estimation, low confidence calibration, stale provenance, or interaction effects;
- whether a pair of individually low-value observations had high joint value;
- whether option value was underestimated;
- whether the acquisition-cost model distorted the selector.

## Why this matters economically

The lab already studies scarce audit budgets. Observation itself is also a scarce budget.

The new object is therefore:

```text
scarce audit budget
+ scarce observation budget
+ imperfect knowledge
+ action-dependent value
```

This turns information acquisition into part of the market microcosm instead of assuming observation is free.

## Safety / scope boundary

This note is about abstract information economics, experimental design, and bounded observation inside synthetic or authorized systems.

It does **not** authorize covert monitoring, stalking, tracking private individuals, credential collection, evasion, or any other intrusive collection method. Public-source incidents may motivate abstractions; operational intelligence tradecraft is out of scope.

## Theory update candidate

A useful working principle is:

> **The best next observation is not the one with the most bits. It is the least-cost observation most likely to change a consequential decision without breaking the evidence boundary.**
