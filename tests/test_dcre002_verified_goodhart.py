from market_microcosm.dcre002_verified_goodhart import (
    frozen_items,
    option_preserving_exact,
    verified_count_gate,
    verified_utility_gate,
)


def test_verified_count_gate_goodharts_on_easy_work() -> None:
    result = verified_count_gate(frozen_items())
    assert result.selected_ids == ("R1", "R2", "R3", "R4", "E1")
    assert result.verified_utility == 20
    assert result.option_value == 0
    assert result.mandatory_complete is False


def test_verified_utility_gate_recovers_mandatory_work_but_discards_option_value() -> None:
    result = verified_utility_gate(frozen_items())
    assert result.selected_ids == ("E1", "E2")
    assert result.verified_utility == 24
    assert result.option_value == 0
    assert result.mandatory_complete is True


def test_option_preserving_exact_keeps_mandatory_and_probe_value() -> None:
    result = option_preserving_exact(frozen_items())
    assert result.selected_ids == ("E1", "E2", "P1", "P2")
    assert result.resource_used == 10
    assert result.verification_used == 8
    assert result.verified_utility == 24
    assert result.option_value == 12
    assert result.total_value == 36
    assert result.mandatory_complete is True


def test_verified_count_is_not_a_safe_proxy_for_value() -> None:
    count_gate = verified_count_gate(frozen_items())
    exact = option_preserving_exact(frozen_items())
    assert len(count_gate.selected_ids) > 2
    assert count_gate.total_value < exact.total_value
    assert not count_gate.mandatory_complete
    assert exact.mandatory_complete
