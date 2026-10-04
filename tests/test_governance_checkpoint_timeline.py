from market_microcosm.governance_checkpoint_timeline import (
    checkpoint_timeline,
    governance_checkpoint_report_payload,
)


def test_allied_governance_timeline_has_intermediate_exit_criteria() -> None:
    row = checkpoint_timeline()
    assert row["chronological"] is True
    assert row["states"] == [
        "REPORTING_REGIME_BREAK",
        "EXPLICIT_EXIT_CRITERIA_BOUND",
        "EXIT_CONFIRMED",
    ]
    assert row["days_reporting_break_to_exit"] == 260


def test_e087_promotion_contract() -> None:
    payload = governance_checkpoint_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_checkpoint_rule"] == (
        "deterioration-governance-path-uses-explicit-exit-criteria-checkpoint-v1"
    )
