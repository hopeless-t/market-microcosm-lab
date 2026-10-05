from market_microcosm.dependence_ambiguity_acquisition import (
    dependence_ambiguity_report_payload,
    dependence_ambiguity_search,
)


def test_nested_witness_makes_frechet_bound_tight():
    x = dependence_ambiguity_search()
    assert all(row["bound_is_tight"] for row in x["rows"])
    assert x["nested_witness_marginals"] == {
        "cash_collection_gap": 0.05,
        "fully_loaded_delivery_margin": 0.10,
        "market_headroom": 0.30,
        "downstream_funnel_success": 0.18,
        "strategic_exit_value_gap": 0.25,
    }


def test_gtm_first_is_dependence_robust():
    x = dependence_ambiguity_search()
    assert x["minimax_tie_count"] == 2
    assert x["selected"]["order"] == [
        "gtm-pack",
        "signed-strategy-gap-attestation",
        "finance-pack",
    ]
    assert round(x["selected"]["worst_case_expected_cost"], 3) == 11.0
    assert round(
        x["selected"]["reference_independent_expected_cost"], 4
    ) == 9.0225


def test_e074_promotion_contract():
    x = dependence_ambiguity_report_payload()
    assert all(x["promotion_gate"].values())
    assert x["promoted_ambiguity_rule"] == (
        "fixed-marginal-dependence-ambiguity-uses-frechet-minimax-order-v1"
    )
