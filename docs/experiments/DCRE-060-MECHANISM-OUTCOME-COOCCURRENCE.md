# DCRE-060 — Mechanism/outcome co-occurrence is not causal effectiveness

## Trigger

DCRE-059 maps a real utility governance bundle onto synthetic DCRE failure modes. The mechanisms are observable in Northern Wasco County PUD’s public large-load framework.

The next temptation is causal:

> If the utility also reports favorable outcomes, did those mechanisms cause the outcomes?

DCRE-060 refuses that jump.

## Publicly reported outcome claims

Northern Wasco County PUD and Oregon Data Center Advisory Committee materials report or describe favorable outcomes alongside the governance bundle, including:

- residential rates remaining comparatively low;
- no reported crowd-out of other industries in the utility’s service territory;
- cost-assignment rules intended to prevent large-load infrastructure and power costs from being shifted to base customers.

Relevant primary/public sources include:

- Northern Wasco County PUD — Data Center Services
  - https://www.nwascopud.org/about-us/data-center-services/
- Oregon Department of Energy — May 29, 2026 Data Center Advisory Committee facilitator summary
  - https://www.oregon.gov/energy/get-involved/Documents/2026-05-29-DCAC-Facilitator-Meeting-Summary.pdf

## Evidence hierarchy

DCRE-060 stores these as **source-reported outcome claims**, not as an independent causal evaluation.

The current evidence does not provide:

```text
randomized treatment
quasi-experimental control
matched untreated utility
pre-registered causal model
counterfactual without the governance bundle
```

Therefore:

```text
mechanism_bundle_observed            = TRUE
favorable_outcome_claims_coexist     = TRUE
independent_causal_evaluation        = FALSE
counterfactual_observed              = FALSE
```

and the inference:

```text
mechanism bundle
+ favorable outcome claims
-> mechanism caused favorable outcomes
```

is blocked.

## Why this matters

The synthetic DCRE chain repeatedly shows that apparently safe controls can create second-order failures. Real institutions should be held to the same discipline.

A governance mechanism can:

- be sensible;
- target a real failure mode;
- coexist with favorable outcomes;

and still lack identified causal effectiveness.

That does not make the mechanism useless. It sets the correct empirical authority ceiling.

## Machine-readable result

```text
mechanism_bundle_observed             = TRUE
favorable_outcome_claims_coexist      = TRUE
all_outcomes_independently_verified   = FALSE
counterfactual_observed               = FALSE
mechanism_caused_favorable_outcomes   = UNKNOWN
causal_effectiveness_identified       = FALSE
authority_effect                      = NONE
```

## Result

DCRE-060 creates a three-level empirical ladder:

```text
Level 1: mechanism exists
Level 2: favorable outcome coexists
Level 3: causal effectiveness identified
```

Current evidence reaches Levels 1–2 only.

## Claim ceiling

```text
claim_ceiling = MECHANISM_OUTCOME_COOCCURRENCE_ONLY
```

No welfare gain, rate reduction effect, reliability effect, anti-cross-subsidy effectiveness, or policy optimality is inferred.

## Next falsifier

DCRE-061 should look for a more independent outcome surface—statewide or federal electricity-rate data, reliability statistics, audited utility financials, or comparable-utility panels—and ask whether any relevant outcome can be independently cross-checked. Even then, comparison would remain observational unless a credible counterfactual design is available.
