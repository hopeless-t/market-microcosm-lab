import pytest

from market_microcosm.dcre031_response_diversity import frozen_cadence_comparison


def test_staggered_cadence_reduces_peak_load() -> None:
    report = frozen_cadence_comparison()
    assert report["synchronized_metrics"]["peak_load"] == pytest.approx(80.0)
    assert report["staggered_metrics"]["peak_load"] == pytest.approx(70.0)


def test_staggered_cadence_reduces_aggregate_movement() -> None:
    report = frozen_cadence_comparison()
    assert report["synchronized_metrics"]["flexible_movement"] == pytest.approx(200.0)
    assert report["staggered_metrics"]["flexible_movement"] == pytest.approx(60.0)


def test_diversity_damps_but_does_not_eliminate_cycle() -> None:
    report = frozen_cadence_comparison()["staggered"]
    assert tuple(row.flexible_a for row in report) == pytest.approx(
        (10.0, 20.0, 30.0, 10.0, 20.0, 30.0)
    )
    assert len(set(row.load_a for row in report)) == 3
