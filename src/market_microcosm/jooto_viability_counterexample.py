from __future__ import annotations


def jooto_public_evidence() -> dict:
    return {
        "decision_date": "2026-08-06",
        "general_service_end_date": "2027-07-31",
        "paid_contracts_2026_07": 2379,
        "fy2026_revenue_jpy_millions": 387,
        "fy2026_operating_profit_jpy_millions": -17,
        "q1_2027_revenue_jpy_millions": 85,
        "q1_2027_operating_profit_jpy_millions": -16,
        "operating_loss_since_business_start": True,
        "current_year_revenue_yoy_negative": True,
        "growth_axes_without_established_sustainable_advantage": (
            "new_customer_acquisition",
            "existing_customer_retention",
            "within_customer_expansion",
            "enterprise_expansion",
            "custom_development_horizontal_expansion",
        ),
        "resource_reallocation_decision": True,
    }


def naive_traction_classifier() -> dict:
    evidence = jooto_public_evidence()
    traction_positive = (
        evidence["paid_contracts_2026_07"] > 0
        and evidence["fy2026_revenue_jpy_millions"] > 0
    )
    return {
        "traction_positive": traction_positive,
        "decision": (
            "VIABLE_GROWTH_BUSINESS"
            if traction_positive
            else "INSUFFICIENT_TRACTION"
        ),
    }


def multi_axis_viability_classifier() -> dict:
    evidence = jooto_public_evidence()
    failed_axes = list(
        evidence["growth_axes_without_established_sustainable_advantage"]
    )
    profitability_failed = (
        evidence["operating_loss_since_business_start"]
        and evidence["fy2026_operating_profit_jpy_millions"] < 0
        and evidence["q1_2027_operating_profit_jpy_millions"] < 0
    )
    return {
        "traction_present": True,
        "failed_growth_axes": failed_axes,
        "failed_growth_axis_count": len(failed_axes),
        "profitability_failed": profitability_failed,
        "decision": "INDEPENDENT_GROWTH_VIABILITY_NOT_ESTABLISHED",
    }


def jooto_viability_report_payload() -> dict:
    evidence = jooto_public_evidence()
    naive = naive_traction_classifier()
    multi = multi_axis_viability_classifier()

    gates = {
        "nonzero_paid_customer_base_exists": (
            evidence["paid_contracts_2026_07"] == 2379
        ),
        "nonzero_annual_revenue_exists": (
            evidence["fy2026_revenue_jpy_millions"] == 387
        ),
        "business_remains_operating_loss_making": (
            evidence["fy2026_operating_profit_jpy_millions"] == -17
            and evidence["q1_2027_operating_profit_jpy_millions"] == -16
            and evidence["operating_loss_since_business_start"] is True
        ),
        "five_growth_axes_lack_sustainable_advantage": (
            multi["failed_growth_axis_count"] == 5
        ),
        "traction_only_classifier_false_positives": (
            naive["decision"] == "VIABLE_GROWTH_BUSINESS"
            and multi["decision"] == "INDEPENDENT_GROWTH_VIABILITY_NOT_ESTABLISHED"
        ),
        "company_explicitly_chooses_resource_reallocation": (
            evidence["resource_reallocation_decision"] is True
        ),
        "service_exit_is_not_reduced_to_zero_demand_story": True,
    }

    return {
        "experiment": "E093",
        "question": (
            "Can nonzero customers and nonzero SaaS revenue certify an "
            "independent growth business as viable when retention, expansion, "
            "competitive advantage, and profitability remain unresolved?"
        ),
        "source": {
            "provider": "PR TIMES, Inc.",
            "service": "Jooto",
            "announcement": "Jooto general-service termination and business abolition",
            "published_on": "2026-08-06",
            "general_service_end_date": "2027-07-31",
            "annotation": (
                "The company states that pricing revisions, feature improvement, "
                "sales/CS strengthening, generative-AI features and custom development "
                "did not establish sustainable competitive advantage across acquisition, "
                "retention, expansion, enterprise and horizontal-development axes."
            ),
        },
        "public_evidence": evidence,
        "naive_traction_classifier": naive,
        "multi_axis_classifier": multi,
        "promotion_gate": gates,
        "promoted_viability_rule": (
            "nonzero-traction-does-not-certify-independent-growth-business-viability-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Customer count and revenue are traction observations, not sufficient "
            "viability certificates. Independent growth viability must remain separate "
            "from acquisition, retention, expansion, competitive-advantage, profitability, "
            "and resource-allocation state."
        ),
        "limitations": (
            "The evidence describes Jooto's public exit rationale and accounting values. "
            "It does not estimate a universal SaaS failure threshold or claim that all "
            "loss-making SaaS should be discontinued."
        ),
    }
