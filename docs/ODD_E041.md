# ODD addendum — E041 minimal observability checkpoint

## Purpose

Find the smallest additional observation needed to repair the current-state ambiguity exposed by E040.

For a fixed-width rolling sum:

```text
S_t = S_(t-1) - outgoing_oldest + newest
```

Two consecutive rolling metrics therefore reveal only:

```text
newest - outgoing_oldest
```

They do not identify either term separately.

## Exact reference

Use:

```text
previous six-month MRR = [10, 8, 6, 4, 2, 0]
newest MRR = 2
current window = [8, 6, 4, 2, 0, 2]
```

The corresponding reported ARR values are:

```text
previous ARR = 60
current ARR = 44
```

Without the outgoing boundary value, the bounded 0–10 integer state admits three pairs:

```text
(outgoing, newest)
(8, 0)
(9, 1)
(10, 2)
```

Current MRR is still ambiguous.

If the one outgoing boundary scalar is retained:

```text
newest
= current_sum - previous_sum + outgoing
= 22 - 30 + 10
= 2
```

The newest MRR is recovered exactly.

## Checkpoint principle

For this one-step observability task, retaining the entire six-month path is unnecessary.

One indispensable boundary checkpoint is sufficient.

This provides a concrete empirical-evidence example of the broader design principle:

```text
preserve the smallest checkpoint
whose absence makes the transition non-identifiable
```

## Promotion rule

`rolling-window-boundary-checkpoint-restores-observability-v1`

## Limitation

The checkpoint reconstructs only the newest scalar under a known exact fixed-width window. Noisy observations, metric-definition changes, product mixtures, or reconstruction of the full interior path require additional state.
