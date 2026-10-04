from market_microcosm.decision_sufficient_acquisition import exact_minimum_decision_portfolio, decision_sufficient_acquisition_report_payload

def test_downstream_failure_needs_only_cheap_funnel_evidence():
    x=exact_minimum_decision_portfolio("downstream_funnel_success-only-bad")["selected"]
    assert x["acquisition_ids"]==["crm-funnel-export"]
    assert x["total_cost"]==2
    assert x["decision"]=="CERTIFIED_WARN"

def test_safe_world_requires_full_contract():
    x=exact_minimum_decision_portfolio("all-safe")["selected"]
    assert x["acquisition_ids"]==["finance-pack","gtm-pack","signed-strategy-gap-attestation"]
    assert x["total_cost"]==14
    assert x["decision"]=="CERTIFIED_SAFE"

def test_e068_promotion_contract():
    x=decision_sufficient_acquisition_report_payload()
    assert all(x["promotion_gate"].values())
    assert x["promoted_decision_rule"]=="warning-evidence-acquisition-is-decision-sufficient-not-full-state-v1"
