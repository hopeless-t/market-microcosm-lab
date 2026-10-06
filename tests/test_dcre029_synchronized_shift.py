import pytest

from market_microcosm.dcre029_synchronized_shift import (
    coordinated_symmetric_outcome,
    independent_herd_outcome,
)


def test_each_actor_independently_sees_offpeak_shift_as_safe() -> None:
    shifts, _ = independent_herd_outcome()
    assert shifts == pytest.approx((20.0, 20.0))


def test_independent_safe_shifts_jointly_create_offpeak_water_peak() -> None:
    _, report = independent_herd_outcome()
    assert report.offpeak_tasks == pytest.approx(60.0)
    assert report.offpeak_water == pytest.approx(24.0)
    assert report.jointly_viable is False


def test_coordinated_split_uses_shared_headroom_once() -> None:
    shifts, report = coordinated_symmetric_outcome()
    assert shifts == pytest.approx((15.0, 15.0))
    assert report.flexible_peak_tasks == pytest.approx(10.0)
    assert report.offpeak_tasks == pytest.approx(50.0)
    assert report.offpeak_water == pytest.approx(20.0)
    assert report.peak_energy == pytest.approx(64.0)
    assert report.jointly_viable is True
