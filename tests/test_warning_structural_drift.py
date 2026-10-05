from market_microcosm.warning_structural_drift import (
    structural_drift_report_payload,
)


def test_e036_warning_is_revoked_by_interaction_shift() -> None:
    payload = structural_drift_report_payload()

    assert payload["legacy_e036_score"]["recall"] < 0.98
    assert payload["legacy_authority_after_shift"] == "REVOKED"


def test_interaction_repair_restores_warning_quality() -> None:
    payload = structural_drift_report_payload()
    repaired = payload["interaction_aware_score"]

    assert repaired["recall"] > 0.99
    assert repaired["precision"] > 0.99
    assert repaired["f1"] > payload["legacy_e036_score"]["f1"]


def test_e037_promotion_contract() -> None:
    payload = structural_drift_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_repair_rule"] == (
        "interaction-aware-warning-generation-v2"
    )
