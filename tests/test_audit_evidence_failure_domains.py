from market_microcosm.audit_evidence_failure_domains import (
    audit_evidence_failure_domain_report_payload,
    exact_failure_domain_aware_audit_cover,
)


def test_e061_shared_bundle_plan_has_common_mode_blast_two() -> None:
    row = exact_failure_domain_aware_audit_cover()
    e061 = row["e061_bundle_plan"]

    assert e061["total_cost"] == 6
    assert e061["evidence_failure_blast"][
        "maximum_obligation_blast"
    ] == 2


def test_failure_domain_safe_cover_uses_corroborated_bundle() -> None:
    row = exact_failure_domain_aware_audit_cover()
    selected = row["selected"]

    assert selected["total_cost"] == 8
    assert selected["action_ids"] == [
        "control-plane-bundle",
        "identity-targeted",
        "operator-targeted",
        "power-deep",
    ]
    assert selected["evidence_failure_blast"][
        "maximum_obligation_blast"
    ] == 1


def test_e062_promotion_contract() -> None:
    payload = audit_evidence_failure_domain_report_payload()

    assert payload[
        "e061_cost_authority_after_evidence_failure_model"
    ] == "REVOKED"
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_failure_domain_rule"] == (
        "audit-evidence-reuse-must-model-proof-obligation-failure-blast-v1"
    )
