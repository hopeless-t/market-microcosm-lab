from market_microcosm.research_portfolio_real_fanout import rpe011_report_payload


def test_rpe011_observed_strata_fanout_contract() -> None:
    payload = rpe011_report_payload()
    assert payload["experiment"] == "RPE-011"
    assert all(payload["promotion_gate"].values())

    observed = payload["observed"]
    assert observed["commit_count"] == 24
    assert observed["distinct_repository_count"] == 24
    assert observed["window_seconds"] == 380.0
    assert observed["max_intercommit_gap_seconds"] == 40.0
    assert observed["all_messages_explicitly_reference_strata"] is True
    assert observed["one_commit_per_repository_in_snapshot"] is True

    counterfactual = payload["counterfactual_envelope"]
    assert counterfactual["observed_materializations"] == 24
    assert counterfactual["candidate_canonical_source_events"] == 1
    assert counterfactual["minimum_projection_count_if_no_downstream_need_is_known"] == 0
    assert counterfactual["maximum_projection_count_if_every_observed_projection_was_needed"] == 24
    assert counterfactual["decision_relevant_projection_count"] is None
    assert counterfactual["counterfactual_materialization_savings"] is None
    assert payload["claim_ceiling"].startswith("OBSERVED_GITHUB_COMMIT_METADATA_CLUSTER_ONLY")
