import pytest

from market_microcosm.dcre039_backlog_release import frozen_backlog_recovery


def test_release_all_creates_second_shortfall_and_demand_peak() -> None:
    report = frozen_backlog_recovery()["release_all"]
    assert len(report.epochs) == 2
    assert tuple(row.demand for row in report.epochs) == pytest.approx((140.0, 120.0))
    assert report.peak_demand == pytest.approx(140.0)
    assert report.total_new_shortfall == pytest.approx(20.0)
    assert report.ending_backlog == pytest.approx(0.0)


def test_capacity_aware_release_clears_same_backlog_without_new_shortfall() -> None:
    report = frozen_backlog_recovery()["capacity_aware"]
    assert len(report.epochs) == 2
    assert tuple(row.demand for row in report.epochs) == pytest.approx((120.0, 120.0))
    assert tuple(row.attempted_release for row in report.epochs) == pytest.approx((20.0, 20.0))
    assert report.peak_demand == pytest.approx(120.0)
    assert report.total_new_shortfall == pytest.approx(0.0)
    assert report.ending_backlog == pytest.approx(0.0)


def test_release_all_does_not_clear_backlog_faster_in_frozen_world() -> None:
    report = frozen_backlog_recovery()
    assert len(report["release_all"].epochs) == len(report["capacity_aware"].epochs) == 2
    assert report["release_all"].peak_demand > report["capacity_aware"].peak_demand
    assert report["release_all"].total_new_shortfall > report["capacity_aware"].total_new_shortfall
