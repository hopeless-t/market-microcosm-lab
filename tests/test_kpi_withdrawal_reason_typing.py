from market_microcosm.kpi_withdrawal_reason_typing import (
    reference_cases,
    scalar_withdrawal_classifier,
    typed_withdrawal_classifier,
    withdrawal_reason_report_payload,
)


def test_scalar_withdrawal_boolean_is_not_semantically_sufficient() -> None:
    allied, redesign = reference_cases()
    assert scalar_withdrawal_classifier(allied) is True
    assert scalar_withdrawal_classifier(redesign) is True
    assert typed_withdrawal_classifier(allied) is True
    assert typed_withdrawal_classifier(redesign) is False


def test_e082_promotion_contract() -> None:
    payload = withdrawal_reason_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_typing_rule"] == (
        "kpi-withdrawal-requires-reason-type-and-source-authority-v1"
    )
