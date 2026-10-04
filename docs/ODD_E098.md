# ODD addendum — E098 real-case warning tournament

## Purpose

E097 adds a real recovery negative control: GVA TECH experiences one quarter of ARR decline plus churn deterioration and then recovers in Q4.

E098 reruns warning semantics on a tiny real-case mechanism suite.

## Cases

- **GVA transient stress** — one-quarter ARR down / churn up, followed by recovery; no structural escalation label.
- **BBD portfolio transition** — KPI signs conflict during active transition; no forced failure label.
- **Allied overseas deterioration** — deterioration-linked reporting-kernel break and later exit path; escalation required.
- **Jooto growth-viability failure** — persistent losses plus explicit failure to establish sustainable competitive advantage; escalation required.

## Tournament

A scalar rule:

`ARR down AND churn up => structural escalation`

false-positives on GVA and misses Allied + Jooto.

A typed mechanism rule escalates on:

- deterioration-linked reporting break; or
- persistent profitability failure + competitive-advantage failure.

It is exact on the four-case semantic regression suite.

## Authority

The exact fit is **not** production predictive accuracy and not a prevalence estimate. It is a semantic regression test ensuring that stronger mechanism evidence survives while the real recovery control does not become a false alarm.

Promotion:

`real-case-warning-escalation-requires-typed-mechanism-evidence-v1`
