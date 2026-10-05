from market_microcosm.withdrawal_exit_holdout import (
    longitudinal_holdout,
    withdrawal_exit_holdout_report_payload,
)


def test_withdrawal_precedes_exit_holdout_by_260_days() -> None:
    row = longitudinal_holdout()
    assert row["chronological"] is True
    assert row["days_between"] == 260
    assert row["same_business_lineage"] is True


def test_e085_promotion_contract() -> None:
    payload = withdrawal_exit_holdout_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_holdout_rule"] == (
        "informative-kpi-withdrawal-is-retained-as-prospective-event-anchor-v1"
    )
