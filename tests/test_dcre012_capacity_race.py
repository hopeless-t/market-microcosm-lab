import pytest

from market_microcosm.dcre012_capacity_race import frozen_capacity_race


def test_efficiency_savings_can_be_reabsorbed_by_capacity_expansion() -> None:
    report = frozen_capacity_race()
    no_reinvestment = report["no_reinvestment"]
    reinvestment = report["resource_reinvestment"]
    assert no_reinvestment.resource_used == pytest.approx(60.0)
    assert reinvestment.resource_used == pytest.approx(100.0)


def test_resource_ceiling_reinvestment_reaches_full_rebound() -> None:
    report = frozen_capacity_race()
    reinvestment = report["resource_reinvestment"]
    assert reinvestment.capacity == pytest.approx(166.66666666666669)
    assert reinvestment.resource_used == pytest.approx(100.0)


def test_verification_aware_capacity_matches_verified_output_with_less_resource() -> None:
    report = frozen_capacity_race()
    reinvestment = report["resource_reinvestment"]
    verified = report["verification_aware"]
    assert reinvestment.verified_output == pytest.approx(120.0)
    assert verified.verified_output == pytest.approx(120.0)
    assert reinvestment.resource_used == pytest.approx(100.0)
    assert verified.resource_used == pytest.approx(72.0)
    assert report["resource_waste_fraction"] == pytest.approx(0.28)


def test_induced_demand_exceeds_all_frozen_capacity_arms() -> None:
    report = frozen_capacity_race()
    no_reinvestment = report["no_reinvestment"]
    assert no_reinvestment.demand == pytest.approx(215.1657414559676)
    assert no_reinvestment.demand > report["resource_reinvestment"].capacity
