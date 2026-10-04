from __future__ import annotations


def bbd_pruning_kpi_series() -> tuple[dict, ...]:
    return (
        {
            "period": "FY2023-Q1",
            "arr_jpy_millions": 1358,
            "churn_rate_pct": 1.12,
            "contracts": 3426,
            "arpa_jpy": 395925,
        },
        {
            "period": "FY2023-Q2",
            "arr_jpy_millions": 1443,
            "churn_rate_pct": 1.53,
            "contracts": 3475,
            "arpa_jpy": 415535,
        },
        {
            "period": "FY2023-Q3",
            "arr_jpy_millions": 1541,
            "churn_rate_pct": 1.53,
            "contracts": 3557,
            "arpa_jpy": 433445,
        },
        {
            "period": "FY2023-Q4",
            "arr_jpy_millions": 1593,
            "churn_rate_pct": 1.15,
            "contracts": 3641,
            "arpa_jpy": 437545,
        },
        {
            "period": "FY2024-Q1",
            "arr_jpy_millions": 1591,
            "churn_rate_pct": 2.13,
            "contracts": 3608,
            "arpa_jpy": 441035,
        },
        {
            "period": "FY2024-Q2",
            "arr_jpy_millions": 1588,
            "churn_rate_pct": 1.74,
            "contracts": 3549,
            "arpa_jpy": 447722,
        },
        {
            "period": "FY2024-Q3",
            "arr_jpy_millions": 1607,
            "churn_rate_pct": 2.33,
            "contracts": 3416,
            "arpa_jpy": 466303,
        },
    )


def endpoint_change() -> dict:
    series = bbd_pruning_kpi_series()
    start = next(row for row in series if row["period"] == "FY2023-Q4")
    end = next(row for row in series if row["period"] == "FY2024-Q3")

    return {
        "start": start,
        "end": end,
        "arr_change_pct": (
            end["arr_jpy_millions"] / start["arr_jpy_millions"] - 1.0
        ) * 100.0,
        "churn_change_percentage_points": (
            end["churn_rate_pct"] - start["churn_rate_pct"]
        ),
        "churn_relative_change_pct": (
            end["churn_rate_pct"] / start["churn_rate_pct"] - 1.0
        ) * 100.0,
        "contracts_change_pct": (
            end["contracts"] / start["contracts"] - 1.0
        ) * 100.0,
        "arpa_change_pct": (
            end["arpa_jpy"] / start["arpa_jpy"] - 1.0
        ) * 100.0,
    }


def churn_semantics_report_payload() -> dict:
    change = endpoint_change()

    sign_counterexample = {
        "churn_increased": (
            change["churn_change_percentage_points"] > 0
        ),
        "contracts_decreased": change["contracts_change_pct"] < 0,
        "arr_increased": change["arr_change_pct"] > 0,
        "arpa_increased": change["arpa_change_pct"] > 0,
    }

    gates = {
        "observed_churn_more_than_doubled_relative": (
            change["churn_relative_change_pct"] > 100.0
        ),
        "arr_did_not_collapse": change["arr_change_pct"] > 0,
        "arpa_increased_materially": change["arpa_change_pct"] > 5.0,
        "contract_count_declined": change["contracts_change_pct"] < -5.0,
        "sign_counterexample_complete": all(sign_counterexample.values()),
        "b2b_mrr_churn_not_equated_with_e010_user_churn": True,
        "churn_cause_must_be_typed": True,
    }

    return {
        "experiment": "E030",
        "question": (
            "Can a higher reported SaaS churn rate coexist with higher ARR "
            "and ARPA when the churn partly reflects deliberate portfolio "
            "pruning and plan migration?"
        ),
        "source_id": "bbd-portfolio-pruning-2024",
        "metric_definition": (
            "BBD defines Churn Rate as quarterly three-month average of "
            "monthly Churn MRR divided by prior month-end MRR."
        ),
        "series": list(bbd_pruning_kpi_series()),
        "endpoint_change": change,
        "sign_counterexample": sign_counterexample,
        "promotion_gate": gates,
        "promoted_churn_rule": (
            "churn-must-be-layer-and-cause-typed-v1"
            if all(gates.values())
            else None
        ),
        "model_update": {
            "forbid_generic_churn_transfer": (
                "Do not map B2B MRR churn directly into E010 baseline user churn."
            ),
            "future_churn_components": (
                "distress_or_demand_churn",
                "intentional_portfolio_pruning",
                "plan_or_segment_migration",
            ),
            "required_layer_identity": (
                "end_user",
                "account_or_logo",
                "mrr",
                "content_or_supplier",
            ),
        },
        "limitations": (
            "The endpoint comparison is descriptive. BBD explicitly attributes "
            "part of the churn increase to unprofitable-service withdrawal and "
            "low-price-plan migration, but E030 does not estimate the causal "
            "share of each component."
        ),
    }
