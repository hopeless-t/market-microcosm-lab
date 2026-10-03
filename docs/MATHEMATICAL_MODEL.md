# Mathematical model

## State

A minimal state can include:

- user population, utility distribution, churn and acquisition;
- developer and publisher cash buffers, burn rates, capacities, entry and exit;
- platform reserve, operating cost, price and take rate;
- content stock, quality, novelty, genre/category and age;
- exposure/recommendation allocation;
- demand and substitution structure;
- market concentration and diversity;
- exogenous shocks.

Write the state as \(x_t\in\mathcal X\).

## Actions

\[
a_t=(payout, floor, ecosystem\_fund, exposure, price, take, grants, rules,\ldots)
\]

subject to feasibility constraints.

## Dynamics and uncertainty

\[
x_{t+1}=F_\theta(x_t,a_t,w_t), \quad y_t=H(x_t)+\varepsilon_t.
\]

\(\theta\) represents uncertain structural parameters; \(w_t\) represents shocks; \(y_t\) is what the Observer exposes.

Research runs should evaluate an ensemble \(\Theta\), not one privileged calibration.

## Viability constraints

Examples:

\[
cash_i(t) \ge 0
\]

for required solvent actors, or a stronger reserve/burn margin;

\[
U_{user}(t)\ge U_{min},\quad Q(t)\ge Q_{min},
\]

\[
HHI(t)\le HHI_{max},\quad EntryRate(t)\ge E_{min}.
\]

The exact constraint set is versioned and explicit.

## Long-run objective

Only after hard constraints hold:

\[
J(\pi)=
\mathbb E\left[\sum_{t=0}^{T}\beta^t
W(x_t,a_t)\right].
\]

Use a vector of welfare dimensions for analysis. Scalarization is experiment-specific and must not become an unexamined universal truth.

## Robust control view

At each decision point, choose an action that keeps future state inside a robust control-invariant/viable region while optimizing economic value over a rolling horizon. This connects the lab naturally to robust economic model-predictive control.

## Promotion statistic

For challenger \(c\) and incumbent \(b\), on held-out scenarios:

\[
\Delta_k=M_k(c)-M_k(b).
\]

Promotion requires:

1. zero invariant violations;
2. catastrophic-failure risk below a declared upper confidence bound;
3. no unacceptable degradation on protected metrics;
4. a positive lower confidence bound for at least one declared target improvement, or a declared Pareto improvement;
5. acceptable train/validation-to-held-out generalization gap.

Thresholds are configuration, not hidden code constants.

## Meta-objective

The outer loop scores the improvement machinery itself using quantities such as:

\[
J_{meta}=
- Regret
- \lambda FP_{promotion}
- \mu GeneralizationGap
+ \eta DiscoveryRate
+ \rho SampleEfficiency.
\]

A faster loop that makes more false promotions is not an improvement.
