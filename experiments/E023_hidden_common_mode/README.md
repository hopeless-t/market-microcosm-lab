# E023 — Hidden common-mode dependency adversary

E022 separates witness identities from declared failure domains. E023 attacks the declarations themselves.

## Nominal model

Five witnesses are declared independent.

Each witness has one independent 1% compromise shock.

For a 3-of-5 quorum, at least three independent shocks are required to forge.

## Hidden dependency

A sixth undeclared shock is introduced:

    hidden-shared-kms → witnesses 0, 1, 2

The witness labels and nominal domains remain unchanged, but one latent shock can now compromise a full quorum.

## Exact enumeration

All shock subsets are enumerated.

At 1% homogeneous shock probability:

- nominal independent forge probability ≈ **0.000985%**;
- hidden-common-mode forge probability ≈ **1.000975%**.

The hidden dependency inflates modeled forge probability by more than **1000×** and collapses the minimum forge shock count from 3 to 1.

## Why this matters

A topology can look fully independent in configuration while depending on one shared KMS, operator, CI/CD system, network route, root credential, or legal/administrative control plane.

Independence labels are therefore hypotheses, not evidence.

## Promotion

The experiment promotes a dependency-audit rule only if:

1. the nominal model needs three shocks;
2. the hidden model needs one;
3. the single shared-KMS shock reaches quorum;
4. modeled forge probability inflates by more than 100×;
5. the hidden model crosses 1% forge probability under the synthetic 1% shock rate;
6. every shock subset is enumerated.

## Limitation

The dependency and probabilities are synthetic. E023 measures sensitivity to an undeclared common mode; it does not estimate real infrastructure risk.
