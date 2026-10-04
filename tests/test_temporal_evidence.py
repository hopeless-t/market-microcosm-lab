from market_microcosm.temporal_evidence import (
    select_fresh_generation_aligned_evidence,
    temporal_evidence_report_payload,
)


def test_authority_only_selection_can_use_wrong_generation() -> None:
    row = select_fresh_generation_aligned_evidence()

    selected = row["authority_only_selection"]
    assert selected["name"] == "fresh_old_generation_attestation"
    assert selected["generation_matches"] is False
    assert selected["admissible"] is False


def test_temporal_generation_filter_selects_fresh_v2_attestation() -> None:
    row = select_fresh_generation_aligned_evidence()

    selected = row["temporal_generation_selection"]
    assert selected["name"] == "fresh_current_generation_attestation"
    assert selected["fresh"] is True
    assert selected["generation_matches"] is True


def test_e047_promotion_contract() -> None:
    payload = temporal_evidence_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_temporal_rule"] == (
        "active-sensing-evidence-must-be-fresh-and-generation-aligned-v1"
    )
