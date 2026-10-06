import pytest

from market_microcosm.dcre018_capacity_rights import frozen_capacity_rights


def test_no_rights_reproduces_duplicated_investment() -> None:
    report = frozen_capacity_rights()["none"]
    assert report.future_capacity == pytest.approx(220.0)
    assert report.idle_capacity == pytest.approx(60.0)
    assert report.construction_resource == pytest.approx(60.0)


def test_winner_take_all_rights_remove_overbuild_but_concentrate_investment() -> None:
    report = frozen_capacity_rights()["winner_take_all"]
    assert report.future_capacity == pytest.approx(160.0)
    assert report.idle_capacity == pytest.approx(0.0)
    assert report.investment_hhi == pytest.approx(1.0)
    assert report.construction_resource == pytest.approx(30.0)


def test_split_rights_remove_overbuild_with_lower_concentration() -> None:
    report = frozen_capacity_rights()["split"]
    assert report.future_capacity == pytest.approx(160.0)
    assert report.idle_capacity == pytest.approx(0.0)
    assert report.investment_hhi == pytest.approx(0.5)
    assert report.construction_resource == pytest.approx(30.0)


def test_capacity_rights_solve_quantity_not_market_structure() -> None:
    reports = frozen_capacity_rights()
    winner = reports["winner_take_all"]
    split = reports["split"]
    assert winner.future_capacity == split.future_capacity
    assert winner.investment_hhi > split.investment_hhi
