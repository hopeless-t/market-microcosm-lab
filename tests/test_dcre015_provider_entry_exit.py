import pytest

from market_microcosm.dcre015_provider_entry_exit import frozen_entry_exit


def test_low_prices_keep_supply_but_break_resource_viability() -> None:
    report = frozen_entry_exit()["low_price"]
    assert report.active_providers == ("SCALE", "LOCAL", "WET")
    assert report.total_capacity == pytest.approx(165.0)
    assert report.total_energy == pytest.approx(123.0)
    assert report.total_water == pytest.approx(43.3)
    assert report.service_viable is True
    assert report.jointly_viable is False


def test_joint_scarcity_prices_can_trigger_service_exit() -> None:
    report = frozen_entry_exit()["scarcity_price"]
    assert report.active_providers == ("SCALE",)
    assert report.total_capacity == pytest.approx(70.0)
    assert report.energy_viable is True
    assert report.water_viable is True
    assert report.service_viable is False


def test_targeted_service_credit_restores_frozen_joint_viability() -> None:
    report = frozen_entry_exit()["scarcity_plus_service_credit"]
    assert report.active_providers == ("SCALE", "LOCAL")
    assert report.total_capacity == pytest.approx(105.0)
    assert report.total_energy == pytest.approx(84.0)
    assert report.total_water == pytest.approx(13.3)
    assert report.public_credit_cost == pytest.approx(3.0)
    assert report.jointly_viable is True


def test_resource_viability_and_service_viability_are_distinct() -> None:
    reports = frozen_entry_exit()
    assert reports["scarcity_price"].energy_viable is True
    assert reports["scarcity_price"].water_viable is True
    assert reports["scarcity_price"].service_viable is False
