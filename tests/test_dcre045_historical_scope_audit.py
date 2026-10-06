from market_microcosm.dcre045_historical_scope_audit import (
    dcre045_scope_aligned_history_audit,
)


def test_lbnl_pair_is_scope_aligned_but_not_causally_admissible() -> None:
    report = dcre045_scope_aligned_history_audit()
    audit = report["audit"]
    assert audit.same_geography is True
    assert audit.same_equipment_scope is True
    assert audit.overlapping_period is True
    assert audit.causal_calibration_admissible is False


def test_model_family_dependence_and_semantic_mismatch_block_eta() -> None:
    report = dcre045_scope_aligned_history_audit()
    reasons = report["audit"].blocking_reasons
    assert "MODEL_FAMILY_DEPENDENCE" in reasons
    assert "NO_SERVICE_OR_COMPUTE_DEMAND_QUANTITY" in reasons
    assert "NO_COMPLETE_PUBLIC_PAIRED_NUMERIC_SERIES" in reasons
    assert report["candidate_eta"] is None


def test_chart_digitization_is_not_an_automatic_calibration_path() -> None:
    report = dcre045_scope_aligned_history_audit()
    assert report["chart_digitization_authorized"] is False
    assert report["authority_effect"] == "NONE"
