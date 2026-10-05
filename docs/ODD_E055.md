# ODD addendum — E055 redundant measurement synthesis after UNSAT

## Purpose

E054 correctly returns UNSAT when the original six unique pair probes are asked to correct two arbitrary probe errors.

E055 asks whether the requirement can be recovered by expanding the measurement design rather than weakening the robustness target.

## Expanded design

Each logical pair probe may be observed through multiple independent measurement channels.

The exact search allows 0–5 repetitions of each pair probe and requires minimum hypothesis-signature distance 5.

The minimum-cost satisfying design is:

```text
ab × 1
ac × 2
ad × 2
bc × 2
bd × 2
cd × 1
```

Result:

```text
channel count = 10
total declared cost = 20
minimum Hamming distance = 5
```

## Exhaustive decode

Five hypotheses are tested under:

- zero errors;
- every one-bit error;
- every two-bit error.

For 10 channels this gives:

```text
5 × (1 + 10 + C(10,2))
= 5 × 56
= 280 cases
```

Nearest-signature decoding recovers the correct hypothesis in all 280 cases.

## Consequence

E054's UNSAT meant:

```text
UNSAT under the current measurement alphabet
```

not:

```text
mathematically impossible under every expanded design
```

The recovery lifecycle becomes:

```text
compile robustness
→ UNSAT
→ expand authorized measurement design
→ recompile
→ exhaustively verify
→ promote only with a new certificate
```

## Promotion rule

`unsat-probe-robustness-may-expand-independent-measurement-channels-v1`

## Limitation

Repeated channels are assumed independent at the error level. Shared sensors, transforms, operators, or upstream roots can create correlated errors and revoke the distance-five interpretation.
