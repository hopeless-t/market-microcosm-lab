from __future__ import annotations

from dataclasses import asdict, dataclass


WITHDRAWN_KPIS = (
    "stock_revenue",
    "stock_revenue_ratio",
    "arr",
    "churn_rate",
    "customer_count",
    "customer_industry_mix",
    "customer_region_mix",
    "average_unit_price",
)


@dataclass(frozen=True)
class DisclosureEvent:
    event_id: str
    published_on: str
    business: str
    event_type: str
    trigger: str
    withdrawn_kpis: tuple[str, ...]
    replacement_disclosure: tuple[str, ...]
    old_series_authority: str


def allied_overseas_saas_withdrawal() -> DisclosureEvent:
    return DisclosureEvent(
        event_id="allied-overseas-saas-fy2023-kpi-withdrawal",
        published_on="2024-02-14",
        business="Allied Architects overseas SaaS / Creadits",
        event_type="KPI_WITHDRAWN_DUE_TO_DETERIORATION",
        trigger=(
            "overseas business deterioration; many Q4 cancellations; "
            "business no longer described as highly recurring"
        ),
        withdrawn_kpis=WITHDRAWN_KPIS,
        replacement_disclosure=("revenue", "operating_profit"),
        old_series_authority="REVOKED_AFTER_WITHDRAWAL",
    )


def naive_missing_handler() -> dict:
    return {
        "missing_value_policy": "drop_or_forward_fill",
        "withdrawal_event_retained": False,
        "post_withdrawal_trend_authority": "UNSOUND",
        "failure_mode": (
            "state-dependent reporting change is erased and the old KPI "
            "series can be mistaken for ordinary missing-at-random data"
        ),
    }


def withdrawal_aware_handler() -> dict:
    event = allied_overseas_saas_withdrawal()
    return {
        "missing_value_policy": "retain_disclosure_event",
        "withdrawal_event_retained": True,
        "series_status": "TERMINATED_BY_REPORTING_POLICY_CHANGE",
        "post_withdrawal_numeric_imputation_permitted": False,
        "forward_fill_permitted": False,
        "cross_withdrawal_trend_extension_permitted": False,
        "withdrawal_event_can_be_used_as_categorical_evidence": True,
        "hidden_kpi_value_inference_permitted": False,
        "event": asdict(event),
    }


def informative_missingness_report_payload() -> dict:
    event = allied_overseas_saas_withdrawal()
    naive = naive_missing_handler()
    aware = withdrawal_aware_handler()

    gates = {
        "withdrawal_is_explicitly_linked_to_deterioration": (
            "deterioration" in event.trigger
        ),
        "multiple_operating_kpis_are_withdrawn": len(event.withdrawn_kpis) == 8,
        "arr_and_churn_are_both_withdrawn": (
            "arr" in event.withdrawn_kpis
            and "churn_rate" in event.withdrawn_kpis
        ),
        "replacement_disclosure_is_narrower": (
            event.replacement_disclosure == ("revenue", "operating_profit")
        ),
        "naive_missing_handler_erases_the_event": (
            naive["withdrawal_event_retained"] is False
        ),
        "aware_handler_forbids_forward_fill": (
            aware["forward_fill_permitted"] is False
        ),
        "aware_handler_forbids_hidden_value_imputation": (
            aware["hidden_kpi_value_inference_permitted"] is False
        ),
        "old_series_authority_is_revoked": (
            event.old_series_authority == "REVOKED_AFTER_WITHDRAWAL"
        ),
    }

    return {
        "experiment": "E079",
        "question": (
            "When KPI disclosure stops because the business deteriorated, "
            "should the missing values be treated as ordinary missing data?"
        ),
        "source": {
            "provider": "Allied Architects, Inc.",
            "document": "FY2023 full-year financial results presentation",
            "published_on": "2024-02-14",
            "url": "https://www2.jpx.co.jp/disc/60810/140120240214537247.pdf",
            "source_pages": [3, 51],
            "evidence_note": (
                "The presentation states that KPI disclosure is being changed "
                "because overseas performance deteriorated; after many Q4 "
                "cancellations it stops disclosing stock revenue, ARR, churn, "
                "customer counts/mix and average unit price, and says revenue "
                "and operating profit will be disclosed until a new KPI set is ready."
            ),
        },
        "withdrawal_event": asdict(event),
        "naive_handler": naive,
        "withdrawal_aware_handler": aware,
        "missingness_class": "INFORMATIVE_STATE_DEPENDENT_REPORTING",
        "formal_mnar_claim": False,
        "promotion_gate": gates,
        "promoted_missingness_rule": (
            "kpi-withdrawal-is-first-class-informative-observation-event-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "The observation process becomes endogenous. KPI withdrawal caused "
            "by deterioration is retained as evidence about reporting state, "
            "while the hidden KPI values remain unknown. Old KPI series cannot "
            "be forward-filled or extrapolated across the disclosure-policy break."
        ),
        "limitations": (
            "The experiment uses the company's stated reason for disclosure "
            "withdrawal as an observed reporting event. It does not claim a "
            "formal statistical MNAR mechanism or infer the undisclosed KPI values."
        ),
    }
