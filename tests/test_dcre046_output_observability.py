from market_microcosm.dcre046_output_observability import (
    dcre046_output_observability_audit,
)


def test_google_pair_is_scope_aligned_but_period_misaligned() -> None:
    report = dcre046_output_observability_audit()
    audit = report["audit"]
    assert audit.scope_aligned is True
    assert audit.period_aligned is False
    assert "BASELINE_PERIOD_MISMATCH" in audit.blocking_reasons


def test_compute_metric_opacity_blocks_absolute_output_reconstruction() -> None:
    report = dcre046_output_observability_audit()
    audit = report["audit"]
    assert audit.definition_reproducible is False
    assert audit.absolute_output_reconstructible is False
    assert "COMPUTE_METRIC_DEFINITION_OPAQUE" in audit.blocking_reasons
    assert "NO_PUBLIC_COMPUTE_INDEX_SERIES" in audit.blocking_reasons


def test_unknown_point_estimates_are_preserved_but_partial_identification_remains_open() -> None:
    report = dcre046_output_observability_audit()
    assert report["candidate_output_growth"] is None
    assert report["candidate_eta"] is None
    assert report["partial_identification_candidate"] is True
    assert report["authority_effect"] == "NONE"
