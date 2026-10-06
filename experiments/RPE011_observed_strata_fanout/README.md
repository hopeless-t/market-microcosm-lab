# RPE-011 — Observed Strata cross-repository fan-out replay

## Why this experiment exists

RPE-001 began from a synthetic claim: one source event can become many physical repository materializations.

RPE-011 stops extending the synthetic ladder and asks whether a comparable fan-out pattern is visible in the actual hopeless-t GitHub history.

## Retrieval

A GitHub commit search for the term `Strata` under `hopeless-t` exposed a dense event cluster on 2026-10-05 JST.

The experiment snapshots the matching commits from:

```text
2026-10-05T23:10:37+09:00
through
2026-10-05T23:16:57+09:00
```

Every retained row includes repository, commit SHA, commit message, and timestamp so the observation remains replayable even if later Strata commits are added.

## Observed result

Inside the 380-second window:

- **24 commits** explicitly reference `Strata`;
- those commits occur in **24 distinct repositories**;
- the maximum inter-commit gap is **40 seconds**;
- mean inter-commit gap is about **16.52 seconds**;
- the observed density is about **3.79 commits per window minute**.

The repositories span runtime, governance, semantic IR, resource labs, recovery, product, evidence, control systems, portfolio allocation, and indexing surfaces.

This is direct evidence that a compact cross-repository source-referencing fan-out event occurred.

## What is not observed

Commit metadata does **not** reveal:

- which of the 24 projections changed a later decision;
- which projections were required immediately rather than merely potentially useful;
- the Human review cost of each commit;
- context/API/token cost;
- whether a canonical intake would have produced the same semantic content;
- whether delaying any particular projection would have caused harm.

Therefore RPE-011 deliberately leaves these fields as `UNKNOWN` / `None`:

```text
decision_relevant_projection_count
counterfactual_materialization_savings
```

The retrospective on-demand envelope is only:

```text
minimum projections if no downstream need were established: 0
maximum projections if every observed projection were required: 24
```

Anything narrower would require additional evidence.

## Theory update

RPE-001's fan-out phenomenon is no longer only a synthetic possibility.

What remains unproven is the economically important part: **how much of the observed fan-out was useful work versus option-preserving duplication?**

That distinction now becomes the next empirical target.

## Candidate next experiment

RPE-012 should search for downstream use evidence for this same 24-repository cluster.

Possible evidence classes:

- later commits that modify or depend on the Strata-derived artifact;
- tests or workflows that execute the imported mechanism;
- PRs/issues that cite the projection in a later decision;
- later supersession/reversion indicating that the projection became stale or unused;
- repository-local documents marking the projection as hypothesis-only versus adopted behavior.

Only after such evidence exists should the lab estimate a retrospective materialization-savings range.

## Claim ceiling

`OBSERVED_GITHUB_COMMIT_METADATA_CLUSTER_ONLY_NO_CAUSAL_OR_COUNTERFACTUAL_SAVINGS_CLAIM`
