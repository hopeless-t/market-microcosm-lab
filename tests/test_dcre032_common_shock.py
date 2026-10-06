import pytest

from market_microcosm.dcre032_common_shock import frozen_shock_comparison


def test_moderate_shock_activates_only_low_threshold_half() -> None:
    report = frozen_shock_comparison()["moderate"]
    assert report.active_responders == ("T05", "T10")
    assert report.flexible_a == pytest.approx(10.0)
    assert report.peak_load == pytest.approx(70.0)


def test_large_common_shock_collapses_response_diversity() -> None:
    report = frozen_shock_comparison()["large"]
    assert report.active_responders == ("T05", "T10", "T15", "T20")
    assert report.flexible_a == pytest.approx(0.0)
    assert report.load_a == pytest.approx(40.0)
    assert report.load_b == pytest.approx(80.0)
    assert report.peak_load == pytest.approx(80.0)


def test_large_shock_restores_synchronized_peak() -> None:
    report = frozen_shock_comparison()
    assert report["large"].peak_load > report["moderate"].peak_load
