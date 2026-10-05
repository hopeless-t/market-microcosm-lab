from market_microcosm.authority_constrained_sensing import (
    authority_constrained_active_sensing_report_payload,
    select_authority_constrained_candidate,
)


def test_naive_cost_search_can_choose_unauthorized_evidence() -> None:
    row = select_authority_constrained_candidate()

    assert row["naive_cost_only_selection"]["name"] == (
        "raw_customer_ledger_boolean"
    )
    assert row["naive_cost_only_selection"]["authorized"] is False


def test_authority_filter_selects_predicate_attestation() -> None:
    row = select_authority_constrained_candidate()

    assert row["authorized_selection"]["name"] == (
        "signed_predicate_attestation"
    )
    assert row["authorized_selection"]["cost"] == 3


def test_e046_promotion_contract() -> None:
    payload = authority_constrained_active_sensing_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_authority_rule"] == (
        "active-sensing-optimizes-only-within-authorized-evidence-set-v1"
    )
