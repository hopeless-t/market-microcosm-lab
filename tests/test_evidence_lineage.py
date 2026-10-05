from market_microcosm.evidence_lineage import (
    evidence_lineage_report_payload,
    hidden_root_reference,
    lineage_diversified_repair,
)


def test_distinct_source_labels_can_share_one_hidden_root() -> None:
    row = hidden_root_reference()
    source = row["source_aware_quorum"]

    assert source["accepted"] is True
    assert source["accepted_value"] is False
    assert len(source["accepted_sources"]) == 3
    assert source["accepted_roots"] == ["master-warehouse"]


def test_root_audit_revokes_false_quorum() -> None:
    row = hidden_root_reference()

    assert row["root_aware_quorum"]["accepted"] is False


def test_diversified_lineage_restores_true_quorum() -> None:
    row = lineage_diversified_repair()

    assert row["accepted"] is True
    assert row["accepted_value"] is True
    assert len(row["accepted_roots"]) == 3


def test_e050_promotion_contract() -> None:
    payload = evidence_lineage_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_lineage_rule"] == (
        "predicate-quorum-must-audit-upstream-lineage-roots-v1"
    )
