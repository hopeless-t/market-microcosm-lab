# ODD addendum — E079 informative KPI withdrawal

## Purpose

E078 re-anchors the lab in Allied Architects public SaaS evidence.

E079 attacks a common longitudinal-data assumption: when a KPI disappears from later reports, treating it as ordinary missing data can erase a state-dependent change in the reporting process.

## Public witness

Allied Architects' FY2023 full-year presentation states that KPI disclosure is being changed **because overseas performance deteriorated**.

The overseas SaaS section reports many Q4 cancellations and says the business can no longer be described as highly recurring. The company then stops disclosing:

- stock revenue;
- stock revenue ratio;
- ARR;
- churn rate;
- customer count;
- customer industry mix;
- customer region mix;
- average unit price.

Until the path to renewed growth is rebuilt, the presentation says only revenue and operating profit will be disclosed, with a new KPI set to be introduced later.

## Observation-model consequence

This is not represented as a blank cell.

The canonical event is:

`KPI_WITHDRAWN_DUE_TO_DETERIORATION`

The event is admissible categorical evidence about the reporting process, but it does **not** reveal the hidden KPI values.

After the withdrawal event:

- forward fill is forbidden;
- numeric imputation is not authorized;
- the old KPI trend cannot be extrapolated through the reporting-policy break;
- old-series authority is `REVOKED_AFTER_WITHDRAWAL`;
- downstream models may retain the disclosure-withdrawal event itself.

## Missingness semantics

E079 calls this **informative state-dependent reporting**.

It deliberately does not claim a formal statistical MNAR mechanism, because the public evidence identifies the reporting-policy change and its stated deterioration context, not the full probability law governing missing values.

## Promotion rule

`kpi-withdrawal-is-first-class-informative-observation-event-v1`

## Limitation

The company's explanation is treated as a reporting-process observation, not an independently identified causal estimate of the undisclosed KPI values.
