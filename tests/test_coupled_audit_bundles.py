from market_microcosm.coupled_audit_bundles import (
    coupled_audit_bundle_report_payload,
    exact_audit_bundle_cover,
)


def test_exact_shared_audit_bundle_cover() -> None:
    row = exact_audit_bundle_cover()
    selected = row["selected"]

    assert selected["action_ids"] == [
        "control-plane-bundle",
        "infra-resilience-bundle",
    ]
    assert selected["action_count"] == 2
    assert selected["total_cost"] == 6


def test_shared_bundles_beat_independent_branch_cost() -> None:
    row = exact_audit_bundle_cover()

    assert row["e060_independent_cost"] == 8
    assert row["savings_vs_e060"] == 2


def test_e061_promotion_contract() -> None:
    payload = coupled_audit_bundle_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_bundle_rule"] == (
        "dependency-audit-allocation-must-model-shared-evidence-bundles-v1"
    )
