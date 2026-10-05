# ODD addendum — E088 effective period vs public availability

## Purpose

E087 identifies an explicit exit-criteria checkpoint between reporting break and eventual exit.

The FY2024 H1 filing, published **2024-08-14**, states that stricter withdrawal criteria had been set in **Q1**.

E088 prevents that retrospective statement from leaking backward into a public prospective evaluator.

## Two times

The evidence record stores:

- effective period: `2024-Q1`;
- public availability: `2024-08-14`.

The filing does not disclose the exact internal day on which the criteria became effective, so E088 stores a period rather than inventing a point timestamp.

## Public prospective authority

At a public cutoff of **2024-05-15**, the criteria evidence returns:

`REJECT_FUTURE_INFORMATION`

On **2024-08-14**, it becomes:

`ADMIT`

Internal operators may of course have known the criteria earlier. That is a different access scope.

## Consequence

`effective_period != publicly_available_on`

A public longitudinal model must use the second field for feature admission.

Promotion:

`public-prospective-evidence-uses-availability-time-not-retrospective-effective-period-v1`
