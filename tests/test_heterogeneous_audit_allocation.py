from market_microcosm.heterogeneous_audit_allocation import (
    exact_branch_audit_allocation,
    heterogeneous_audit_report_payload,
)


def test_exact_branch_specific_allocation() -> None:
    row = exact_branch_audit_allocation()
    selected = row["selected"]

    assert selected["total_cost"] == 8
    assert selected["selection"]["network"]["option"] == "targeted"
    assert selected["selection"]["identity"]["option"] == "targeted"
    assert selected["selection"]["power"]["option"] == "deep"
    assert selected["selection"]["vendor"]["option"] == "none"
    assert selected["selection"]["operator"]["option"] == "targeted"


def test_branch_specific_allocation_beats_uniform_deep() -> None:
    row = exact_branch_audit_allocation()

    assert row["uniform_deep_cost"] == 16
    assert row["cost_savings_vs_uniform_deep"] == 8


def test_e060_promotion_contract() -> None:
    payload = heterogeneous_audit_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_allocation_rule"] == (
        "recursive-lineage-audit-depth-is-allocated-per-proof-obligation-v1"
    )
