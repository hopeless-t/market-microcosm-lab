# E021 — Multi-witness checkpoint quorum

E020 preserves continuity to older checkpoints, but it still assumes one external anchor authority is trustworthy. E021 distributes that trust across five synthetic witnesses.

## Contract

The candidate contract is:

three-of-five-witness-quorum-with-equivocation-detection-v1

A checkpoint is accepted only when at least three distinct registered witnesses provide valid attestations over the same checkpoint sequence and checkpoint hash.

The experiment uses deterministic HMAC-SHA256 attestations as a small-world signature analogue.

## Compromise boundary

For a forged checkpoint:

- 1 compromised witness → no quorum;
- 2 compromised witnesses → no quorum;
- 3 compromised witnesses → forged quorum succeeds.

The third case is not a success condition to hide. It is the explicit compromise threshold.

## Quorum intersection

E021 exhaustively enumerates all exact-size witness quorums.

For 3-of-5:

- there are 10 quorum sets;
- every pair of quorums intersects;
- minimum intersection is at least one witness;
- no disjoint quorum pair exists.

For 2-of-5:

- disjoint quorum pairs exist.

This demonstrates why strict-majority quorum geometry matters for split-view evidence.

## Split view

Two conflicting checkpoints at the same sequence are given valid 3-of-5 quorums:

- honest view: witnesses 0, 1, 2;
- conflicting view: witnesses 2, 3, 4.

Both views individually verify.

Because 3-of-5 quorums must intersect, witness 2 signed both conflicting checkpoint hashes. The retained attestations therefore contain explicit equivocation evidence.

## Promotion

The contract is promoted only if:

1. honest 3-of-5 verification passes;
2. 1–2 compromised witnesses cannot forge;
3. 3 compromised witnesses demonstrate the exact forge boundary;
4. all 3-of-5 quorums intersect;
5. 2-of-5 has a disjoint-quorum counterexample;
6. two conflicting 3-of-5 views can both verify only with detectable equivocation;
7. invalid signatures are rejected.

## Limitation

Witness independence is simulated in one process. Real deployments need physically or administratively independent failure domains, protected private keys, authenticated publication, and durable evidence retention.
