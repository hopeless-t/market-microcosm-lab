import pytest

from market_microcosm.dcre022_spatial_resources import frozen_spatial_allocation


def test_energy_headroom_greedy_overloads_water_in_grid_rich_region() -> None:
    report = frozen_spatial_allocation()["energy_greedy"]
    assert report.grid_rich_tasks == pytest.approx(100.0)
    assert report.grid_rich_energy == pytest.approx(80.0)
    assert report.grid_rich_water == pytest.approx(30.0)
    assert report.jointly_viable is False


def test_water_headroom_greedy_overloads_energy_in_water_rich_region() -> None:
    report = frozen_spatial_allocation()["water_greedy"]
    assert report.water_rich_tasks == pytest.approx(100.0)
    assert report.water_rich_energy == pytest.approx(80.0)
    assert report.water_rich_water == pytest.approx(30.0)
    assert report.jointly_viable is False


def test_joint_grid_splits_work_across_complementary_headroom() -> None:
    report = frozen_spatial_allocation()["joint"]
    assert report.grid_rich_tasks == pytest.approx(50.0)
    assert report.water_rich_tasks == pytest.approx(50.0)
    assert report.grid_rich_energy == pytest.approx(40.0)
    assert report.grid_rich_water == pytest.approx(15.0)
    assert report.water_rich_energy == pytest.approx(40.0)
    assert report.water_rich_water == pytest.approx(15.0)
    assert report.jointly_viable is True
