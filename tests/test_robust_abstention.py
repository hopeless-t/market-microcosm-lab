from market_microcosm.robust_abstention import (
    abstention_reference,
    robust_abstention_report_payload,
)


def test_boundary_straddling_interval_abstains() -> None:
    row = abstention_reference()

    assert row["ambiguous_interval"] == [1.5, 2.5]
    assert row["ambiguous_robust_result"] == "ABSTAIN"


def test_clear_intervals_still_decide() -> None:
    row = abstention_reference()

    assert row["clearly_true_result"] == "CERTIFIED_TRUE"
    assert row["clearly_false_result"] == "CERTIFIED_FALSE"


def test_midpoint_forcing_is_unsound() -> None:
    row = abstention_reference()

    assert row["midpoint_forced_result"] is True
    assert row["midpoint_forced_decision_is_unsound"] is True


def test_e044_promotion_contract() -> None:
    payload = robust_abstention_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_decision_rule"] == (
        "boundary-straddling-uncertainty-must-abstain-v1"
    )
