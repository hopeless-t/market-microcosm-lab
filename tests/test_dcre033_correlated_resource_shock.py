import pytest

from market_microcosm.dcre033_correlated_resource_shock import frozen_resource_shocks


def test_baseline_diversified_capacity_is_feasible() -> None:
    report = frozen_resource_shocks()["baseline"]
    assert report.feasible is True
    assert report.selected_a == pytest.approx(50.0)
    assert report.selected_b == pytest.approx(50.0)


def test_independent_regional_shock_can_be_reallocated() -> None:
    report = frozen_resource_shocks()["independent_shock"]
    assert report.aggregate_capacity == pytest.approx(100.0)
    assert report.feasible is True
    assert report.selected_a == pytest.approx(40.0)
    assert report.selected_b == pytest.approx(60.0)


def test_common_shock_eliminates_feasible_allocation() -> None:
    report = frozen_resource_shocks()["common_shock"]
    assert report.aggregate_capacity == pytest.approx(80.0)
    assert report.feasible is False
    assert report.selected_a is None
    assert report.selected_b is None
