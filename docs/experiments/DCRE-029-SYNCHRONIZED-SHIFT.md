# DCRE-029 — Synchronized load shifting recreates the peak

## Trigger

DCRE-028 finds a jointly viable temporal split for one aggregate flexible workload.

That result assumes one allocator owns the whole flexible budget.

DCRE-029 splits the same 40 flexible tasks across two independent actors. Each actor observes the same offpeak slack and decides locally.

## Frozen actors

```text
Actor A flexible tasks = 20
Actor B flexible tasks = 20
```

Each actor evaluates OFFPEAK against the baseline before the other actor moves:

```text
baseline OFFPEAK tasks = 20
one actor shifts 20
assumed OFFPEAK tasks = 40
assumed water = 40 * .4 = 16 <= ceiling 20
```

So moving all 20 tasks looks locally safe to both actors.

## Independent response

Both actors make the same individually safe move:

```text
A shifts 20
B shifts 20
aggregate shift = 40
```

Actual destination load becomes:

```text
OFFPEAK tasks = 60
energy = 48
water = 24 > ceiling 20
```

The destination period becomes the new resource peak.

## Coordinated headroom use

If the shared offpeak headroom is allocated once rather than independently consumed twice:

```text
A shifts 15
B shifts 15
aggregate shift = 30

PEAK flexible remainder = 10
OFFPEAK tasks = 50
OFFPEAK water = 20
PEAK energy = 64
```

The same frozen multi-resource constraints pass.

## Result

```text
correct local observation
+ identical rational response
!= jointly viable response
```

Temporal demand response has the same ecological failure mode as DCRE-004 belief herding and DCRE-017 shared-forecast investment herding: a shared signal can synchronize individually sensible actions and cause the apparent slack to be consumed multiple times.

The control target is therefore not merely a better price or forecast. It is **shared headroom accounting under concurrent response**.

## Boundary

There are only two actors, one destination period, deterministic response, and no bidding, fairness, strategic withholding, or rebound demand. The symmetric 15/15 split is an existence proof, not a promoted allocation rule.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_SYNCHRONIZED_LOAD_SHIFT_COUNTEREXAMPLE
```

## Next falsifier

DCRE-030 should test whether a temporal scarcity price fixes synchronization or simply creates another distribution problem: actors with higher willingness-to-pay may consume the scarce offpeak headroom while flexible but essential low-budget work remains in the constrained period.
