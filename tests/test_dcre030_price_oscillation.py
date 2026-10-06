import pytest

from market_microcosm.dcre030_price_oscillation import frozen_price_response


def test_full_lagged_price_response_alternates_between_periods() -> None:
    report = frozen_price_response()["full"]
    assert tuple(row.flexible_a for row in report) == pytest.approx(
        (0.0, 40.0, 0.0, 40.0, 0.0, 40.0)
    )
    assert tuple(row.load_a for row in report) == pytest.approx(
        (40.0, 80.0, 40.0, 80.0, 40.0, 80.0)
    )
    assert tuple(row.load_b for row in report) == pytest.approx(
        (80.0, 40.0, 80.0, 40.0, 80.0, 40.0)
    )


def test_partial_response_reduces_peak_and_movement() -> None:
    report = frozen_price_response()
    assert report["full_metrics"]["peak_load"] == pytest.approx(80.0)
    assert report["damped_metrics"]["peak_load"] == pytest.approx(70.0)
    assert report["full_metrics"]["flexible_movement"] == pytest.approx(200.0)
    assert report["damped_metrics"]["flexible_movement"] == pytest.approx(100.0)


def test_damped_response_still_oscillates_in_frozen_world() -> None:
    report = frozen_price_response()["damped"]
    assert tuple(row.flexible_a for row in report) == pytest.approx(
        (10.0, 30.0, 10.0, 30.0, 10.0, 30.0)
    )
