# RPE-008 — Partial staleness and observation-budget allocation

## Question

RPE-007 treated a canonical meaning as one binary `FRESH/STALE` object. RPE-008 breaks that simplification:

> If only some semantic atoms are stale, which atoms deserve scarce re-observation budget?

## Canonical object

The synthetic object contains seven atoms with different observation costs, decision values, evidence ages, hidden freshness states, and hazard signals.

One atom — `authority-contract` — is mandatory for promotion. A policy that ignores it is invalid regardless of scalar restoration value.

Total full-object refresh cost is **13**, while the available observation budget is **7**.

The hidden stale decision value is **30**.

## Policies

### Observe whole object

Re-observe every atom.

This would restore all stale value, but costs 13 and therefore violates the declared budget. Whole-object refresh is not an admissible default in this world.

### Oldest first

Spend budget on the oldest evidence first.

It chooses archive/display/source/cost atoms, spends 6, restores only 8 stale decision-value units, and misses the mandatory authority atom.

Age is therefore not equivalent to decision relevance.

### Mandatory + value-density greedy

First include the mandatory authority atom, then choose by declared decision value per observation cost.

It spends the full budget of 7 and restores 22 units, but wastes two cost units re-observing a fresh high-value workflow atom.

Decision value alone is not equivalent to expected restoration value when freshness is uncertain.

### Hazard-aware exact budget

Enumerate atom subsets under the budget while requiring the mandatory authority atom and scoring only atoms carrying the declared hazard signal.

In this deliberately constructed fixture it selects:

```text
authority-contract
cost-model
dependency-map
```

Cost = 7, restored stale decision value = **29/30**.

### Hidden-staleness oracle

An oracle that can see the hidden fresh/stale state chooses the same three atoms in this fixture. This is a qualification comparator, not operationally available truth.

## Theory update

The useful unit of re-observation may be smaller than the canonical object:

```text
canonical meaning
  -> semantic atoms
  -> per-atom evidence age / dependency / hazard
  -> bounded observation portfolio
  -> reconstructed current projection
```

This keeps RPE from replacing one form of over-materialization with another: preserving one canonical object does not imply refreshing the entire object whenever any field becomes suspect.

## Candidate rule

```text
REOBSERVE_DECISION_RELEVANT_STALE_ATOMS
NOT_WHOLE_OBJECTS
PRESERVE_MANDATORY_AUTHORITY_ATOMS
```

## Next falsifiers

RPE-009 should attack the hazard signal itself at atom granularity:

- false-positive hazard atoms waste observation budget;
- false-negative hazards hide stale mandatory atoms;
- shared dependency changes make hazard errors correlated;
- one observation may update several dependent atoms;
- the observation portfolio may need a fail-closed audit path rather than trusting the hazard selector indefinitely.

## Claim ceiling

`EXACT_SMALL_SYNTHETIC_ATOM_PORTFOLIO_ONLY_NO_REAL_STALENESS_DETECTOR_CLAIM`
