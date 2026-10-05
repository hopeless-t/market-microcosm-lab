# ODD addendum — E089 predicate-scoped governance checkpoints

## Purpose

E087 identifies a real three-step public governance path:

`reporting break -> explicit exit criteria -> confirmed exit`

E089 attacks the opposite failure mode from E086: requiring the entire timeline for every decision.

## Exact checkpoint compilation

Each public checkpoint carries one reference claim:

- reporting break -> `REVIEW_REQUIRED`;
- explicit exit criteria -> `EXIT_CRITERIA_EXIST`;
- explicit dissolution/liquidation decision -> `EXIT_CONFIRMED`.

Exact subset search gives the minimum sufficient evidence:

- `REVIEW_REQUIRED`: reporting break only;
- `EXIT_CRITERIA_EXIST`: criteria checkpoint only;
- `EXIT_CONFIRMED`: exit event only;
- `CHECKPOINTED_GOVERNANCE_PATH`: all three checkpoints.

## Consequence

Evidence requirements are predicate-scoped.

The full timeline is indispensable only for a claim about the full governance path. Requiring it for a simple review or exit-status decision would add unnecessary evidence friction.

Promotion:

`governance-checkpoints-carry-predicate-specific-minimum-authority-v1`
