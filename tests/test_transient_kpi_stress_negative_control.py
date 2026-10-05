from market_microcosm.transient_kpi_stress_negative_control import (
    holdout_aware_rule,
    transient_kpi_stress_report_payload,
    transitions,
)


def test_q3_bad_signs_recover_in_q4() -> None:
    q3, q4 = transitions()
    assert q3["arr_delta_jpy_millions"] == -32
    assert round(q3["churn_delta_percentage_points"], 2) == 0.45
    assert q4["arr_delta_jpy_millions"] == 66
    assert round(q4["churn_delta_percentage_points"], 2) == -0.12
    assert holdout_aware_rule()["decision"] == "TRANSIENT_STRESS_NOT_STRUCTURAL_FAILURE"


def test_e097_promotion_contract() -> None:
    payload = transient_kpi_stress_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_negative_control_rule"] == (
        "one-quarter-arr-down-churn-up-does-not-certify-structural-saas-failure-v1"
    )
