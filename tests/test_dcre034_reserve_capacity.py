import pytest

from market_microcosm.dcre034_reserve_capacity import frozen_reserve_market


def test_low_shock_probability_prefers_no_reserve() -> None:
    report = frozen_reserve_market()["low_risk"]
    assert report.reserve_units == pytest.approx(0.0)
    assert report.expected_total_cost == pytest.approx(1.0)


def test_high_shock_probability_prefers_full_twenty_unit_reserve() -> None:
    report = frozen_reserve_market()["high_risk"]
    assert report.reserve_units == pytest.approx(20.0)
    assert report.expected_total_cost == pytest.approx(2.0)


def test_marginal_probability_knee_is_ten_percent() -> None:
    assert frozen_reserve_market()["probability_knee"] == pytest.approx(0.1)
