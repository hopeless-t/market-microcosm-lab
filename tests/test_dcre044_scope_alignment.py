from market_microcosm.dcre044_scope_alignment import (
    causal_elasticity_ready_candidates,
    promotion_requirements,
    scope_alignment_candidates,
    scope_alignment_report,
)


def test_current_public_pairs_do_not_identify_causal_eta() -> None:
    assert len(scope_alignment_candidates()) == 3
    assert causal_elasticity_ready_candidates() == ()
    report = scope_alignment_report()
    assert report["eta_status"] == "UNKNOWN"
    assert report["automatic_eta_write"] is None


def test_each_rejected_pair_has_explicit_blocker() -> None:
    assert all(row.blocker for row in scope_alignment_candidates())
    assert all(row.causal_elasticity_ready is False for row in scope_alignment_candidates())


def test_promotion_contract_requires_scope_time_grain_and_identification() -> None:
    requirements = promotion_requirements()
    assert "matched_scope" in requirements
    assert "matched_period_or_explicit_lag_model" in requirements
    assert "stock_or_throughput_volume_not_unmatched_shipment_flow" in requirements
    assert "causal_confounders_or_identification_strategy_explicit" in requirements
