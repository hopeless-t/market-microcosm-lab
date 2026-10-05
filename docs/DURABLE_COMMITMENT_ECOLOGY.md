# Durable Commitment ecology

Status: synthetic research candidate

Source intake: https://note.com/npaka/n/n341b20a052c6

## Why this belongs in the microcosm

Persistent AI work creates an economy of scarce resources: observation budget, planner compute, tool calls, verification, Human attention, deadlines, and unresolved obligations.

A durable Commitment is therefore not only a software object. A population of Commitments forms a small resource-allocation ecology.

## Candidate world

Each Commitment has:

```text
value_if_completed
observation_cost
wake_cost
execution_cost
verification_cost
human_attention_cost
expiry / deadline
risk
state
```

The platform/governor has bounded budgets per epoch.

Policies allocate budget among:

- sleeping commitments;
- newly triggered commitments;
- verification of claimed completion;
- audit of old/stale commitments;
- Human escalation.

## Research questions

1. Does naive "wake everything frequently" collapse under load before event-driven allocation?
2. When does aggressive sleeping increase missed-deadline or stale-state loss?
3. What is the viability frontier between responsiveness and observation/compute cost?
4. How should scarce independent verification budget be allocated across long-lived commitments?
5. Can a backlog create positive feedback where delayed observation causes more expensive recovery later?

## Connection to existing work

This can reuse the lab's existing themes:

```text
certificate lifecycle
+ audit portfolio
+ provenance ledger
+ failure-domain analysis
```

A Commitment's current state may be cheap to retain, while re-certifying that state has a lifecycle and cost.

## Important boundary

The model must not assume that more automation or more completed tasks is always better. The North Star remains ecosystem viability under bounded resources and uncertainty.

Candidate slogan:

> **Unfinished work is an ecology: persistence has value, but attention is scarce.**