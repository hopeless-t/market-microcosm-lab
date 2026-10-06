import pytest

from market_microcosm.dcre014_resource_substitution import frozen_resource_substitution


def test_energy_only_choice_displaces_pressure_into_water() -> None:
    report = frozen_resource_substitution()
    energy = report["energy_only"]
    assert energy.technology.name == "WET"
    assert energy.total_energy == pytest.approx(84.0)
    assert energy.total_water == pytest.approx(60.0)
    assert energy.energy_viable is True
    assert energy.water_viable is False


def test_water_only_choice_displaces_pressure_into_energy() -> None:
    report = frozen_resource_substitution()
    water = report["water_only"]
    assert water.technology.name == "DRY"
    assert water.total_energy == pytest.approx(120.0)
    assert water.total_water == pytest.approx(6.0)
    assert water.energy_viable is False
    assert water.water_viable is True


def test_joint_viability_selects_hybrid() -> None:
    report = frozen_resource_substitution()
    joint = report["joint"]
    assert joint.technology.name == "HYBRID"
    assert joint.total_energy == pytest.approx(98.4)
    assert joint.total_water == pytest.approx(24.0)
    assert joint.jointly_viable is True


def test_single_resource_optima_are_not_jointly_viable() -> None:
    report = frozen_resource_substitution()
    assert report["energy_only"].jointly_viable is False
    assert report["water_only"].jointly_viable is False
    assert report["joint"].jointly_viable is True
