# E022 — Failure-domain diversity under correlated witness compromise

E021 proves that 3-of-5 witness quorums have useful intersection geometry when witnesses are independent identities.

E022 asks whether those five identities are actually independent enough to deserve that interpretation.

## Topologies

Three five-witness / 3-of-5 topologies are compared:

- **concentrated 3-1-1** — three witnesses share one failure domain;
- **balanced 2-2-1** — two pairs share domains;
- **independent 1-1-1-1-1** — every witness has its own failure domain.

A domain compromise or outage affects every witness inside that domain together.

## Exact subset enumeration

For each topology, E022 enumerates every subset of failure domains.

The model derives:

- minimum compromised domains needed to forge a quorum;
- minimum failed domains needed to lose availability;
- exact forge probability for a homogeneous independent domain-event probability;
- exact availability-loss probability under the same topology.

## 10% domain-event comparison

With an illustrative 10% independent event probability per domain:

- concentrated 3-1-1 → forge probability **10.0%**;
- balanced 2-2-1 → **2.8%**;
- independent 1-1-1-1-1 → **0.856%**.

The independent topology reduces modeled forge probability by **91.44%** relative to the concentrated topology.

## Effective compromise boundary

The nominal quorum is 3-of-5 in all cases, but the domain-level compromise boundary differs:

- concentrated → **1 domain** can forge;
- balanced → **2 domains**;
- independent → **3 domains**.

This is why witness count alone is insufficient.

## Promotion

The experiment promotes a rule only if exact enumeration confirms:

1. concentrated 3-1-1 collapses to a one-domain forge;
2. balanced 2-2-1 needs two domains;
3. full independence needs three domains;
4. the independent model stays below 1% forge probability at a 10% domain-event rate;
5. it reduces forge probability by more than 90% versus concentrated;
6. availability loss obeys the same quorum geometry;
7. every domain subset was enumerated.

## Limitation

The domain model assumes domains fail independently and uses homogeneous synthetic event probabilities.

Real cloud providers, regions, operators, key stores, networks, and legal jurisdictions can share hidden dependencies. A label such as different region or different vendor is not evidence of true independence.
