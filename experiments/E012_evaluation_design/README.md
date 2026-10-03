# E012 — Meta-improvement of the evaluator

E010's neutral baseline gave every mechanism a full survival rate. That means a neutral-only benchmark is too weak to discriminate long-run robustness.

E012 therefore makes the **evaluation curriculum itself** the object of meta-improvement.

## Candidate evaluation designs

### Neutral-only
Select mechanisms using pressure level 0 only.

### Mild curriculum
Select mechanisms across pressure levels 0–3.

### Boundary curriculum
Select mechanisms across pressure levels 1–5, deliberately including worlds near and beyond the preliminary E011 knees.

Each design chooses a mechanism using its own discovery seed bank.

## Meta verification

The selected mechanisms are then evaluated on a common, isolated meta bank:

- pressure levels 2–6;
- new seeds unseen by every design;
- a longer horizon.

The evaluation design that produces the most robust selected mechanism wins.

## Why this is a meta-loop experiment

E012 does not primarily ask which allocation mechanism is best. It asks which **method of choosing mechanisms** generalizes best to stressful worlds.

This is a concrete implementation of improving the self-improvement loop rather than only improving its current policy.
