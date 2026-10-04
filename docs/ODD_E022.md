# ODD addendum — E022 failure-domain diversity

## Purpose

Measure how much nominal 3-of-5 witness security survives when witness failures are correlated through shared infrastructure or administration.

## Entities

WitnessTopology:

- five witness slots;
- 3-of-5 quorum threshold;
- one failure-domain label per witness.

Reference topologies:

    concentrated: 3-1-1
    balanced:     2-2-1
    independent:  1-1-1-1-1

## Correlated event model

A domain event affects every witness assigned to that domain.

Two event types are evaluated:

- compromise — all affected witnesses can attest to a forged checkpoint;
- outage — all affected witnesses become unavailable.

Domains are treated as mutually independent in the probability calculation.

## Exact enumeration

For D domains, all 2^D domain subsets are enumerated.

A compromised subset can forge if compromised witness count is at least three.

An outage subset breaks availability if fewer than three witnesses remain online.

## Probability model

For homogeneous domain-event probability p, the probability of one exact subset S is:

    p^|S| * (1-p)^(D-|S|)

Exact forge or availability-loss probability is the sum over all subsets that trigger the corresponding condition.

## Promotion target

The strongest reference topology is the fully independent five-domain arrangement.

Promotion requires a minimum of three domain compromises to forge and the explicit exact-enumeration gates defined by E022.

## Trust boundary

The experiment measures consequences of declared domain assignments.

It does not prove that two declared domains are truly independent. Hidden common dependencies remain an external-validity problem.
