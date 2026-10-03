# Meta-improvement loop

The inner loop improves ecosystem policy. The outer loop improves the inner loop.

## Objects the meta-loop may change

- observation/sampling strategy;
- causal estimator;
- candidate generator;
- search algorithm;
- simulation budget allocation;
- planning horizon;
- uncertainty model;
- stress-test generator;
- metric estimator;
- experiment stopping rule.

## Objects it may not silently change

- accounting conservation;
- run/replay identity semantics;
- held-out isolation;
- protected hard constraints;
- promotion evidence requirements.

Those belong to the Root of Trust. They can evolve only as a separately versioned constitutional change, after re-evaluating historical baselines.

## Meta-loop health metrics

Track:
- oracle regret;
- false-promotion rate;
- false-rejection rate where measurable;
- discovery rate of real improvements;
- sample efficiency;
- time-to-diagnosis;
- generalization gap;
- calibration error of predicted intervention effects;
- robustness under adversarial scenario generation;
- reproducibility rate.

## Meta-pressure-knee experiments

Treat the improvement loop itself as an ecosystem. Sweep search aggressiveness, observation compression, simulation budget, promotion alpha, and horizon. Locate knees where faster adaptation suddenly increases false promotion or collapse risk.

The target is not maximal loop speed. It is maximal trustworthy improvement throughput.
