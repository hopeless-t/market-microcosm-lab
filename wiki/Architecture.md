# Architecture

## Inner loop

Observe → propose → simulate → verify → promote/reject → repeat.

Candidate search uses discovery scenarios. Promotion uses a separate untouched holdout.

## Meta loop

Alternative improvement systems run full inner loops. Their resulting policies are evaluated on a third meta-holdout that was not used by any inner loop.

The meta-loop can change observation design, candidate search width, simulation budget, horizon, estimators, and stress generation.

## Root of Trust

Within one constitutional generation, a candidate cannot rewrite:

- accounting conservation;
- Oracle isolation;
- held-out isolation;
- run/replay identity;
- independent promotion requirements.

Changing the constitution creates a new generation and requires recertification.

## Three truth levels

**World truth** — complete latent simulator state.

**Operational truth** — what the Governor may observe.

**Certification truth** — persisted evidence accepted by the independent Verifier.

Keeping these separate is the main defense against self-certifying improvement.
