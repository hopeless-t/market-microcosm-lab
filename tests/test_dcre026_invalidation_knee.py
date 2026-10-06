import pytest

from market_microcosm.dcre026_invalidation_knee import frozen_invalidation_sweep


def test_three_use_invalidation_knee_is_fifteen_percent() -> None:
    report = frozen_invalidation_sweep()
    assert report["knee_3"] == pytest.approx(0.15)
    low = report["uses_3_q_010"]
    high = report["uses_3_q_020"]
    assert low.raw_expected_cost == pytest.approx(75.0)
    assert low.prepared_expected_cost == pytest.approx(72.0)
    assert low.prepared_wins is True
    assert high.prepared_expected_cost == pytest.approx(78.0)
    assert high.prepared_wins is False


def test_eight_use_invalidation_knee_is_about_thirty_five_percent() -> None:
    report = frozen_invalidation_sweep()
    assert report["knee_8"] == pytest.approx(74.0 / 210.0)
    low = report["uses_8_q_030"]
    high = report["uses_8_q_040"]
    assert low.raw_expected_cost == pytest.approx(200.0)
    assert low.prepared_expected_cost == pytest.approx(189.0)
    assert low.prepared_wins is True
    assert high.prepared_expected_cost == pytest.approx(210.0)
    assert high.prepared_wins is False


def test_more_reuse_tolerates_more_invalidation_on_frozen_surface() -> None:
    report = frozen_invalidation_sweep()
    assert report["knee_8"] > report["knee_3"]
