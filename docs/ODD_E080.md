# ODD addendum — E080 reporting policy as an observation kernel

## Purpose

E079 promotes KPI withdrawal into a first-class observation event.

E080 moves one layer deeper: the withdrawal changes the **observation kernel**, not merely the number of values present in one unchanged dataset.

## Kernel generations

Before withdrawal, the reference rich kernel exposes revenue, operating profit, stock revenue, stock ratio, ARR, churn, customer count, and average unit price.

After the Allied overseas-SaaS disclosure change, the reference degraded kernel exposes only revenue and operating profit.

The same latent state therefore maps to different public observations depending on the active reporting kernel.

## Fail-closed semantics

A KPI not emitted by the active kernel is:

`NOT_OBSERVED_UNDER_ACTIVE_KERNEL`

It is not encoded as zero and is not implicitly imputed.

Cross-kernel estimators require both metric visibility and an explicit comparability bridge. The E080 reference has no bridge, so ARR trend estimation across the withdrawal boundary returns:

`ABSTAIN_KERNEL_BREAK`

Even a metric visible in both kernels does not automatically receive cross-kernel trend authority when the reporting regime itself changed and no bridge was admitted.

## Consequence

A future replacement KPI set is a **new kernel generation**, not an automatic continuation of the old KPI series.

Promotion:

`reporting-policy-change-creates-new-observation-kernel-generation-v1`

## Limitation

The latent numeric state used in the exact reference is synthetic. It exists only to prove the observation-operator distinction and is not an estimate of undisclosed company KPI values.
