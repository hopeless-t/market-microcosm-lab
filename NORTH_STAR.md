# North Star

## Research question

What allocation, recommendation, pricing, funding, and governance rules keep a pooled-revenue market ecosystem viable over long horizons while preserving user value, service quality, diversity, innovation, and the ability of new actors to enter?

The target is not one-period profit and not one scalar engagement metric.

## Primary object: robust viability

Let ecosystem state be \(x_t\), intervention be \(a_t\), uncertain parameters be \(\theta\), and disturbance be \(w_t\):

\[
x_{t+1}=F_\theta(x_t,a_t,w_t).
\]

Let \(\mathcal C\) be the acceptable region defined by hard survival and integrity constraints.

The central object is the robust viability kernel:

\[
\operatorname{Viab}(\mathcal C)=
\{x_0\mid \exists\pi,\; x_t\in\mathcal C\;\forall t,\forall w\in\mathcal W\}.
\]

A policy is interesting when it enlarges the viable region, increases safety margin inside it, or improves welfare without shrinking viability.

## Lexicographic objective

1. Preserve accounting and model invariants.
2. Keep essential actor classes viable.
3. Keep minimum user utility and service quality.
4. Avoid pathological concentration and loss of entry.
5. Subject to 1-4, improve long-run welfare, diversity, innovation, and efficiency.

No candidate may trade a hard invariant for a higher aggregate score.

## Anti-goals

- Do not optimize watch/play time as a proxy for welfare.
- Do not let the controller define the metric that certifies itself.
- Do not use oracle-only hidden state in deployable policies.
- Do not treat calibration fit as proof of causal correctness.
- Do not promote a policy on the same scenario seeds used to discover it.
