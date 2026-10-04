from market_microcosm.cross_company_sign_replication import (
    allied_transitions,
    cross_company_sign_replication_report_payload,
    q3_q4_product_decomposition,
)


def test_allied_q3_q4_churn_up_arr_up():
    x = allied_transitions()[-1]
    assert x["arr_delta_jpy_millions"] == 70
    assert x["arr_direction"] == "up"
    assert round(x["churn_delta_percentage_points"], 1) == 1.5
    assert x["churn_direction"] == "up"


def test_product_decomposition_reconciles():
    x = q3_q4_product_decomposition()
    assert x["components_jpy_millions"] == {
        "letro": 65,
        "letro_studio": 16,
        "monipla_fan_blog": -11,
    }
    assert x["component_sum"] == 70
    assert x["reported_total_delta"] == 70
    assert x["reconciles"] is True


def test_e078_promotion_contract():
    x = cross_company_sign_replication_report_payload()
    assert all(x["promotion_gate"].values())
    assert x["promoted_replication_rule"] == (
        "churn-arr-sign-counterexample-replicates-cross-company-v1"
    )
