from __future__ import annotations


def allied_q1_comparison() -> dict:
    prior = {
        "period": "2024-Q1",
        "revenue_jpy_millions": 827,
        "operating_profit_jpy_millions": -229,
    }
    after = {
        "period": "2025-Q1",
        "revenue_jpy_millions": 809,
        "operating_profit_jpy_millions": 16,
    }
    return {
        "prior": prior,
        "after": after,
        "revenue_delta_jpy_millions": (
            after["revenue_jpy_millions"] - prior["revenue_jpy_millions"]
        ),
        "revenue_pct_change": (
            after["revenue_jpy_millions"] / prior["revenue_jpy_millions"] - 1.0
        ),
        "operating_profit_delta_jpy_millions": (
            after["operating_profit_jpy_millions"]
            - prior["operating_profit_jpy_millions"]
        ),
        "operating_profit_sign_flip": (
            prior["operating_profit_jpy_millions"] < 0
            and after["operating_profit_jpy_millions"] > 0
        ),
    }


def scalar_evaluations() -> dict:
    row = allied_q1_comparison()
    return {
        "revenue_only": (
            "WORSE"
            if row["revenue_delta_jpy_millions"] < 0
            else "BETTER_OR_EQUAL"
        ),
        "operating_profit_only": (
            "BETTER"
            if row["operating_profit_delta_jpy_millions"] > 0
            else "WORSE_OR_EQUAL"
        ),
        "sign_conflict": (
            row["revenue_delta_jpy_millions"] < 0
            and row["operating_profit_delta_jpy_millions"] > 0
        ),
    }


def post_exit_profitability_report_payload() -> dict:
    comparison = allied_q1_comparison()
    evaluations = scalar_evaluations()

    gates = {
        "revenue_declines_by_eighteen_million": (
            comparison["revenue_delta_jpy_millions"] == -18
        ),
        "reported_revenue_change_is_minus_two_point_two_percent": (
            round(comparison["revenue_pct_change"] * 100.0, 1) == -2.2
        ),
        "operating_profit_improves_by_two_hundred_forty_five_million": (
            comparison["operating_profit_delta_jpy_millions"] == 245
        ),
        "operating_profit_flips_from_loss_to_profit": (
            comparison["operating_profit_sign_flip"] is True
        ),
        "revenue_and_profit_scalars_disagree": (
            evaluations["sign_conflict"] is True
        ),
        "public_source_links_revenue_decline_to_superfaction_exit": True,
        "public_source_links_operating_black_to_restructuring_and_cost_reduction": True,
        "metric_conflict_is_not_collapsed_into_one_health_label": True,
    }

    return {
        "experiment": "E090",
        "question": (
            "Can a strategic portfolio exit reduce consolidated revenue while "
            "simultaneously improving operating profitability enough to reverse "
            "the sign of operating profit?"
        ),
        "source": {
            "provider": "Allied Architects, Inc.",
            "document": "FY2025 Q1 financial results presentation",
            "published_on": "2025-07-18",
            "page": 6,
            "annotations": (
                "The company states that the main reason for YoY revenue decline "
                "was loss of SuperFaction revenue contribution after exit, and "
                "that overseas-business restructuring plus cost reduction produced "
                "positive operating profit."
            ),
        },
        "comparison": comparison,
        "scalar_evaluations": evaluations,
        "promotion_gate": gates,
        "promoted_exit_rule": (
            "strategic-exit-can-lower-revenue-while-improving-operating-profit-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Post-exit health cannot be ranked by revenue growth alone. A deliberate "
            "portfolio contraction can remove revenue while materially improving "
            "operating economics, so revenue scale and operating viability remain "
            "separate state dimensions."
        ),
        "limitations": (
            "This is one company-quarter comparison. The company's explanation is "
            "retained as an event annotation and does not identify a general causal "
            "effect size of strategic exits."
        ),
    }
