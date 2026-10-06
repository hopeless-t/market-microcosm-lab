import pytest

from market_microcosm.dcre042_recovery_price import frozen_recovery_price_market


def test_low_uniform_recovery_payment_underbuilds() -> None:
    report = frozen_recovery_price_market()["low_payment"]
    assert report["builds"] == pytest.approx((0.0, 0.0))
    assert report["final_capacity"] == pytest.approx(60.0)
    assert report["shortfall"] == pytest.approx(40.0)
    assert report["overshoot"] == pytest.approx(0.0)


def test_high_uniform_recovery_payment_overbuilds_shared_gap() -> None:
    report = frozen_recovery_price_market()["high_payment"]
    assert report["builds"] == pytest.approx((40.0, 40.0))
    assert report["final_capacity"] == pytest.approx(140.0)
    assert report["shortfall"] == pytest.approx(0.0)
    assert report["overshoot"] == pytest.approx(40.0)


def test_coordinated_gap_accounting_hits_target_without_overshoot() -> None:
    report = frozen_recovery_price_market()["coordinated"]
    assert report["builds"] == pytest.approx((20.0, 20.0))
    assert report["final_capacity"] == pytest.approx(100.0)
    assert report["shortfall"] == pytest.approx(0.0)
    assert report["overshoot"] == pytest.approx(0.0)
