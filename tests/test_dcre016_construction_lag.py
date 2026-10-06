import pytest

from market_microcosm.dcre016_construction_lag import frozen_construction_lag


def test_full_reactive_policy_oscillates_out_of_phase() -> None:
    report = frozen_construction_lag()["full_reactive"]
    capacities = tuple(row.capacity for row in report.periods)
    assert capacities == pytest.approx((100.0, 100.0, 180.0, 100.0, 180.0, 100.0))
    assert report.total_mismatch == pytest.approx(400.0)
    assert report.capacity_movement == pytest.approx(320.0)


def test_damped_response_reduces_mismatch_and_capacity_churn() -> None:
    reports = frozen_construction_lag()
    full = reports["full_reactive"]
    damped = reports["damped_half"]
    assert damped.total_mismatch == pytest.approx(285.0)
    assert damped.capacity_movement == pytest.approx(115.0)
    assert damped.total_mismatch < full.total_mismatch
    assert damped.capacity_movement < full.capacity_movement


def test_damping_is_not_claimed_as_optimal() -> None:
    damped = frozen_construction_lag()["damped_half"]
    assert damped.total_unmet == pytest.approx(195.0)
    assert damped.total_idle == pytest.approx(90.0)
    assert damped.total_unmet > 0.0
