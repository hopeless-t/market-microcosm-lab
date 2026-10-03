# E015 — Adaptive boundary sampling

E014 exhaustively evaluates 49 cells for every mechanism × pressure pair. That produces a trustworthy interaction surface, but it is expensive.

E015 treats E014 as a hidden oracle and asks whether a cheaper boundary-search algorithm can recover the same result.

## Candidate

monotone-staircase-boundary-sampler-v1

The candidate assumes that failure is monotone in each pressure axis: once a cell fails, cells with equal-or-higher pressure on both axes also fail.

For each 7×7 surface, it walks the survival/failure boundary from the high-B edge. A monotone n×n surface needs only O(n) oracle queries rather than O(n²).

## Independent checks against E014

The E014 exhaustive truth is used only as the verifier.

For every one of 18 surfaces, E015 checks:

- monotonicity violations;
- all-cell survival/failure classification;
- exact first-frontier recovery;
- exact interaction-only cell count;
- query cost.

## Promotion gate

The adaptive sampler is promoted only if:

1. E014 contains zero monotonicity violations;
2. all 882 cells are inferred exactly;
3. all 18 first frontiers are recovered exactly;
4. all interaction-only counts are recovered exactly;
5. pair-surface query cost falls by at least 50%.

Even after promotion, exhaustive E014 remains the periodic audit/reference path because future richer worlds may break monotonicity.
