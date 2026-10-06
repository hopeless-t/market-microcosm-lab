import pytest

from market_microcosm.dcre023_network_locality import frozen_network_locality


def test_resource_only_spatial_solution_can_break_network_ceiling() -> None:
    report = frozen_network_locality()["resource_only_projection"]
    assert report is not None
    assert report.resource_viable is True
    assert report.remote_tasks == pytest.approx(50.0)
    assert report.total_network == pytest.approx(25.0)
    assert report.network_viable is False
    assert report.jointly_viable is False


def test_raw_transfer_has_no_jointly_viable_point_on_frozen_grid() -> None:
    assert frozen_network_locality()["raw_network_exact"] is None


def test_compact_transfer_restores_joint_viability() -> None:
    report = frozen_network_locality()["compact_network_exact"]
    assert report is not None
    assert report.grid_rich_tasks == pytest.approx(50.0)
    assert report.remote_tasks == pytest.approx(50.0)
    assert report.total_network == pytest.approx(15.0)
    assert report.jointly_viable is True
