from __future__ import annotations


def gva_tech_kpi_series() -> tuple[dict, ...]:
    return (
        {"quarter": "FY2025-Q2", "arr_jpy_millions": 796, "churn_pct": 0.50},
        {"quarter": "FY2025-Q3", "arr_jpy_millions": 764, "churn_pct": 0.95},
        {"quarter": "FY2025-Q4", "arr_jpy_millions": 830, "churn_pct": 0.83},
    )


def transitions() -> tuple[dict, ...]:
    rows = gva_tech_kpi_series()
    out = []
    for previous, current in zip(rows, rows[1:]):
        arr_delta = current["arr_jpy_millions"] - previous["arr_jpy_millions"]
        churn_delta = current["churn_pct"] - previous["churn_pct"]
        out.append(
            {
                "from": previous["quarter"],
                "to": current["quarter"],
                "arr_delta_jpy_millions": arr_delta,
                "arr_direction": "up" if arr_delta > 0 else "down" if arr_delta < 0 else "flat",
                "churn_delta_percentage_points": churn_delta,
                "churn_direction": "up" if churn_delta > 0 else "down" if churn_delta < 0 else "flat",
            }
        )
    return tuple(out)


def naive_one_quarter_failure_rule() -> dict:
    q3 = transitions()[0]
    triggered = q3["arr_direction"] == "down" and q3["churn_direction"] == "up"
    return {
        "triggered": triggered,
        "decision": "STRUCTURAL_FAILURE" if triggered else "NO_SIGNAL",
    }


def holdout_aware_rule() -> dict:
    q3, q4 = transitions()
    q3_bad = q3["arr_direction"] == "down" and q3["churn_direction"] == "up"
    q4_recovery = q4["arr_direction"] == "up" and q4["churn_direction"] == "down"
    return {
        "q3_stress_signal": q3_bad,
        "q4_recovery_signal": q4_recovery,
        "decision": "TRANSIENT_STRESS_NOT_STRUCTURAL_FAILURE" if q3_bad and q4_recovery else "UNRESOLVED",
    }


def transient_kpi_stress_report_payload() -> dict:
    series = gva_tech_kpi_series()
    rows = transitions()
    naive = naive_one_quarter_failure_rule()
    holdout = holdout_aware_rule()

    gates = {
        "q2_to_q3_arr_falls_by_32": rows[0]["arr_delta_jpy_millions"] == -32,
        "q2_to_q3_churn_worsens_by_0_45pp": round(rows[0]["churn_delta_percentage_points"], 2) == 0.45,
        "q3_to_q4_arr_recovers_by_66": rows[1]["arr_delta_jpy_millions"] == 66,
        "q3_to_q4_churn_improves_by_0_12pp": round(rows[1]["churn_delta_percentage_points"], 2) == -0.12,
        "naive_one_quarter_rule_false_positives": naive["decision"] == "STRUCTURAL_FAILURE",
        "holdout_reclassifies_as_transient_stress": holdout["decision"] == "TRANSIENT_STRESS_NOT_STRUCTURAL_FAILURE",
        "source_calls_q3_effect_temporary_and_q4_recovering": True,
    }

    return {
        "experiment": "E097",
        "question": (
            "Does one quarter of simultaneous ARR decline and churn deterioration "
            "certify structural SaaS failure, or can it be a transient segment-mix shock?"
        ),
        "source": {
            "provider": "GVA TECH Co., Ltd.",
            "document": "FY2025 full-year financial results presentation",
            "published_on": "2026-02-13",
            "business": "LegalTech SaaS / OLGA",
            "annotation": (
                "The company attributes Q3 churn deterioration to cancellations among "
                "non-main-target customers and states the temporary impact converged, "
                "with ARR and churn recovering in Q4."
            ),
        },
        "series": list(series),
        "transitions": list(rows),
        "naive_rule": naive,
        "holdout_aware_rule": holdout,
        "promotion_gate": gates,
        "promoted_negative_control_rule": (
            "one-quarter-arr-down-churn-up-does-not-certify-structural-saas-failure-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Negative-evidence warnings gain a real recovery control. A simultaneous "
            "ARR decline and churn spike is a stress signal, not sufficient structural-"
            "failure authority, unless persistence or other mechanism evidence survives "
            "a prospective holdout."
        ),
        "limitations": (
            "This is one recovery case and does not establish a universal persistence "
            "window. Management's temporary-shock explanation is retained as annotation."
        ),
    }
