# RPE-014 — Projection maturity with provenance

## Goal

Close the Research Portfolio Ecology bootstrap by replacing the binary question "did the projection survive?" with a provenance-aware maturity ladder.

A file remaining on `main` is evidence of persistence, not evidence of downstream operational value.

## Maturity states

```text
OPERATIONAL_TRANSFER
  downstream code/test/runtime artifact exists and provenance matches this projection

REINFORCEMENT
  the target already had an operationally similar mechanism before this projection

CONVERGENT_OTHER_SOURCE
  a later similar mechanism is explicitly attributed to a different source

PERSISTENT_DOC_ONLY_UNKNOWN
  the projection remains addressable, but downstream operational adoption is not established

DORMANT_OR_LOST_UNKNOWN
  persistence is not established and operational value remains unknown
```

## Representative Strata v0.1.39 sample

Five repo-specific projections were inspected at commit and current-main level.

| repository | observed projection | current classification |
| --- | --- | --- |
| `catfood-semantic-forge` | one docs/research note; unique `ResourceNode` marker found only in that note | `PERSISTENT_DOC_ONLY_UNKNOWN` |
| `market-microcosm-lab` | one docs/research note; unique `shadow_price` marker found only in that note | `PERSISTENT_DOC_ONLY_UNKNOWN` |
| `field-report-app` | one docs/research note; distinctive lower-resolution/deferred-export wording found only in that note | `PERSISTENT_DOC_ONLY_UNKNOWN` |
| `recursive-flourishing-lab` | Strata note persists, while executable semantic-working-set code/tests already exist in the observed repository snapshot and are tied to a finite-RAM transfer lineage | `REINFORCEMENT` |
| `next-generation-github` | Strata note persists; later HOT/WARM/COLD/OFF capability work explicitly names DeepSeek Harness as its trigger | `CONVERGENT_OTHER_SOURCE` |

Snapshot summary:

```text
PERSISTENT_DOC_ONLY_UNKNOWN  3
REINFORCEMENT                1
CONVERGENT_OTHER_SOURCE      1
OPERATIONAL_TRANSFER         0
```

`OPERATIONAL_TRANSFER = 0` in this five-item sample is **not** evidence that no Strata projection was useful. It means the inspected evidence did not establish a provenance-matched downstream operational transfer.

## Consequence

Repository fan-out count is not a value metric.

```text
projection count != adoption count
persistence       != causal contribution
similarity        != provenance
```

This prevents two symmetric errors:

1. declaring all cross-repo projection waste because no immediate code change followed;
2. claiming later similar work as proof that the earlier projection caused it.

## Bootstrap exit criterion

RPE bootstrap is now sufficient to support the main Market Microcosm programme when all of the following hold:

- curiosity admission and downstream materialization are separated;
- canonicalization errors have explicit adversaries;
- residency/wake/re-observation have bounded-resource models;
- scheduler candidates remain checked against exact small-world oracles;
- real fan-out has at least one observed corpus bridge;
- projection maturity preserves provenance and `UNKNOWN` states;
- RPE's own authoring path batches coherent changes before triggering the full verifier.

After this point, new RPE work should be **demand-paged by failures observed in mainline Market Microcosm research**, rather than expanded as a permanent foreground programme.

## Authority and claim boundary

```text
authority_effect = NONE
claim_ceiling = SNAPSHOT_SPECIFIC_REPOSITORY_EVIDENCE
```

The five-repository sample is deliberately not generalized to the whole portfolio. The classification can change when stronger provenance, downstream experiments, or contradictory evidence appear.
