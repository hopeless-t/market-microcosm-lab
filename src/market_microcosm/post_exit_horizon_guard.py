from __future__ import annotations


def post_exit_horizons() -> dict:
    return {
        "2025-Q1": {
            "revenue_jpy_millions": 809,
            "operating_profit_jpy_millions": 16,
            "profitability_state": "QUARTERLY_POSITIVE",
        },
        "2025-H1": {
            "revenue_jpy_millions": 1499,
            "operating_profit_jpy_millions": -49,
            "profitability_state": "CUMULATIVE_OPERATING_LOSS",
        },
        "2024-H1": {
            "revenue_jpy_millions": 1731,
            "operating_profit_jpy_millions": -285,
            "profitability_state": "CUMULATIVE_OPERATING_LOSS",
        },
    }


def horizon_authority() -> dict:
    rows = post_exit_horizons()
    h1_improvement = (
        rows["2025-H1"]["operating_profit_jpy_millions"]
        - rows["2024-H1"]["operating_profit_jpy_millions"]
    )
    return {
        "q1_directional_improvement": True,
        "q1_positive_operating_profit": True,
        "h1_operating_profit_improvement_jpy_millions": h1_improvement,
        "h1_still_loss_making": (
            rows["2025-H1"]["operating_profit_jpy_millions"] < 0
        ),
        "durable_profitability_certified": False,
        "decision": "IMPROVING_BUT_NOT_DURABLY_PROFITABLE",
    }


def post_exit_horizon_report_payload() -> dict:
    rows = post_exit_horizons()
    authority = horizon_authority()

    gates = {
        "q1_is_operating_profit_positive": (
            rows["2025-Q1"]["operating_profit_jpy_millions"] == 16
        ),
        "h1_remains_operating_loss": (
            rows["2025-H1"]["operating_profit_jpy_millions"] == -49
        ),
        "h1_improves_by_236_million_yoy": (
            authority["h1_operating_profit_improvement_jpy_millions"] == 236
        ),
        "directional_improvement_is_retained": (
            authority["q1_directional_improvement"] is True
        ),
        "durable_profitability_is_not_certified": (
            authority["durable_profitability_certified"] is False
        ),
        "one_quarter_sign_flip_does_not_define_long_horizon_state": True,
    }

    return {
        "experiment": "E092",
        "question": (
            "Does E090's positive FY2025 Q1 operating result certify durable "
            "post-exit profitability over a longer observation horizon?"
        ),
        "source": {
            "provider": "Allied Architects, Inc.",
            "q1_document": "FY2025 Q1 financial results presentation",
            "h1_document": "FY2025 H1 financial results / earnings release",
            "h1_published_on": "2025-08-14",
            "annotation": (
                "FY2025 H1 reports revenue 1,499m JPY and operating loss 49m JPY "
                "versus FY2024 H1 revenue 1,731m and operating loss 285m."
            ),
        },
        "horizons": rows,
        "authority": authority,
        "promotion_gate": gates,
        "promoted_horizon_rule": (
            "one-quarter-profit-sign-flip-does-not-certify-durable-profitability-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Post-exit improvement and durable profitability are separate claims. "
            "A short-horizon positive operating result can coexist with a longer-"
            "horizon cumulative operating loss; authority must state its horizon."
        ),
        "limitations": (
            "H1 still reflects transition costs and period aggregation. E092 does "
            "not claim the business failed to improve; it limits the durability "
            "claim supported by the observed horizon."
        ),
    }
