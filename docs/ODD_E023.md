# ODD addendum — E023 hidden common-mode dependency

## Purpose

Test whether declared witness-domain independence remains meaningful when an unmodeled shared dependency affects multiple witnesses simultaneously.

## Nominal state

- five witnesses;
- 3-of-5 quorum;
- five independent one-witness shocks;
- homogeneous shock probability p = 0.01.

## Hidden dependency state

Add:

    hidden-shared-kms = {w0, w1, w2}

This shock is not represented by the nominal failure-domain labels.

## Exact method

For N shock variables, enumerate all 2^N subsets.

The probability of one subset is the product of each active shock probability and each inactive shock complement.

A subset is forge-capable when the union of affected witnesses contains at least three identities.

## Diagnostic quantities

- exact forge probability;
- minimum shocks to forge;
- minimal forge-capable shock subsets;
- inflation ratio hidden / nominal.

## Interpretation

The experiment distinguishes declared topology from causal dependency structure.

A common-mode hyperedge can invalidate independence even when every witness has a unique nominal domain label.

## Trust boundary

The model can only test dependencies it is told about.

Detecting unknown real dependencies requires inventory, telemetry, organizational review, fault injection, or other external evidence.
