# ODD addendum — E082 KPI-withdrawal reason typing

## Purpose

E079 correctly treats Allied Architects' overseas-SaaS KPI withdrawal as informative because the company explicitly connects the reporting change to deterioration and many Q4 cancellations.

E082 attacks the dangerous generalization:

`KPI withdrawn => business deteriorated`

## Counterexample

Two records can both have `withdrawn = true` while carrying different semantics:

- `DUE_TO_DETERIORATION` — the Allied public-disclosure anchor;
- `DUE_TO_METRIC_REDESIGN` — a synthetic non-deterioration case consistent with JPX guidance that KPI changes/withdrawals can accompany business-plan progress or revision when reasons are disclosed.

A scalar `withdrawn` classifier labels both as deterioration and therefore false-positives on the redesign case.

The typed rule requires:

- withdrawal occurred;
- reason type is `DUE_TO_DETERIORATION`;
- admitted deterioration evidence is present;
- source authority is retained.

## Consequence

Reporting-process events need semantic reason types just like churn and exit events do elsewhere in the lab.

Promotion:

`kpi-withdrawal-requires-reason-type-and-source-authority-v1`

## Limitation

The redesign record is a synthetic counterexample motivated by JPX disclosure guidance, not a claim about Allied Architects.
