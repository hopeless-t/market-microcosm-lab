import pytest

from market_microcosm.dcre019_withholding import frozen_withholding


def test_unconstrained_right_holder_prefers_partial_withholding() -> None:
    report = frozen_withholding()["unconstrained"]
    assert report.deploy == pytest.approx(40.0)
    assert report.withheld == pytest.approx(20.0)
    assert report.unmet_demand == pytest.approx(20.0)
    assert report.market_price == pytest.approx(1.6)
    assert report.net_revenue == pytest.approx(64.0)


def test_full_deployment_has_lower_revenue_without_obligation() -> None:
    report = frozen_withholding()["unconstrained"]
    assert report.net_revenue > 60.0


def test_use_or_lose_penalty_restores_full_deployment_in_frozen_world() -> None:
    report = frozen_withholding()["use_or_lose"]
    assert report.deploy == pytest.approx(60.0)
    assert report.withheld == pytest.approx(0.0)
    assert report.unmet_demand == pytest.approx(0.0)
    assert report.net_revenue == pytest.approx(60.0)
