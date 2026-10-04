from __future__ import annotations


def jooto_exit_value_state() -> dict:
    return {
        "standalone_general_service_growth_business": "TERMINATING",
        "general_service_end_date": "2027-07-31",
        "customer_base_value": "RETAINED_VALUE_ACKNOWLEDGED",
        "technology_value": "RETAINED_VALUE_ACKNOWLEDGED",
        "knowhow_value": "RETAINED_VALUE_ACKNOWLEDGED",
        "toyota_custom_tool": "CONTINUES",
        "employee_capability": "REDEPLOYED_INTERNALLY",
        "standalone_growth_viability": False,
        "residual_capability_value_zero": False,
    }


def naive_total_failure_model() -> dict:
    return {
        "service_exit": True,
        "assumed_customer_base_value": 0,
        "assumed_technology_value": 0,
        "assumed_knowhow_value": 0,
        "assumed_employee_reuse": False,
        "assumed_adjacent_product_continuity": False,
        "status": "CONTRADICTED_BY_PUBLIC_EXIT_PLAN",
    }


def residual_value_report_payload() -> dict:
    state = jooto_exit_value_state()
    naive = naive_total_failure_model()

    gates = {
        "general_service_is_terminating": (
            state["standalone_general_service_growth_business"] == "TERMINATING"
        ),
        "standalone_growth_viability_is_not_certified": (
            state["standalone_growth_viability"] is False
        ),
        "customer_technology_and_knowhow_value_are_retained": all(
            state[key] == "RETAINED_VALUE_ACKNOWLEDGED"
            for key in (
                "customer_base_value",
                "technology_value",
                "knowhow_value",
            )
        ),
        "adjacent_custom_tool_continues": (
            state["toyota_custom_tool"] == "CONTINUES"
        ),
        "employee_capability_is_redeployed": (
            state["employee_capability"] == "REDEPLOYED_INTERNALLY"
        ),
        "exit_does_not_imply_zero_residual_capability_value": (
            state["residual_capability_value_zero"] is False
        ),
        "naive_total_failure_model_is_rejected": (
            naive["status"] == "CONTRADICTED_BY_PUBLIC_EXIT_PLAN"
        ),
    }

    return {
        "experiment": "E095",
        "question": (
            "Does terminating a standalone SaaS growth business imply that its "
            "customer base, technology, know-how, adjacent implementations, and "
            "employee capabilities all have zero residual value?"
        ),
        "source": {
            "provider": "PR TIMES, Inc.",
            "service": "Jooto",
            "published_on": "2026-08-06",
            "annotation": (
                "The company says Jooto's customer base, technology and know-how "
                "retain important value; the Toyota custom work-management tool "
                "continues; and Jooto employees are generally to be redeployed "
                "to other internal businesses using their experience."
            ),
        },
        "exit_value_state": state,
        "naive_total_failure_model": naive,
        "promotion_gate": gates,
        "promoted_residual_value_rule": (
            "service-business-exit-does-not-imply-zero-residual-capability-value-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Standalone business viability and residual capability value are "
            "separate state dimensions. Strategic exit can terminate one growth "
            "vehicle while preserving/redeploying customer knowledge, technology, "
            "adjacent implementations, and human capability."
        ),
        "limitations": (
            "The source establishes qualitative retained value and continuity, "
            "not a monetary valuation of those residual assets or capabilities."
        ),
    }
