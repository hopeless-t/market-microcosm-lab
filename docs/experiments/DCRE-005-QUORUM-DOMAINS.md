# DCRE-005 — Witness count vs independent evidence domains

## Trigger

DCRE-004 shows that common beliefs can duplicate exploration. A natural response is replication: probe the same question multiple times before acting.

Replication only adds evidence when the probes fail independently enough.

DCRE-005 deliberately reuses the repository's existing `WitnessTopology` abstraction from E022 instead of introducing a new failure-domain type. The experiment is therefore a projection of an already-qualified mechanism into the exploration market.

## Frozen evidence model

Three nominal witnesses each have domain accuracy 0.8. Witnesses in the same failure domain share the same correctness state; different domains are independent in this small world. Majority vote requires two of three nominal votes.

### Three witnesses, one domain

```text
witness_domains = a,a,a
nominal witnesses = 3
independent domains = 1
majority accuracy = 0.800
```

Three copies of the same failure mode do not improve the evidence.

### Three witnesses, three domains

```text
witness_domains = a,b,c
nominal witnesses = 3
independent domains = 3
majority accuracy = 3*(0.8^2*0.2) + 0.8^3
                  = 0.896
```

### Correlated pair plus one independent witness

```text
witness_domains = a,a,b
independent domains = 2
majority accuracy = 0.800
```

Because the correlated pair already controls the majority, the third witness cannot repair the common-mode error in this exact voting rule.

## Market interpretation

A market that pays per witness can purchase nominal redundancy without purchasing independent evidence.

```text
witness count
!= independent failure domains
!= effective evidence strength
```

This matters for exploration markets because repeated model calls, agents, evaluators, sensors, or organizations can look plural while sharing training lineage, source data, infrastructure, incentives, or upstream observation channels.

The policy implication is deliberately narrow: do not price evidence by count alone. Preserve provenance and failure-domain identity so replication can be valued according to explicit, falsifiable independence assumptions.

## Relationship to E021–E023

DCRE-005 does not replace the existing witness-quorum work. It reuses the same topology semantics for a different economic question:

```text
E021–E023: can authority/evidence survive compromised or correlated witnesses?
DCRE-005: when does spending scarce exploration budget on another witness buy independent information?
```

This is a mainline semantic transfer, not a new governance layer.

## Boundary

The 0.8 accuracy and domain structure are synthetic. Real independence is rarely known exactly. Unknown correlation must remain unknown rather than being silently assigned independence.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = EXACT_SYNTHETIC_FAILURE_DOMAIN_QUORUM_COUNTEREXAMPLE
```

## Next falsifier

DCRE-006 should make domain identity uncertain. If independence itself must be inferred, the market must decide whether to buy another witness, buy a new failure domain, or spend resources learning the correlation structure.
