# ODD addendum — E054 probe robustness compiler

## Purpose

Generalize E052 and E053 into one authority compiler.

E052 finds the cheapest noiseless identifying probe set.

E053 finds the cheapest one-error-correcting probe set.

E054 makes the tolerated observation error budget an explicit input.

## Coding bound

For worst-case binary substitution errors, correcting up to (e) errors requires minimum pairwise signature distance:

```text
d_min >= 2e + 1
```

The compiler exactly enumerates probe subsets and selects the minimum-cost subset satisfying that certificate.

## Reference compilation

### e = 0

Required distance:

```text
1
```

Compiled portfolio:

```text
ab, ac, bc
probe count = 3
cost = 4
```

This recovers E052.

### e = 1

Required distance:

```text
3
```

Compiled portfolio:

```text
ab, ac, ad, bc, bd, cd
probe count = 6
cost = 12
```

This recovers E053.

### e = 2

Required distance:

```text
5
```

No subset of the six reference probes can satisfy the requirement.

The compiler returns:

`UNSAT`

It does not silently downgrade the robustness contract.

## Consequence

Robustness is no longer attached informally to a probe set.

Authority is compiled from:

```text
declared threat / error budget
→ required code distance
→ exact portfolio search
→ SAT certificate or UNSAT
```

## Promotion rule

`lineage-probe-authority-compiled-from-declared-error-budget-v1`

## Limitation

The certificate is specific to worst-case binary substitution errors. Erasures, correlated errors, continuous observations, and probabilistic models need a different compiler.
