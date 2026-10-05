# ODD addendum — E037 structural-drift revocation of early warning

## Purpose

Attack E036's strongest remaining assumption: discovery and holdout came from the same structural generator.

A different random seed is not enough if the generator omits a failure mechanism.

E037 therefore changes the failure law itself.

## Structural mutation

The E036 oracle already contains:

- cash failure;
- very low fully-loaded margin;
- very low market headroom;
- very low downstream success;
- strategic-exit dominance.

E037 adds an interaction-only failure:

```text
market_headroom * downstream_success_ratio < 0.15
```

This creates states where neither marginal threshold must independently look extreme, yet the joint state is unacceptable.

## Legacy warning

The frozen E036 threshold vector is evaluated unchanged on 1,000 states from the new structural generation.

Its recall falls below the prior 98% authority threshold.

The E036 warning therefore loses authority despite excellent performance on its original untouched holdout.

## Repair

The candidate repair keeps every E036 component and adds the interaction term.

On the same shifted generation:

- recall rises above 99%;
- precision remains above 99%;
- F1 improves over the legacy warning.

## Lifecycle consequence

The allowed warning lifecycle is now explicit:

```text
discover
→ holdout
→ promote
→ structural generation changes
→ revoke old certificate
→ diagnose new failure topology
→ add interaction-aware candidate
→ re-evaluate
→ promote new generation
```

This mirrors E016's adaptive-sampler revocation on the empirical warning plane.

## Promotion rule

`interaction-aware-warning-generation-v2`

## Limitation

The added interaction is deliberately synthetic. E037 demonstrates how model-family drift can destroy warning authority; it does not claim this exact interaction law governs real SaaS failure.
