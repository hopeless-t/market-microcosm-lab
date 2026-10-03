# ODD addendum — E015 adaptive boundary sampling

## Purpose

Improve the experiment machinery itself by reducing the number of expensive pair-surface evaluations required to locate market viability boundaries.

## Reference truth

E014 is the exhaustive oracle:

- 3 pressure pairs;
- 6 mechanisms;
- 7×7 cells per surface;
- 18 surfaces;
- 882 pair-cell evaluations.

E015 does not modify the market world. It benchmarks an adaptive query strategy against this fixed reference.

## Monotone staircase

For a monotone failure surface, each row has a threshold:

- cells below the threshold survive;
- cells at or above the threshold fail.

Starting at the highest B-pressure cell, the algorithm moves toward lower B while cells fail, moves to the next A row when a cell survives, and infers the remaining cells from the recovered thresholds.

The number of oracle queries is O(n) per surface rather than O(n²).

## Promotion criteria

Promotion requires all of:

- zero monotonicity violations in exhaustive truth;
- 100% cell-classification accuracy;
- 100% exact first-frontier recovery;
- exact interaction-only counts;
- at least 50% query savings.

## Trust boundary

E014 remains the verifier. E015 may improve the default exploratory evaluator but cannot delete the exhaustive audit path.

If future world changes violate monotonicity, the adaptive sampler must fail closed or fall back to exhaustive sampling.
