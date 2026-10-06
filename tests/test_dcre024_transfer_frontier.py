import pytest

from market_microcosm.dcre024_transfer_frontier import (
    frozen_transfer_frontier,
    jointly_viable_modes,
)


def test_raw_preserves_semantics_but_breaks_network_ceiling() -> None:
    report = frozen_transfer_frontier()["RAW"]
    assert report.total_network == pytest.approx(25.0)
    assert report.total_encode_compute == pytest.approx(0.0)
    assert report.preserved_semantic_tasks == pytest.approx(50.0)
    assert report.network_viable is False
    assert report.semantic_viable is True


def test_overcompression_saves_network_but_breaks_semantic_floor() -> None:
    report = frozen_transfer_frontier()["OVERCOMPRESSED"]
    assert report.total_network == pytest.approx(7.5)
    assert report.total_encode_compute == pytest.approx(20.0)
    assert report.preserved_semantic_tasks == pytest.approx(40.0)
    assert report.network_viable is True
    assert report.compute_viable is True
    assert report.semantic_viable is False


def test_heavy_lossless_breaks_encode_compute_ceiling() -> None:
    report = frozen_transfer_frontier()["HEAVY_LOSSLESS"]
    assert report.total_network == pytest.approx(12.5)
    assert report.total_encode_compute == pytest.approx(25.0)
    assert report.preserved_semantic_tasks == pytest.approx(50.0)
    assert report.compute_viable is False


def test_balanced_compaction_is_only_jointly_viable_frozen_mode() -> None:
    report = frozen_transfer_frontier()["COMPACT_BALANCED"]
    assert report.total_network == pytest.approx(15.0)
    assert report.total_encode_compute == pytest.approx(10.0)
    assert report.preserved_semantic_tasks == pytest.approx(47.5)
    assert report.jointly_viable is True
    assert jointly_viable_modes() == ("COMPACT_BALANCED",)
