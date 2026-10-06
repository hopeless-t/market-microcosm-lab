import pytest

from market_microcosm.dcre041_backlog_portfolio import frozen_backlog_portfolio


def test_fifo_spends_recovery_capacity_on_zero_delay_loss_bulk() -> None:
    report = frozen_backlog_portfolio()
    assert report["fifo_names"] == ("BULK",)
    assert report["fifo_preserved_value"] == 48


def test_e018_projection_selects_urgent_and_flex_backlog() -> None:
    report = frozen_backlog_portfolio()
    assert report["dp_matches_oracle"] is True
    assert report["dp"].selected_names == ("FLEX", "URGENT")
    assert report["dp"].total_cost_units == 20
    assert report["dp"].total_restoration_value == 32
    assert report["dp_preserved_value"] == 80


def test_backlog_reduction_volume_is_not_value_preservation() -> None:
    report = frozen_backlog_portfolio()
    assert report["dp_preserved_value"] > report["fifo_preserved_value"]
    assert report["dp_preserved_value"] - report["fifo_preserved_value"] == 32
