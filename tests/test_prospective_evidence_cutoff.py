from market_microcosm.prospective_evidence_cutoff import (
    availability_partition,
    feature_sets,
    prospective_evidence_cutoff_report_payload,
)


def test_q4_annotations_are_future_relative_to_q3_cutoff() -> None:
    row = availability_partition()
    future = {item["evidence_id"] for item in row["future_only"]}

    assert "q4_launch_delay_annotation" in future
    assert "q4_withdrawal_prep_annotation" in future
    assert "q4_outcome_metrics" in future


def test_retrospective_features_are_rejected_for_prospective_warning() -> None:
    row = feature_sets()

    assert row["prospective_all_available"] is True
    assert row["retrospective_contains_future_leakage"] is True
    assert row["leaked_feature_ids"] == [
        "q4_launch_delay_annotation",
        "q4_withdrawal_prep_annotation",
    ]


def test_e064_promotion_contract() -> None:
    payload = prospective_evidence_cutoff_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_cutoff_rule"] == (
        "prospective-warning-evidence-must-exist-before-decision-cutoff-v1"
    )
