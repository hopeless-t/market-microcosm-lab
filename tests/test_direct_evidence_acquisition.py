from market_microcosm.direct_evidence_acquisition import exact_acquisition_portfolio, direct_evidence_acquisition_report_payload

def test_naive_optimizer_uses_unauthorized_board_minutes():
    x=exact_acquisition_portfolio(authorized_only=False)["selected"]
    assert x["total_cost"]==10
    assert "raw-board-minutes" in x["acquisition_ids"]
    assert x["all_authorized"] is False

def test_authorized_minimum_portfolio():
    x=exact_acquisition_portfolio(authorized_only=True)["selected"]
    assert x["acquisition_ids"]==["finance-pack","gtm-pack","signed-strategy-gap-attestation"]
    assert x["total_cost"]==14
    assert len(x["covered_axes"])==5
    assert x["all_authorized"] is True

def test_e067_promotion_contract():
    x=direct_evidence_acquisition_report_payload()
    assert all(x["promotion_gate"].values())
    assert x["promoted_acquisition_rule"]=="acquire-minimum-authorized-direct-feature-portfolio-v1"
