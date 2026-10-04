# ODD addendum — E078 cross-company churn / ARR sign replication

E063 found within BBD FY2025 that churn direction does not determine ARR direction.

E078 freezes one of those counterexamples — **churn up while ARR also rises** — and tests it against an independent public company.

Source: Allied Architects FY2023 full-year financial results presentation, page 30.

Published domestic SaaS data:

```text
2023-Q1 ARR  831m JPY, churn 4.1%
2023-Q2 ARR  919m JPY, churn 3.4%
2023-Q3 ARR 1010m JPY, churn 3.0%
2023-Q4 ARR 1080m JPY, churn 4.5%
```

Q3 -> Q4 therefore gives:

```text
ARR   +70m JPY
churn +1.5 percentage points
```

The company states that account cancellations remained controlled while increased downgrades temporarily worsened its MRR-based gross revenue churn.

The ARR increase exactly decomposes across the three products:

```text
Letro              +65
LetroStudio        +16
Monipla Fan Blog   -11
----------------------
total              +70m JPY
```

The legacy Monipla Fan Blog is explicitly described as strategically decreasing.

Thus aggregate ARR growth, churn deterioration, and deliberate legacy-product contraction coexist in the same quarter.

BBD and Allied Architects now independently contain churn-up / ARR-up transitions.

This does not estimate a universal probability. It promotes a stronger counterexample class:

`churn-arr-sign-counterexample-replicates-cross-company-v1`.
