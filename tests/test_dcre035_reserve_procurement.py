import pytest

from market_microcosm.dcre035_reserve_procurement import frozen_reserve_procurement


def test_no_capacity_payment_produces_no_private_reserve() -> None:
    report = frozen_reserve_procurement()["no_payment"]
    assert report["selected_names"] == ()
    assert report["aggregate_reserve"] == pytest.approx(0.0)
    assert report["system_expected_cost"] == pytest.approx(4.0)


def test_zero_profit_knee_does_not_induce_entry_under_strict_rule() -> None:
    report = frozen_reserve_procurement()["at_knee"]
    assert report["selected_names"] == ()
    assert report["aggregate_reserve"] == pytest.approx(0.0)


def test_slightly_above_private_knee_procures_full_twenty_unit_reserve() -> None:
    report = frozen_reserve_procurement()["above_knee"]
    assert report["selected_names"] == ("P1", "P2")
    assert report["aggregate_reserve"] == pytest.approx(20.0)
    assert report["system_expected_cost"] == pytest.approx(2.0)
    assert report["total_capacity_payment"] == pytest.approx(2.2)


def test_private_payment_knee_matches_holding_cost() -> None:
    assert frozen_reserve_procurement()["payment_knee"] == pytest.approx(0.1)
