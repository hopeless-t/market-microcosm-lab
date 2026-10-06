# RPE-007 — Stale meaning, re-observation, and bounded replanning

## Question

RPE-006 assumes that once a meaning is selected for wake-up, executing the warm-up action restores a usable projection.

RPE-007 attacks that assumption:

> What if the meaning wakes successfully but is semantically stale?

The experiment separates three events that are easy to collapse incorrectly:

```text
wake succeeded
!=
freshness verified
!=
authority restored
```

## Initial plan

The original four-epoch plan assumes meaning A is fresh:

1. wake A;
2. mandatory verification;
3. fresh B;
4. fresh C.

At epoch 1, A wakes mechanically but the freshness check returns `STALE`.

The old projection immediately loses authority and recovering A now requires a separate re-observation action.

## Remaining actions

Epochs 2–4 have capacity one per epoch.

| Action | Window | Value | Mandatory |
| --- | --- | ---: | --- |
| mandatory verification | `[2,3)` | 0 | yes |
| re-observe stale A | `[2,4)` | 9 | no |
| fresh B | `[2,4)` | 7 | no |
| fresh C | `[2,5)` | 6 | no |

The mandatory verification is modeled as a hard invariant rather than a value-bearing job.

## Policies

### Static commitment

Continue the old plan and do not allocate capacity to re-observation.

- mandatory work survives;
- B and C survive;
- stale A contributes zero value;
- captured value = 13.

### Immediate re-observation greedy

Spend epoch 2 immediately on recovering A, then take B and C.

- captured value = 22;
- mandatory verification misses its deadline.

This policy is intentionally unsafe: a higher scalar value must not override a protected invariant.

### Exact safe replan

After staleness revokes the old projection, enumerate the remaining feasible action subsets while requiring the mandatory verification to remain scheduled.

The exact safe plan is:

```text
epoch 2  mandatory verification
epoch 3  re-observe A
epoch 4  fresh C
```

Captured value = 15.

It beats static commitment while remaining below the unsafe greedy's scalar value because it preserves the protected constraint.

## Theory update

The RPE chain now distinguishes:

```text
stored meaning
-> wake eligibility
-> wake execution
-> freshness validation
-> authority restoration
-> downstream use
```

A successful wake is only a transport/residency fact. It is not evidence that the retrieved semantic object is still valid for the current decision generation.

## Candidate rule

```text
WAKE_DOES_NOT_RESTORE_AUTHORITY
VALIDATE_FRESHNESS
REOBSERVE_IF_NEEDED
REPLAN_UNDER_MANDATORY_CONSTRAINTS
```

## Next falsifiers

RPE-008 should attack the binary `FRESH/STALE` model:

- partially stale meaning;
- multiple evidence ages inside one canonical object;
- re-observation can repair only some fields;
- uncertainty over which dependency changed;
- observation budget must be allocated to the most decision-relevant stale atoms.

That would connect Research Portfolio Ecology back to observation economics and finite semantic working sets.

## Claim ceiling

`EXACT_SMALL_SYNTHETIC_REOBSERVATION_WORLD_ONLY_NO_REAL_RESEARCH_FRESHNESS_POLICY_CLAIM`
