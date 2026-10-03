# ODD addendum — E014 pairwise pressure interactions

E014 reuses E010 entities, E013 axis definitions, and the 60-period ecological viability criteria.

## Purpose

Test whether simultaneous moderate stress on two axes can cross the viability boundary earlier than either matched single-axis intervention.

## Factors

Pairwise grids:

1. subscription price multiplier × platform cost multiplier;
2. subscription price multiplier × baseline churn rate;
3. platform cost multiplier × baseline churn rate.

Each axis uses levels 0–6.

## Evidence

- grid evaluation seeds: 15000–15011;
- frontier biopsy seeds: 16000–16039;
- horizon: 60.

These banks are disjoint from E010–E013 banks.

## Interaction-only definition

A cell is interaction-only if pair survival is below 90% while both matched single-axis survivals are at least 90%.

## Excess survival loss

Let:

    L_pair = 1 - S_pair
    L_a = 1 - S_a
    L_b = 1 - S_b

E014 reports:

    Delta_max = L_pair - max(L_a, L_b)

and:

    Delta_add = L_pair - min(1, L_a + L_b)

Positive Delta_add means observed pair survival loss exceeds the sum of matched single-axis survival losses.

## Frontier selection

For each mechanism/pair, the first frontier minimizes:

1. level_a + level_b;
2. max(level_a, level_b);
3. absolute level imbalance;
4. level_a;
5. level_b.

## Interpretation boundary

E014 identifies interaction inside a declared synthetic model. It does not establish a causal interaction in any named real market.
