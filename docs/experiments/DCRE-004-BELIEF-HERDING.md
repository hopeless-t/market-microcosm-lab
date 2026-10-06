# DCRE-004 — Belief herding and duplicated exploration

## Why DCRE-003 is still single-agent

DCRE-003 found an exact exploration knee for one decision-maker. A market contains multiple actors, however, and individually reasonable exploration can become collectively wasteful when everyone shares the same ranking and independently probes the same opportunity.

DCRE-004 isolates that coordination failure.

## Frozen world

Four opportunities have synthetic priors and equal high-state value 10:

```text
A: p=0.80
B: p=0.70
C: p=0.60
D: p=0.55
```

Four probe tokens are available. Probes are assumed perfect and simultaneous. Repeated probes of the same opportunity add no new information.

That perfect-probe assumption is intentionally strong: it creates a clean lower bound on redundant information acquisition. Later work should add noisy evidence where repeated observation can be useful.

## Policies

### HERD

All actors independently choose the highest-ranked opportunity A.

```text
assignments = A,A,A,A
probe count = 4
unique opportunities = 1
duplicate probes = 3
expected discovery value = 0.8 * 10 = 8
expected value / probe = 2
```

### DIVERSIFIED

Coordinate the same four probes across distinct opportunities.

```text
assignments = A,B,C,D
probe count = 4
unique opportunities = 4
duplicate probes = 0
expected discovery value = (0.8+0.7+0.6+0.55)*10 = 26.5
expected value / probe = 6.625
```

### SHARED_OBSERVATION

Probe only A once and share the observation among actors.

```text
assignments = A
probe count = 1
expected discovery value = 8
expected value / probe = 8
```

Under the frozen perfect-observation contract, four simultaneous probes of A contain no more information than one shared probe of A.

## Market interpretation

The scarce resource is no longer only compute or verification. It is also **independent information acquisition**.

A market can fail even when every actor uses the same locally sensible policy:

```text
common belief ranking
 -> same target selected
 -> duplicated exploration
 -> low information diversity
 -> alternative opportunities remain unobserved
```

The coordination target is not forced diversity for its own sake. It is to avoid paying repeatedly for the same information when observations are shareable and failure domains are common.

## Important boundary

DCRE-004 does **not** prove that correlated exploration is generally bad.

Repeated probes can be valuable when:

- observations are noisy;
- actors have different sensors or failure domains;
- replication is required for trust;
- observations cannot be shared safely;
- strategic incentives make reports unreliable.

Those cases are deliberately absent here.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = PERFECT_PROBE_SYNTHETIC_COORDINATION_COUNTEREXAMPLE
```

The priors and values are synthetic. This is not an empirical estimate of AI research, data-center scheduling, or market R&D behavior.

## Next falsifier

DCRE-005 should add noisy probes and correlation structure. The question becomes how much replication is evidence and how much is waste. That directly connects this mainline market ecology back to the repository's existing witness-quorum and hidden-common-mode machinery without making RPE foreground again.
