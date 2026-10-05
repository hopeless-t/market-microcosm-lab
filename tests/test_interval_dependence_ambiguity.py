from market_microcosm.interval_dependence_ambiguity import (
    interval_dependence_report_payload,
    interval_dependence_search,
)


def test_interval_dependence_minimax():
    x = interval_dependence_search()
    assert x["minimax_tie_count"] == 2
    assert x["selected"]["order"] == [
        "gtm-pack",
        "signed-strategy-gap-attestation",
        "finance-pack",
    ]
    assert round(
        x["selected"]["worst_case_expected_cost"], 3
    ) == 12.0
    assert all(row["bound_is_tight"] for row in x["rows"])


def test_e075_promotion_contract():
    x = interval_dependence_report_payload()
    assert all(x["promotion_gate"].values())
    assert x["promoted_interval_rule"] == (
        "interval-marginal-dependence-ambiguity-uses-lower-risk-frechet-bound-v1"
    )
