from market_microcosm.exit_residual_value import (
    jooto_exit_value_state,
    residual_value_report_payload,
)


def test_business_exit_and_residual_value_are_separate() -> None:
    row = jooto_exit_value_state()
    assert row["standalone_growth_viability"] is False
    assert row["residual_capability_value_zero"] is False
    assert row["toyota_custom_tool"] == "CONTINUES"
    assert row["employee_capability"] == "REDEPLOYED_INTERNALLY"


def test_e095_promotion_contract() -> None:
    payload = residual_value_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_residual_value_rule"] == (
        "service-business-exit-does-not-imply-zero-residual-capability-value-v1"
    )
