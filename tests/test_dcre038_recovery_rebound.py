import pytest

from market_microcosm.dcre038_recovery_rebound import (
    frozen_recovery_plans,
    peak_weight_knee,
    scalarized_loss,
)


def test_aggressive_recovery_reduces_service_shortfall_but_doubles_peak() -> None:
    report = frozen_recovery_plans()
    aggressive = report["aggressive"]
    damped = report["damped"]
    assert aggressive.total_shortfall == pytest.approx(60.0)
    assert damped.total_shortfall == pytest.approx(80.0)
    assert aggressive.peak_recovery_resource == pytest.approx(60.0)
    assert damped.peak_recovery_resource == pytest.approx(30.0)
    assert aggressive.total_recovery_resource == pytest.approx(60.0)
    assert damped.total_recovery_resource == pytest.approx(60.0)


def test_aggressive_recovery_creates_second_wave_shortfall() -> None:
    aggressive = frozen_recovery_plans()["aggressive"]
    assert tuple(row.service_shortfall for row in aggressive.epochs) == pytest.approx(
        (40.0, 20.0, 0.0)
    )


def test_exact_peak_resource_weight_knee_is_two_thirds() -> None:
    report = frozen_recovery_plans()
    knee = peak_weight_knee()
    assert knee == pytest.approx(2.0 / 3.0)
    assert scalarized_loss(report["aggressive"], knee) == pytest.approx(
        scalarized_loss(report["damped"], knee)
    )


def test_policy_ranking_flips_around_knee() -> None:
    report = frozen_recovery_plans()
    assert scalarized_loss(report["aggressive"], 0.5) < scalarized_loss(report["damped"], 0.5)
    assert scalarized_loss(report["aggressive"], 1.0) > scalarized_loss(report["damped"], 1.0)
