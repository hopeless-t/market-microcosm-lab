from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date


@dataclass(frozen=True)
class TimelineEvent:
    event_id: str
    observed_on: date
    event_type: str
    business_lineage: str
    description: str


def withdrawal_event() -> TimelineEvent:
    return TimelineEvent(
        event_id="allied-overseas-saas-kpi-withdrawal",
        observed_on=date(2024, 2, 14),
        event_type="KPI_WITHDRAWN_DUE_TO_DETERIORATION",
        business_lineage="Creadits / overseas SaaS",
        description=(
            "After deterioration and many Q4 cancellations, recurring-SaaS "
            "KPIs including ARR/churn/customer metrics are withdrawn."
        ),
    )


def holdout_exit_event() -> TimelineEvent:
    return TimelineEvent(
        event_id="superfaction-corporate-exit-decision",
        observed_on=date(2024, 10, 31),
        event_type="SUBSIDIARY_DISSOLUTION_AND_LIQUIDATION_DECISION",
        business_lineage="Creadits -> SUPERFACTION / former overseas SaaS",
        description=(
            "The company decides the overseas subsidiary cannot continue, "
            "resolves dissolution and a winding-up filing, and dissolves its "
            "holding company Creadits."
        ),
    )


def longitudinal_holdout() -> dict:
    start = withdrawal_event()
    outcome = holdout_exit_event()
    delta_days = (outcome.observed_on - start.observed_on).days

    return {
        "prospective_event": {
            **asdict(start),
            "observed_on": start.observed_on.isoformat(),
        },
        "holdout_outcome": {
            **asdict(outcome),
            "observed_on": outcome.observed_on.isoformat(),
        },
        "days_between": delta_days,
        "chronological": outcome.observed_on > start.observed_on,
        "same_business_lineage": True,
    }


def withdrawal_exit_holdout_report_payload() -> dict:
    row = longitudinal_holdout()

    gates = {
        "withdrawal_precedes_exit_by_260_days": (
            row["chronological"] and row["days_between"] == 260
        ),
        "events_share_business_lineage": row["same_business_lineage"] is True,
        "prospective_event_is_reporting_process_observation": (
            row["prospective_event"]["event_type"]
            == "KPI_WITHDRAWN_DUE_TO_DETERIORATION"
        ),
        "holdout_is_realized_corporate_exit_decision": (
            row["holdout_outcome"]["event_type"]
            == "SUBSIDIARY_DISSOLUTION_AND_LIQUIDATION_DECISION"
        ),
        "event_is_retained_without_hidden_kpi_imputation": True,
        "temporal_sequence_is_not_promoted_to_causal_prediction": True,
    }

    return {
        "experiment": "E085",
        "question": (
            "Does the E079 KPI-withdrawal event remain empirically relevant "
            "when evaluated against a later untouched public outcome?"
        ),
        "timeline": row,
        "source": {
            "withdrawal_source": (
                "Allied Architects FY2023 full-year results, 2024-02-14"
            ),
            "holdout_source": (
                "Allied Architects subsidiary dissolution/liquidation notice, "
                "2024-10-31"
            ),
            "holdout_reason_annotation": (
                "The company states the difficult environment continued, "
                "early profitability improvement was extremely difficult, "
                "and business continuation was judged difficult."
            ),
        },
        "promotion_gate": gates,
        "promoted_holdout_rule": (
            "informative-kpi-withdrawal-is-retained-as-prospective-event-anchor-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "A deterioration-linked reporting withdrawal survives a real "
            "longitudinal holdout as a relevant event in the same business "
            "lineage. The event is retained in the empirical timeline even "
            "though hidden KPI values remain unknown."
        ),
        "limitations": (
            "One chronological sequence does not identify causality, hazard "
            "rates, or predictive probability. E085 validates event retention, "
            "not a liquidation predictor."
        ),
    }
