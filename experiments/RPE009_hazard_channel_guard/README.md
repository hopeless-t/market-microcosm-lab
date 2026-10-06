# RPE-009 — Atom-level hazard-channel reliability adversary

## Question

RPE-008 used per-atom hazard signals to spend re-observation budget efficiently. RPE-009 attacks the signal layer itself:

> What if the atom-level staleness hazard channel produces false positives or false negatives?

The hidden fresh/stale state remains fixed from RPE-008. Four signal scenarios modify only what the operational selector can see.

## Scenarios

1. **healthy** — hazard signals match the stale atoms;
2. **false-positive-workflow** — a fresh workflow atom receives a false hazard and its noncritical signal group is explicitly degraded;
3. **false-negative-dependency** — a stale dependency atom loses its hazard while the critical governance signal group is degraded;
4. **combined** — both failures occur together.

## Policies

### Hazard only

Trust active atom hazards while always preserving the mandatory authority atom.

In the fixed fixture the restored stale decision value becomes:

```text
healthy                  29
false-positive-workflow  22
false-negative-dependency 20
combined                 19
```

A false positive can crowd real stale work out of the budget; a false negative can hide decision-relevant stale state.

### Health-guarded hazard

Separate the presence of a hazard from the health of the channel that produced it.

- if a **critical** group is degraded, fail closed to observing the group's atoms;
- if a **noncritical** group is degraded, suppress untrusted positive signals from that group rather than spending scarce budget on them;
- mandatory authority atoms remain mandatory regardless of hazard state.

In this deliberately constructed fixture, the guarded selector restores 29/30 stale decision-value units in all four scenarios and spends no budget on fresh atoms.

This does not establish a universal degraded-channel policy. The critical/noncritical distinction is declared fixture metadata.

## Theory update

The RPE observation path now mirrors the earlier certificate logic:

```text
hazard signal
!=
reliable hazard evidence

absence of hazard
!=
evidence of freshness
when the channel is degraded
```

A selector may rely on sparse observation only while the observation mechanism itself retains authority.

## Candidate rule

```text
ATOM_HAZARDS_REQUIRE_GROUP_HEALTH_GUARDS
CRITICAL_DEGRADATION_FAILS_CLOSED_TO_AUDIT
NONCRITICAL_DEGRADATION_SUPPRESSES_UNTRUSTED_SIGNALS
```

## Next falsifiers

RPE-010 should remove the assumption that atom groups fail independently:

- one hidden shared dependency can corrupt several hazard channels;
- apparently separate groups may share one upstream source;
- group-health labels themselves can be wrong;
- independent audit should target failure domains, not just atom counts.

This would close the loop back to E022/E023's failure-domain and hidden-common-mode results, now at the semantic-observation layer.

## Claim ceiling

`DETERMINISTIC_SYNTHETIC_HAZARD_CHANNEL_FIXTURE_ONLY_NO_REAL_STALENESS_SIGNAL_RELIABILITY_CLAIM`
