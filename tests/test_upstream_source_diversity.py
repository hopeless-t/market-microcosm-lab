from market_microcosm.upstream_source_diversity import (
    diversified_repair_reference,
    hidden_common_source_reference,
    upstream_source_diversity_report_payload,
)


def test_domain_diverse_quorum_can_share_one_bad_source() -> None:
    row = hidden_common_source_reference()

    assert row["domain_only_quorum"]["accepted_value"] is False
    assert len(row["domain_only_quorum"]["accepted_domains"]) == 3
    assert row["domain_only_quorum"]["accepted_sources"] == ["shared-feed"]


def test_source_diversity_revokes_common_mode_false_quorum() -> None:
    row = hidden_common_source_reference()

    assert row["source_aware_quorum"]["accepted"] is False


def test_diversified_repair_accepts_true() -> None:
    row = diversified_repair_reference()

    assert row["accepted"] is True
    assert row["accepted_value"] is True
    assert len(row["accepted_sources"]) == 3


def test_e049_promotion_contract() -> None:
    payload = upstream_source_diversity_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_source_rule"] == (
        "predicate-quorum-must-diversify-upstream-evidence-sources-v1"
    )
