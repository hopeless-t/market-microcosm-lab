from market_microcosm.research_portfolio_projection_maturity import rpe012_report_payload


def test_rpe012_projection_maturity_contract() -> None:
    payload = rpe012_report_payload()
    assert payload["experiment"] == "RPE-012"
    assert all(payload["promotion_gate"].values())

    summary = payload["summary"]
    assert summary["sample_size"] == 5
    assert summary["docs_only_at_insertion_count"] == 5
    assert summary["persist_on_main_count"] == 5
    assert summary["unique_source_operational_transfer_confirmed_count"] == 0
    assert summary["persistent_docs_only_unknown_count"] == 3
    assert summary["maturity_counts"] == {
        "CONVERGENT_OTHER_SOURCE": 1,
        "PERSISTENT_DOC_ONLY_UNKNOWN": 3,
        "REINFORCEMENT_OF_PREEXISTING_MECHANISM": 1,
    }

    rows = {row["repository"]: row for row in payload["sample"]}
    assert rows["recursive-flourishing-lab"]["maturity"] == "REINFORCEMENT_OF_PREEXISTING_MECHANISM"
    assert rows["next-generation-github"]["maturity"] == "CONVERGENT_OTHER_SOURCE"
    assert payload["claim_ceiling"].startswith("FIVE_REPOSITORY_OBSERVED_METADATA_AND_FILE_SAMPLE_ONLY")
