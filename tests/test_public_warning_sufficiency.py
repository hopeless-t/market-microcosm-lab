from market_microcosm.public_warning_sufficiency import (
    prospective_warning_decision,
    public_evidence_sufficiency_report_payload,
    warning_feature_coverage,
)


def test_public_q3_evidence_does_not_cover_structural_warning_axes() -> None:
    row = warning_feature_coverage()

    assert row["covered_axes"] == []
    assert len(row["missing_axes"]) == 5
    assert row["coverage_fraction"] == 0.0
    assert row["complete"] is False


def test_missing_public_features_force_abstention() -> None:
    row = prospective_warning_decision()

    assert row["status"] == "ABSTAIN"
    assert row["decision"] == "INSUFFICIENT_PUBLIC_EVIDENCE"
    assert row["imputation_permitted"] is False


def test_e065_promotion_contract() -> None:
    payload = public_evidence_sufficiency_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_sufficiency_rule"] == (
        "structural-warning-must-abstain-when-public-feature-contract-is-incomplete-v1"
    )
