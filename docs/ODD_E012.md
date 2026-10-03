# ODD addendum — E012 evaluator meta-improvement

E012 reuses the E010 world and E011 pressure mapping.

## Meta-agent

The object being selected is an EvaluationDesign containing:

- a pressure curriculum;
- a discovery seed bank;
- a simulation horizon.

Each design evaluates the same mechanism family and selects one mechanism.

## Outer evaluation

Every selected mechanism is evaluated on a common meta-holdout with unseen seeds, broader pressure levels, and a longer horizon.

The outer score is lexicographic:

1. worst pressure-level survival;
2. mean survival;
3. mean survival duration;
4. worst ecosystem health;
5. mean ecosystem health.

Search cost breaks ties in favor of the cheaper evaluation design.

## Interpretation

If a stress-aware curriculum beats neutral-only evaluation, that is evidence that the improvement system itself became better at selecting robust policies inside the declared synthetic world.

It remains model-relative evidence, not a real-market prescription.
