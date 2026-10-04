from market_microcosm.joint_extended_robustness import (
    extended_scenario_search,
    joint_extended_robustness_report_payload,
)


def test_e071_order_survives_added_joint_scenario():
    x = extended_scenario_search()["selected"]
    assert x["order"] == [
        "signed-strategy-gap-attestation",
        "finance-pack",
        "gtm-pack",
    ]
    assert round(x["worst_case_expected_cost"], 3) == 11.315
    assert round(x["worst_case_regret"], 2) == 2.70


def test_e073_promotion_contract():
    x = joint_extended_robustness_report_payload()
    assert x["e071_order_authority"] == "RETAINED"
    assert x["e071_regret_bound_authority"] == "REISSUED"
    assert all(x["promotion_gate"].values())
