from market_microcosm.dependency_depth_stopping import (
    compile_minimum_audit_depth,
    dependency_depth_stopping_report_payload,
)


def test_minimum_certifying_audit_depth_is_two() -> None:
    row = compile_minimum_audit_depth()

    assert row["status"] == "SAT"
    assert row["selected"]["depth"] == 2
    assert row["selected"]["cumulative_cost"] == 5
    assert row["selected"]["maximum_unverified_blast_channels"] == 2


def test_deeper_audit_adds_cost_without_stronger_reference_bound() -> None:
    row = compile_minimum_audit_depth()
    depth2 = row["depths"][2]
    depth3 = row["depths"][3]

    assert depth2["maximum_unverified_blast_channels"] == 2
    assert depth3["maximum_unverified_blast_channels"] == 2
    assert depth3["cumulative_cost"] > depth2["cumulative_cost"]


def test_e059_promotion_contract() -> None:
    payload = dependency_depth_stopping_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_stopping_rule"] == (
        "recursive-lineage-audit-stops-at-minimum-depth-meeting-blast-budget-v1"
    )
