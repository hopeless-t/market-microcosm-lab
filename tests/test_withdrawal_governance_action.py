from market_microcosm.withdrawal_governance_action import (
    governance_action,
    withdrawal_governance_report_payload,
)


def test_withdrawal_escalates_without_deterministic_exit() -> None:
    assert governance_action("KPI_WITHDRAWN", "DUE_TO_DETERIORATION") == (
        "ESCALATE_REVIEW"
    )
    assert governance_action("KPI_WITHDRAWN", "DUE_TO_METRIC_REDESIGN") == (
        "KERNEL_CHANGE_ONLY"
    )
    assert governance_action("KPI_WITHDRAWN", None) == "ABSTAIN_REASON_UNKNOWN"


def test_explicit_exit_event_has_separate_authority() -> None:
    assert governance_action(
        "SUBSIDIARY_DISSOLUTION_AND_LIQUIDATION_DECISION"
    ) == "EXIT_CONFIRMED"


def test_e086_promotion_contract() -> None:
    payload = withdrawal_governance_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_governance_rule"] == (
        "deterioration-linked-kpi-withdrawal-triggers-review-not-deterministic-exit-v1"
    )
