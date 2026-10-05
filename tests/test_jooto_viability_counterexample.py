from market_microcosm.jooto_viability_counterexample import (
    jooto_viability_report_payload,
    multi_axis_viability_classifier,
    naive_traction_classifier,
)


def test_nonzero_traction_can_false_positive_viability() -> None:
    naive = naive_traction_classifier()
    multi = multi_axis_viability_classifier()
    assert naive["traction_positive"] is True
    assert naive["decision"] == "VIABLE_GROWTH_BUSINESS"
    assert multi["failed_growth_axis_count"] == 5
    assert multi["profitability_failed"] is True
    assert multi["decision"] == "INDEPENDENT_GROWTH_VIABILITY_NOT_ESTABLISHED"


def test_e093_promotion_contract() -> None:
    payload = jooto_viability_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_viability_rule"] == (
        "nonzero-traction-does-not-certify-independent-growth-business-viability-v1"
    )
