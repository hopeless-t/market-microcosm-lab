import pytest

from market_microcosm.dcre020_use_or_lose_uncertainty import frozen_use_or_lose_uncertainty


def test_both_policies_serve_same_frozen_demand() -> None:
    reports = frozen_use_or_lose_uncertainty()
    flexible = reports["flexible"]
    rigid = reports["use_or_lose"]
    assert flexible.expected_served_demand == pytest.approx(130.0)
    assert rigid.expected_served_demand == pytest.approx(130.0)
    assert flexible.expected_unmet_demand == pytest.approx(0.0)
    assert rigid.expected_unmet_demand == pytest.approx(0.0)


def test_rigid_use_or_lose_doubles_expected_activation_resource() -> None:
    reports = frozen_use_or_lose_uncertainty()
    flexible = reports["flexible"]
    rigid = reports["use_or_lose"]
    assert flexible.expected_activation_resource == pytest.approx(15.0)
    assert rigid.expected_activation_resource == pytest.approx(30.0)


def test_rigid_obligation_creates_idle_capacity_in_low_demand_state() -> None:
    reports = frozen_use_or_lose_uncertainty()
    flexible = reports["flexible"]
    rigid = reports["use_or_lose"]
    assert flexible.expected_idle_capacity == pytest.approx(0.0)
    assert rigid.expected_idle_capacity == pytest.approx(30.0)
