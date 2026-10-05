from __future__ import annotations


REQUIRED_WARNING_AXES = (
    "cash_collection_gap",
    "fully_loaded_delivery_margin",
    "market_headroom",
    "downstream_funnel_success",
    "strategic_exit_value_gap",
)


def public_q3_evidence_mapping() -> dict[str, dict]:
    return {
        "arr": {
            "available": True,
            "value": 1688.0,
            "unit": "JPY millions",
            "maps_to_warning_axis": None,
        },
        "churn": {
            "available": True,
            "value": 2.16,
            "unit": "percent",
            "maps_to_warning_axis": None,
        },
        "contract_count": {
            "available": True,
            "value": 3304,
            "unit": "accounts",
            "maps_to_warning_axis": None,
        },
        "arpa": {
            "available": True,
            "value": 511_090,
            "unit": "JPY/account/year",
            "maps_to_warning_axis": None,
        },
        "cash_collection_gap": {
            "available": False,
            "value": None,
            "unit": None,
            "maps_to_warning_axis": "cash_collection_gap",
        },
        "fully_loaded_delivery_margin": {
            "available": False,
            "value": None,
            "unit": None,
            "maps_to_warning_axis": "fully_loaded_delivery_margin",
        },
        "market_headroom": {
            "available": False,
            "value": None,
            "unit": None,
            "maps_to_warning_axis": "market_headroom",
        },
        "downstream_funnel_success": {
            "available": False,
            "value": None,
            "unit": None,
            "maps_to_warning_axis": "downstream_funnel_success",
        },
        "strategic_exit_value_gap": {
            "available": False,
            "value": None,
            "unit": None,
            "maps_to_warning_axis": "strategic_exit_value_gap",
        },
    }


def warning_feature_coverage() -> dict:
    mapping = public_q3_evidence_mapping()
    covered = []
    missing = []

    for axis in REQUIRED_WARNING_AXES:
        item = mapping[axis]
        if item["available"]:
            covered.append(axis)
        else:
            missing.append(axis)

    return {
        "required_axes": list(REQUIRED_WARNING_AXES),
        "covered_axes": covered,
        "missing_axes": missing,
        "coverage_fraction": len(covered) / len(REQUIRED_WARNING_AXES),
        "complete": len(missing) == 0,
    }


def prospective_warning_decision() -> dict:
    coverage = warning_feature_coverage()

    if coverage["complete"]:
        status = "EVALUABLE"
        decision = "RUN_WARNING"
    else:
        status = "ABSTAIN"
        decision = "INSUFFICIENT_PUBLIC_EVIDENCE"

    return {
        "status": status,
        "decision": decision,
        "feature_coverage": coverage,
        "imputation_permitted": False,
    }


def public_evidence_sufficiency_report_payload() -> dict:
    coverage = warning_feature_coverage()
    decision = prospective_warning_decision()

    gates = {
        "all_five_structural_warning_axes_are_declared": (
            len(coverage["required_axes"]) == 5
        ),
        "public_q3_kpis_do_not_directly_cover_structural_axes": (
            coverage["covered_axes"] == []
        ),
        "all_structural_axes_are_explicitly_missing": (
            coverage["missing_axes"] == list(REQUIRED_WARNING_AXES)
        ),
        "coverage_fraction_is_zero": (
            coverage["coverage_fraction"] == 0.0
        ),
        "prospective_warning_abstains": (
            decision["status"] == "ABSTAIN"
            and decision["decision"] == "INSUFFICIENT_PUBLIC_EVIDENCE"
        ),
        "missing_axes_are_not_imputed": (
            decision["imputation_permitted"] is False
        ),
    }

    return {
        "experiment": "E065",
        "question": (
            "At the public FY2025 Q3 decision cutoff, is the admitted BBD "
            "evidence sufficient to evaluate the five-axis E035/E036-style "
            "structural early-warning rule without inventing hidden state?"
        ),
        "source_context": {
            "provider": "BBD Initiative Inc.",
            "decision_cutoff": "2025-08-14",
            "public_q3_metrics": {
                "arr_jpy_millions": 1688.0,
                "churn_rate_pct": 2.16,
                "contract_count": 3304,
                "arpa_jpy": 511_090,
            },
            "note": (
                "These public KPIs are observations but are not direct "
                "measurements of the five structural warning axes."
            ),
        },
        "mapping": public_q3_evidence_mapping(),
        "coverage": coverage,
        "prospective_warning": decision,
        "promotion_gate": gates,
        "promoted_sufficiency_rule": (
            "structural-warning-must-abstain-when-public-feature-contract-is-incomplete-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "A real-company warning evaluation must satisfy its feature "
            "contract from admitted evidence. ARR, churn, contracts, and ARPA "
            "cannot be silently transformed into cash timing, fully loaded "
            "margin, market headroom, downstream success, or exit-value gap. "
            "Missing structural axes produce ABSTAIN rather than imputation."
        ),
        "limitations": (
            "The public IR set is intentionally narrower than internal company "
            "data. E065 says the public dataset cannot evaluate this warning "
            "contract; it does not say the company lacked the underlying state."
        ),
    }
