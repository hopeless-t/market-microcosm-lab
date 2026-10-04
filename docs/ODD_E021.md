# ODD addendum — E021 witness quorum

## Purpose

Reduce dependence on a single provenance-anchor authority by requiring a threshold of independent checkpoint witnesses and by retaining evidence of witness equivocation.

## Entities

Witness:

- stable witness ID;
- synthetic secret key.

Attestation:

- checkpoint sequence;
- checkpoint hash;
- witness ID;
- HMAC-SHA256 signature.

## Quorum rule

The candidate rule is 3-of-5.

Only unique valid witness identities count toward the threshold.

## Exact geometry

The experiment enumerates all exact-size quorum subsets.

For witness count n and quorum threshold q, two quorums are guaranteed to intersect when:

    2q > n

For n=5:

- q=3 is intersecting;
- q=2 is not.

## Compromise model

Honest witnesses do not attest to a forged checkpoint.

A forged checkpoint therefore needs at least q compromised witnesses.

For q=3, the tested boundary is:

- 1 compromised → fail;
- 2 compromised → fail;
- 3 compromised → pass.

## Split-view model

Two different checkpoint hashes are issued for the same sequence.

The fixed 3-of-5 views use witness sets:

    {0,1,2}
    {2,3,4}

Both satisfy quorum. The intersection witness has signed both views, producing retained equivocation evidence.

## Trust boundary

Quorum intersection guarantees evidence only if attestations are authenticated and retained.

It does not prevent compromise of q witnesses, key theft, correlated witness failures, or suppression of evidence.

The current HMAC implementation is a deterministic research stand-in for independently held signing keys, not a deployment cryptosystem.
