from market_microcosm.exit_runoff_state_machine import (
    exit_runoff_report_payload,
    jooto_exit_states,
)


def test_jooto_exit_has_runoff_before_final_shutdown() -> None:
    runoff, shutdown = jooto_exit_states()
    assert runoff.state == "RUNOFF_AND_MIGRATION"
    assert runoff.accepts_new_customers is False
    assert runoff.serves_existing_customers is True
    assert runoff.transition_obligations_active is True
    assert shutdown.state == "FINAL_SHUTDOWN"


def test_e094_promotion_contract() -> None:
    payload = exit_runoff_report_payload()
    assert payload["runoff_inclusive_days"] == 360
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_exit_state_rule"] == (
        "strategic-exit-is-runoff-state-machine-not-instant-zeroing-v1"
    )
