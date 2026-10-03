# E014 — Pairwise interaction surfaces

E013 showed that no single pressure axis produced a preliminary survival knee before level 6, while E011's composite pressure produced knees at levels 3–4.

E014 tests whether two moderate stresses are sufficient to advance collapse.

## Pairwise surfaces

Three 7×7 grids are evaluated for every mechanism:

- subscription price × platform operating cost;
- subscription price × baseline churn;
- platform operating cost × baseline churn.

Levels 0–6 reuse the E013 step definitions.

## Interaction-only cells

A grid cell is marked **interaction-only** when:

- the pair has observed survival below 90%;
- axis A alone at the same level has survival at least 90%;
- axis B alone at the same level has survival at least 90%.

This is direct model-relative evidence that the joint intervention crosses the viability boundary even though neither component does so alone at the matched intensity.

## Survival-loss interaction metrics

For each cell:

    loss = 1 - survival_rate

Two excess measures are stored:

    joint_loss - max(single_loss_a, single_loss_b)

and

    joint_loss - min(1, single_loss_a + single_loss_b)

The second is a stricter super-additivity test with respect to observed survival loss.

## Frontier

For each mechanism and pair, E014 records the failing cell with the smallest total pressure level. Ties prefer lower peak axis level and more balanced pressure.

A separate biopsy seed bank captures the first failing trajectory at that frontier.

## Limitations

The grid is coarse and model-relative. Positive interaction is not evidence of real-world causal interaction until a calibrated empirical design exists.
