import pytest

from market_microcosm.dcre017_shared_forecast import frozen_shared_forecast


def test_shared_forecast_can_duplicate_market_gap_investment() -> None:
    report = frozen_shared_forecast()["uncoordinated"]
    assert report.provider_investments == pytest.approx((60.0, 60.0))
    assert report.future_capacity == pytest.approx(220.0)
    assert report.idle_capacity == pytest.approx(60.0)
    assert report.unmet_demand == pytest.approx(0.0)
    assert report.construction_resource == pytest.approx(60.0)


def test_coordinated_residual_split_hits_forecast_without_idle_capacity() -> None:
    report = frozen_shared_forecast()["coordinated"]
    assert report.provider_investments == pytest.approx((30.0, 30.0))
    assert report.future_capacity == pytest.approx(160.0)
    assert report.idle_capacity == pytest.approx(0.0)
    assert report.unmet_demand == pytest.approx(0.0)
    assert report.construction_resource == pytest.approx(30.0)


def test_coordination_halves_frozen_construction_resource() -> None:
    reports = frozen_shared_forecast()
    uncoordinated = reports["uncoordinated"]
    coordinated = reports["coordinated"]
    assert coordinated.construction_resource * 2 == pytest.approx(
        uncoordinated.construction_resource
    )
