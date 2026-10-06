import pytest

from market_microcosm.dcre040_backlog_value_decay import frozen_backlog_value_market


def test_low_decay_prefers_pacing_over_burst_purchase() -> None:
    report = frozen_backlog_value_market()
    assert report["low_decay_pace"].net_value == pytest.approx(38.0)
    assert report["low_decay_burst"].net_value == pytest.approx(36.0)
    assert report["low_decay_pace"].net_value > report["low_decay_burst"].net_value


def test_high_decay_prefers_burst_purchase() -> None:
    report = frozen_backlog_value_market()
    assert report["high_decay_pace"].net_value == pytest.approx(34.0)
    assert report["high_decay_burst"].net_value == pytest.approx(36.0)
    assert report["high_decay_burst"].net_value > report["high_decay_pace"].net_value


def test_exact_decay_knee_is_twenty_percent() -> None:
    assert frozen_backlog_value_market()["decay_knee"] == pytest.approx(0.20)
