from market_microcosm.evidence_quorum import (
    conflict_reference,
    evidence_quorum_report_payload,
    single_witness_reference,
)


def test_single_witness_can_disagree_with_independent_quorum() -> None:
    row = single_witness_reference()

    assert row["single_witness_result"] is False
    assert row["quorum_result"]["accepted_value"] is True
    assert row["single_witness_disagrees_with_quorum"] is True


def test_conflict_without_three_votes_abstains() -> None:
    row = conflict_reference()

    assert row["accepted"] is False
    assert row["accepted_value"] is None


def test_e048_promotion_contract() -> None:
    payload = evidence_quorum_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_quorum_rule"] == (
        "predicate-attestation-requires-independent-witness-quorum-v1"
    )
