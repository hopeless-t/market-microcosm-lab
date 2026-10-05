# ODD addendum — E052 minimum lineage-probe portfolio

## Purpose

E051 demonstrates that active probes can reveal a hidden common root.

E052 asks how few probe interventions are actually necessary.

This turns lineage discovery into an exact experiment-design problem.

## Hypothesis family

Four sources `a,b,c,d` admit five reference hypotheses:

- no shared root;
- abc share one hidden root;
- abd share one hidden root;
- acd share one hidden root;
- bcd share one hidden root.

## Candidate probes

Each pair probe asks whether the two named sources respond as members of the same hidden shared-root group.

The six candidate pair probes have declared synthetic costs:

```text
ab=1, ac=1, ad=2, bc=2, bd=3, cd=3
```

## Exact search

All probe subsets are enumerated.

A portfolio is identifying only if every admissible root hypothesis produces a unique binary response signature.

The exact minimum-cost portfolio is:

```text
ab, ac, bc
probe count = 3
total cost = 4
```

Its signatures are unique across all five hypotheses.

## Consequence

The objective is not maximum probing.

It is:

```text
minimize intervention cost
subject to
every admissible lineage hypothesis being distinguishable
```

This is the lineage-discovery analogue of E041/E045 minimal sufficient observability.

## Promotion rule

`lineage-discovery-probes-use-exact-minimum-identifying-portfolio-v1`

## Limitation

The hypothesis family is finite and tiny, outcomes are noiseless/binary, and costs are synthetic. Larger systems need adaptive bounded search and noisy information-gain methods.
