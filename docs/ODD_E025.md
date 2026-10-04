# ODD addendum — E025 regional empirical complexity knee

## Purpose

Use an admitted E024 empirical source to choose model complexity rather than importing a synthetic convenience assumption into empirical calibration.

Netflix reports regional streaming revenue, paid memberships, and ARM for UCAN, EMEA, LATAM, and APAC across Q2 2023 through Q2 2024 in its Q2 2024 shareholder letter.

E025 asks how many regional ARM groups are required to compress that published structure while keeping a declared maximum relative error below 10%.

## Evidence split

Discovery quarters:

- Q2 2023;
- Q3 2023;
- Q4 2023;
- Q1 2024.

Holdout quarter:

- Q2 2024.

The holdout is not used to choose the structural partition.

## Candidate model family

A candidate is a partition of the four reporting regions.

For each group and discovery quarter, the representative ARM is the paid-membership-weighted mean of member regions.

For a region (r):

```text
relative_error[r] = abs(predicted_ARM[r] - observed_ARM[r]) / observed_ARM[r]
```

Every set partition of the four regions is enumerated exactly.

For each group count (k = 1, 2, 3, 4), E025 selects the partition with:

1. minimum worst-quarter maximum relative error;
2. then minimum mean membership-weighted RMSE;
3. then deterministic lexical partition order.

This makes the complexity boundary an exact small-world oracle rather than a clustering heuristic.

## Discovery result

Across Q2 2023 through Q1 2024:

- one group has worst maximum relative error above 50%;
- two groups remain above 20%;
- three groups fall below 9%;
- four groups reproduce the four published region values exactly.

The minimum model satisfying the 10% tolerance is therefore three groups.

The selected topology is:

```text
{UCAN}
{EMEA}
{LATAM, APAC}
```

The same three-group topology is optimal in each individual quarter in the five-quarter source window.

## Forward holdout

After structure selection, the selected topology is calibrated on Q1 2024 only. Those group centroids are frozen and used to predict Q2 2024 ARM.

The one-quarter-forward maximum relative error remains below 10%.

This is deliberately stronger than merely refitting the Q2 2024 holdout.

## Interpretation

E025 identifies a **complexity knee** in this specific published aggregate window.

It does not claim that LATAM and APAC are causally one market, that ARM equals subscription price, or that three regions are universally sufficient. It only rejects the one-global-parameter and two-group empirical ARM model families at the declared tolerance while showing that a three-group compression survives a short forward holdout.

## Meta-loop consequence

The empirical loop can now reject an overly simple simulator assumption before fitting a larger market world:

```text
public evidence admission
→ exact model-family enumeration
→ complexity knee
→ untouched temporal holdout
→ promote structural constraint
→ build next empirical world
```

The promoted constraint is `regional-arm-complexity-knee-k3-v1`.

## Next step

E026 should move from parameter heterogeneity to observation heterogeneity: use SARTRAS's sampled institution reports to test whether a governor that sees only sampled usage can recover allocation-relevant population structure without receiving Oracle truth.
