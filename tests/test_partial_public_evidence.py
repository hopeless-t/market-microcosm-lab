from market_microcosm.partial_public_evidence import exact_public_evidence_portfolio, partial_public_evidence_report_payload

def test_exact_minimum_partial_evidence_portfolio():
    x=exact_public_evidence_portfolio()["selected"]
    assert x["artifact_ids"]==["q3-financial-summary","q3-market-environment"]
    assert x["total_cost"]==2
    assert (x["coverage"]["direct_count"],x["coverage"]["partial_count"],x["coverage"]["absent_count"])==(0,2,3)

def test_partial_axes_do_not_satisfy_direct_contract():
    x=exact_public_evidence_portfolio()["selected"]["coverage"]
    assert x["partial_axes"]==["fully_loaded_delivery_margin","market_headroom"]
    assert x["direct_contract_complete"] is False

def test_e066_promotion_contract():
    x=partial_public_evidence_report_payload()
    assert x["e065_direct_coverage_authority"]=="CONFIRMED"
    assert x["e065_information_granularity_authority"]=="REFINED"
    assert x["prospective_warning"]["status"]=="ABSTAIN"
    assert all(x["promotion_gate"].values())
