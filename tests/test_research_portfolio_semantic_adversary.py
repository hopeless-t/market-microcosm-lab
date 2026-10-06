from market_microcosm.research_portfolio_semantic_adversary import rpe002_report_payload


def test_rpe002_semantic_adversary_contract() -> None:
    payload = rpe002_report_payload()
    assert payload["experiment"] == "RPE-002"
    assert all(payload["promotion_gate"].values())

    policies = payload["policies"]
    reference = policies["ground_truth_reference"]
    topic = policies["surface_topic_canonicalizer"]
    no_merge = policies["no_merge_fail_closed"]
    guarded = policies["invariant_guarded_canonicalizer"]

    assert reference["review_cost"] == 38
    assert reference["verified_decision_value_coverage"] == 1.0

    assert topic["false_merge_pairs"] == 1
    assert topic["false_split_meaning_count"] == 1
    assert topic["duplicate_semantic_projections"] == 1
    assert topic["review_cost"] == 39
    assert topic["verified_decision_value_coverage"] == 0.7875

    assert no_merge["false_merge_pairs"] == 0
    assert no_merge["verified_decision_value_coverage"] == 1.0
    assert no_merge["review_cost"] == 52

    assert guarded["false_merge_pairs"] == 0
    assert guarded["false_split_meaning_count"] == 0
    assert guarded["review_cost"] == reference["review_cost"]
    assert guarded["verified_decision_value_coverage"] == 1.0

    assert payload["comparison"]["surface_topic_verified_value_loss_pct"] == 21.25
    assert payload["claim_ceiling"].startswith("DETERMINISTIC_SYNTHETIC")
