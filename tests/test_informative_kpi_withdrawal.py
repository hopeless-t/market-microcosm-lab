from market_microcosm.informative_kpi_withdrawal import (
    allied_overseas_saas_withdrawal,
    informative_missingness_report_payload,
    withdrawal_aware_handler,
)


def test_withdrawal_event_revokes_old_series_authority() -> None:
    event = allied_overseas_saas_withdrawal()
    assert event.event_type == "KPI_WITHDRAWN_DUE_TO_DETERIORATION"
    assert event.old_series_authority == "REVOKED_AFTER_WITHDRAWAL"
    assert "arr" in event.withdrawn_kpis
    assert "churn_rate" in event.withdrawn_kpis


def test_withdrawal_aware_handler_fails_closed() -> None:
    row = withdrawal_aware_handler()
    assert row["series_status"] == "TERMINATED_BY_REPORTING_POLICY_CHANGE"
    assert row["forward_fill_permitted"] is False
    assert row["post_withdrawal_numeric_imputation_permitted"] is False
    assert row["cross_withdrawal_trend_extension_permitted"] is False
    assert row["withdrawal_event_can_be_used_as_categorical_evidence"] is True
    assert row["hidden_kpi_value_inference_permitted"] is False


def test_e079_promotion_contract() -> None:
    payload = informative_missingness_report_payload()
    assert payload["missingness_class"] == "INFORMATIVE_STATE_DEPENDENT_REPORTING"
    assert payload["formal_mnar_claim"] is False
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_missingness_rule"] == (
        "kpi-withdrawal-is-first-class-informative-observation-event-v1"
    )
