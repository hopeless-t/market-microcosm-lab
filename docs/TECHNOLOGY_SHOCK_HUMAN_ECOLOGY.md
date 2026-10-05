# Technology shocks as human-ecology transitions

## Research question

Can Market Microcosm model AI, typewriters, digital photography, spreadsheets, search engines, industrial robots, and similar technologies on one axis: a technology shock that changes the production function of tasks and forces an ecosystem-level reallocation of human activity?

The core framing is deliberately non-anthropomorphic:

```text
AI is not modeled as a new human worker.
AI is modeled as a technology that changes task cost, quality, capacity, latency, and complementarity.
```

The important question is therefore not only whether a named occupation grows or shrinks. The higher-level question is whether the human ecosystem remains viable while obsolete task bundles dissolve and new task bundles, firms, skills, consumption patterns, and forms of value emerge.

## Historical analogues

Examples such as the decline of dedicated typist roles or neighborhood photo-processing shops are useful as analogues, not as proof of a universal law. In both cases, technology can destroy a formerly valuable task bundle without implying that aggregate economic activity must contract. The displaced labor, capital, demand, and capabilities may be reallocated into other activities.

This motivates a general model of transition rather than a binary `technology creates jobs / technology destroys jobs` claim.

## Atomic model

Let a job be a bundle of tasks rather than an indivisible object:

\[
J_i = \{\tau_{i1},\tau_{i2},\ldots,\tau_{in}\}.
\]

A technology shock changes the effective production parameters of each task:

\[
\tau_k:
(c_k, q_k, \ell_k, s_k, a_k)
\rightarrow
(c'_k, q'_k, \ell'_k, s'_k, a'_k),
\]

where:

- \(c\): marginal cost;
- \(q\): achievable quality;
- \(\ell\): latency;
- \(s\): substitutability for human execution;
- \(a\): augmentability/complementarity with human execution.

The occupation changes only after firms rebundle tasks around the new production frontier.

## Firm response

For firm \(f\), let the production function be:

\[
Y_f = F_f(H_f, K_f, T_f; \theta_f),
\]

with human labor \(H\), capital \(K\), and technology \(T\).

A technology shock does not directly remove a person. It modifies the relative productivity and cost of combinations of \(H\), \(K\), and \(T\). The firm then chooses a new bundle subject to demand, verification cost, liability, regulation, coordination cost, and transition friction.

Important state variables include:

- substitution pressure;
- augmentation gain;
- demand elasticity after price decline;
- verification and liability cost;
- task rebundling cost;
- retraining cost;
- organizational migration friction;
- local/physical/presence constraints;
- human-authenticity or relationship premium.

## Reallocation loop

The primary loop is:

```text
technology shock
  -> task production frontier changes
  -> firm task bundles change
  -> product price / quality / capacity changes
  -> demand changes
  -> labor demand changes by task
  -> wages and entry incentives change
  -> workers retrain / migrate / exit / create firms
  -> household income and consumption change
  -> demand changes again
  -> new equilibrium or collapse regime
```

This is intentionally circular. A one-step employment comparison is insufficient.

## Human-ecosystem viability

The experiment should protect human populations, not specific historical occupations.

Candidate viability constraints include:

\[
IncomeFloor_p(t) \ge I_{min},
\]

\[
Participation_p(t) \ge P_{min},
\]

\[
SkillReproduction_p(t) \ge S_{min},
\]

\[
Mobility_p(t) \ge M_{min},
\]

\[
Welfare_p(t) \ge W_{min},
\]

for protected population/cohort \(p\).

Additional ecological metrics:

- transition unemployment duration;
- real household consumption;
- income and wealth concentration;
- new-firm entry rate;
- occupational/task diversity;
- regional concentration;
- retraining burden;
- intergenerational mobility;
- skill pipeline continuity;
- social participation and non-wage utility;
- resilience to the next technology shock.

A world can therefore satisfy:

```text
aggregate output rises
and
specific occupations collapse
and
human welfare still improves
```

or the opposite:

```text
aggregate output rises
while
transition costs, concentration, or skill-pipeline failure
push protected human populations outside the viability region.
```

The model must distinguish these cases.

## Skill-reproduction failure mode

A particularly important delayed effect is the training pipeline.

If junior tasks are automated first:

\[
JuniorTaskDemand_t \downarrow,
\]

then short-run productivity may rise while future expert supply falls:

\[
ExpertSupply_{t+k}
=
ExpertSupply_t
+ TrainingFlow_t
- Attrition_t.
\]

A technology policy that looks optimal in one period can therefore become non-viable after a delay if it destroys the apprenticeship path that regenerates scarce human capability.

## Species-level framing without anthropomorphizing technology

For this experiment, the modeled ecological subject is the human population. Technology is part of the environment and production apparatus, not a competing biological species.

The key research objective is:

> Find transition policies and institutional mechanisms that allow large productivity shocks while keeping human populations inside a robust long-run viability region.

Possible control variables include:

- retraining grants;
- transition-income support;
- portable benefits;
- apprenticeship subsidies;
- reduced barriers to firm creation;
- worker ownership / revenue participation;
- shorter work time when productivity rises;
- public or cooperative access to productivity tools;
- regional transition funds;
- tax/transfer rules;
- credential reform;
- task-market and matching infrastructure.

These are experiment controls, not policy endorsements. Their effects should be compared under multiple structural models and adversarial shocks.

## Proposed experiment family

### T001 — Occupation-neutral technology shock

Create several synthetic task bundles and apply a shock that reduces the cost of a subset of tasks by 90% while varying substitutability and augmentability.

Measure:

- output;
- price;
- employment by task and occupation;
- wages;
- entry/exit;
- worker migration;
- household consumption;
- transition duration.

### T002 — Historical-shape analogues

Construct stylized, non-causal analogues for:

- typist / word-processing transition;
- local photo-processing / digital-camera transition;
- bookkeeping / spreadsheet transition;
- search / information-retrieval transition;
- generative-AI task transition.

The goal is not to fit history exactly. The goal is to test whether one mechanism family can represent both occupation collapse and continued aggregate expansion.

### T003 — Human viability controller

Compare laissez-faire rebundling against bounded transition mechanisms. Search for policies that preserve:

- aggregate productivity gain;
- protected population viability;
- skill reproduction;
- entry and diversity;
- fiscal feasibility.

### T004 — Delayed skill-pipeline adversary

Make junior-task automation look beneficial for several periods, then expose a delayed shortage of experts. Require any promoted policy to survive the full horizon rather than only the immediate productivity window.

### T005 — Concentration adversary

Let technology access have high fixed cost or proprietary control. Test whether output can rise while human welfare falls through market concentration, rent extraction, or reduced entry.

### T006 — Democratized-tool counterfactual

Repeat T005 with low-cost broad access to the same productivity technology. Compare whether the same technical capability produces a different ecological outcome under different ownership/access structures.

## Promotion gate

A candidate transition mechanism may be promoted only when:

1. hard accounting and feasibility invariants pass;
2. aggregate output gains are not achieved by silently violating protected-population floors;
3. transition unemployment and skill-pipeline risks stay below declared limits;
4. no single structural model is treated as privileged;
5. delayed and concentration adversaries are included;
6. results are reported as conditional model evidence, not universal causal truth.

## Source stimulus

Initial stimulus:

- Noah Smith, summarized in Japanese at `https://econ101.jp/noah-smith_ai-isnt-taking-college-jobs/`

The article is useful as a trigger for the research question, but this document intentionally generalizes beyond AI and beyond any single empirical interpretation of current graduate employment.

## Claim ceiling

This proposal does **not** claim that AI cannot cause aggregate contraction, that all displaced workers will be smoothly reallocated, or that historical technology transitions guarantee benign outcomes.

The narrower claim is:

> Occupation loss and aggregate economic decline are different observables. Market Microcosm should model the full reallocation ecology and ask which transition regimes preserve human viability under technology shocks.
