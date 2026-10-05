# Workflow Ecology: Occupations as Executable Economic Programs — 2026-10-05

## Source spark

- https://note.com/shi3zblog/n/nf59b8740cd24
- Transferable idea: everyday work can be decomposed into operations, conditions, and repetition before being expressed as programming syntax.

## Microcosm hypothesis

An occupation can be modeled not only as a job title or labor quantity, but as a **workflow program embedded in an economic ecosystem**.

```text
Occupation
  = actors
  + state / artifacts
  + ordered operations
  + decision guards
  + loops / waits
  + failure / recovery
  + authority boundaries
  + evidence requirements
  + time / cost / error distributions
```

This creates a finer unit for studying automation than "AI replaces job X".

## Why this matters for market ecology

Technology rarely acts on an occupation as a single indivisible object. It changes individual workflow nodes.

Examples:

- removes a transcription step;
- reduces search cost;
- changes review frequency;
- adds verification work;
- shifts a decision from a person to a deterministic rule;
- creates a new coordination or compliance step;
- makes one actor able to process more cases;
- changes entry costs for new firms or workers.

Therefore the economic impact can be represented as a mutation of the workflow graph rather than an immediate deletion of an occupation.

## Candidate model

Let an occupation workflow be a graph `G=(V,E)` where each node has attributes:

```text
node {
  type
  actor_type
  service_time
  monetary_cost
  compute_cost
  error_probability
  retry_probability
  semantic_ambiguity
  authority_requirement
  evidence_requirement
  capacity_limit
}
```

A technology intervention transforms the graph:

```text
T(G) -> G'
```

Examples:

```text
manual_search
→ assisted_search
→ lower service_time, lower cost, maybe higher verification demand

manual_form_entry
→ deterministic extraction
→ node removed or compressed, review node retained

expert_decision
→ model proposal + human gate
→ decision cost shifts; new verification / escalation edges appear
```

The important output is not simply "task automated" but the resulting ecosystem state after costs, capacity, error, demand, and actor behavior adjust.

## From workflow mutation to ecology

A workflow change can propagate through the market model:

```text
workflow cost / throughput / quality change
        ↓
firm operating cost + capacity
        ↓
price / service quality / margin
        ↓
entry / exit / hiring / specialization
        ↓
user utility / demand
        ↓
ecosystem viability
```

This connects micro-level process changes to the lab's existing macro viability analysis.

## Automation is not one scalar

Candidate dimensions:

- `time_compression`
- `cost_compression`
- `error_change`
- `semantic_residual`
- `verification_overhead`
- `coordination_overhead`
- `capital_requirement`
- `skill_requirement`
- `throughput_multiplier`
- `new_failure_modes`

A technology can improve one dimension while worsening another.

## Recomposition of occupations

The model should allow jobs to change shape:

```text
G_old
  ├─ node A disappears
  ├─ node B becomes faster
  ├─ node C becomes an AI proposal
  ├─ new verification node D appears
  └─ actor allocation changes
        ↓
G_new
```

Possible ecological outcomes include:

- same occupation, higher throughput;
- fewer workers per unit of output but much larger demand;
- new specialist verification role;
- lower entry cost and more firms;
- concentration if capital / model access becomes dominant;
- lower prices and market expansion;
- partial task substitution without occupation extinction.

The simulation should discover which outcomes emerge under declared assumptions rather than presuppose a single employment story.

## Candidate synthetic experiment

Build a minimal closed service market with:

- consumers generating service demand;
- service firms composed of one workflow graph;
- worker capacity measured through workflow execution time;
- price and quality affecting demand;
- bounded entry / exit;
- one automation intervention that changes selected nodes.

Sweep interventions from narrow node compression to broad workflow restructuring and compare:

- employment / actor count;
- output volume;
- price;
- service quality;
- firm survival;
- worker income / specialization;
- consumer utility;
- ecosystem viability.

A useful control is a naive model that replaces labor with a single productivity multiplier. Compare whether the workflow model exposes failure modes or redistribution effects hidden by the scalar model.

## Relationship to Semantic Forge

Semantic Forge could supply a standardized workflow representation for occupations:

```text
industry-specific DSL
→ Canonical Workflow IR
→ market-microcosm cost / capacity projection
```

This would let the same semantic workflow support execution research and economic simulation without claiming that the economic projection captures every real institutional detail.

## Falsification / discipline

- Do not infer empirical employment effects from synthetic workflow experiments.
- Do not assume every workflow node is automatable.
- Keep semantic ambiguity, authority, verification, and error costs explicit.
- Stress demand elasticity, market expansion, capital concentration, and entry assumptions independently.
- Compare workflow-graph results against simpler productivity baselines.
- Preserve counterexamples where automation lowers task cost but worsens ecosystem viability.

## Core research question

Instead of asking only:

> "Will AI eliminate this occupation?"

ask:

> "Which workflow nodes change, what new nodes appear, how does the occupation recompose, and does the surrounding economic ecosystem remain viable after actors adapt?"

That is a natural Market Microcosm framing of occupation-as-DSL.
