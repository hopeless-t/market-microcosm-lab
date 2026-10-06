import pytest

from market_microcosm.dcre021_telemetry_value import frozen_telemetry_value


def test_break_even_accuracy_is_three_quarters() -> None:
    report = frozen_telemetry_value()
    assert report["break_even_accuracy"] == pytest.approx(0.75)


def test_low_quality_telemetry_is_worse_than_safe_always_on() -> None:
    report = frozen_telemetry_value()
    always = report["always_on"]
    low = report["telemetry_060"]
    assert always.expected_loss == pytest.approx(30.0)
    assert low.expected_activation_resource == pytest.approx(15.0)
    assert low.expected_unmet_demand == pytest.approx(12.0)
    assert low.expected_loss == pytest.approx(39.0)
    assert low.expected_loss > always.expected_loss


def test_high_quality_telemetry_crosses_value_knee() -> None:
    report = frozen_telemetry_value()
    always = report["always_on"]
    high = report["telemetry_080"]
    assert high.expected_activation_resource == pytest.approx(15.0)
    assert high.expected_unmet_demand == pytest.approx(6.0)
    assert high.expected_idle_capacity == pytest.approx(6.0)
    assert high.expected_loss == pytest.approx(27.0)
    assert high.expected_loss < always.expected_loss
