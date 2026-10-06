import pytest

from market_microcosm.dcre028_temporal_resources import frozen_temporal_market


def test_energy_only_shift_overloads_offpeak_water() -> None:
    report = frozen_temporal_market()["energy_greedy"]
    assert report.flexible_peak_tasks == pytest.approx(0.0)
    assert report.peak_energy == pytest.approx(56.0)
    assert report.offpeak_water == pytest.approx(24.0)
    assert report.jointly_viable is False


def test_water_only_shift_overloads_peak_energy() -> None:
    report = frozen_temporal_market()["water_greedy"]
    assert report.flexible_peak_tasks == pytest.approx(40.0)
    assert report.peak_energy == pytest.approx(88.0)
    assert report.jointly_viable is False


def test_joint_temporal_grid_finds_only_viable_coarse_allocation() -> None:
    report = frozen_temporal_market()["joint"]
    assert report.flexible_peak_tasks == pytest.approx(10.0)
    assert report.peak_tasks == pytest.approx(80.0)
    assert report.offpeak_tasks == pytest.approx(50.0)
    assert report.peak_energy == pytest.approx(64.0)
    assert report.peak_water == pytest.approx(16.0)
    assert report.offpeak_energy == pytest.approx(40.0)
    assert report.offpeak_water == pytest.approx(20.0)
    assert report.jointly_viable is True
