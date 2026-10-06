from market_microcosm.dcre063_empirical_evidence_matrix import (
    EvidenceClass,
    dcre063_empirical_evidence_matrix_report,
)


def test_empirical_evidence_classes_remain_categorical() -> None:
    report = dcre063_empirical_evidence_matrix_report()
    classes = {row.evidence_class for row in report["rows"]}
    assert EvidenceClass.PRIMARY_SOURCE_REPORTED in classes
    assert EvidenceClass.THIRD_PARTY_ASSURED_PRIMARY in classes
    assert EvidenceClass.INDEPENDENT_OFFICIAL_CROSSCHECK in classes
    assert EvidenceClass.SECONDARY_DERIVED_CANDIDATE in classes


def test_secondary_reliability_transcription_is_not_promoted() -> None:
    report = dcre063_empirical_evidence_matrix_report()
    reliability = next(
        row for row in report["rows"] if "SAIDI/SAIFI" in row.claim
    )
    assert reliability.evidence_class is EvidenceClass.SECONDARY_DERIVED_CANDIDATE
    assert reliability.promoted is False
    assert "direct NWCPUD row" in reliability.blocker
    assert report["reliability_candidate_promoted"] is False


def test_no_empirical_row_is_laundered_into_causal_identification() -> None:
    report = dcre063_empirical_evidence_matrix_report()
    assert report["promoted_count"] >= 6
    assert report["candidate_count"] >= 1
    assert report["causal_count"] == 0
    assert report["causally_identified_rows"] == ()
    assert report["authority_effect"] == "NONE"
