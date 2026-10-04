from market_microcosm.robust_prior_acquisition import (
    minimax_order,
    robust_prior_set_report_payload,
)


def test_minimax_order():
    x = minimax_order()["selected"]
    assert x["order"] == [
        "signed-strategy-gap-attestation",
        "finance-pack",
        "gtm-pack",
    ]
    assert round(x["worst_case_expected_cost"], 3) == 11.315
    assert round(x["worst_case_regret"], 4) == 2.2925


def test_e071_promotion_contract():
    x = robust_prior_set_report_payload()
    assert all(x["promotion_gate"].values())
    assert x["promoted_robust_rule"] == (
        "uncertain-prior-sequential-acquisition-uses-minimax-order-v1"
    )
