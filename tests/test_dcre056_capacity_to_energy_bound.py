import pytest

from market_microcosm.dcre056_capacity_to_energy_bound import (
    annual_energy_upper_bound_mwh,
    dcre056_capacity_to_energy_bound_report,
)


def test_capacity_to_energy_upper_bound_theorem_is_exact() -> None:
    assert annual_energy_upper_bound_mwh(capacity_mw=277.0) == pytest.approx(
        277.0 * 8760.0
    )


def test_utility_load_does_not_certify_google_site_capacity() -> None:
    report = dcre056_capacity_to_energy_bound_report()
    cert = report["certificate"]
    assert cert.capacity_positive is True
    assert cert.capacity_customer_specific is False
    assert cert.capacity_site_specific is False
    assert cert.capacity_population_matches_target is False
    assert cert.capacity_is_peak_power_not_energy is True
    assert cert.certified is False


def test_uncertified_capacity_bound_is_not_promoted() -> None:
    report = dcre056_capacity_to_energy_bound_report()
    assert report["mathematical_annual_energy_upper_bound_mwh"] == pytest.approx(
        2_426_520.0
    )
    assert report["promoted_google_site_annual_energy_upper_bound_mwh"] is None
    assert report["google_site_capacity_mw"] is None
    assert report["google_site_annual_energy_mwh"] is None


def test_capacity_bound_audit_does_not_upgrade_authority() -> None:
    assert dcre056_capacity_to_energy_bound_report()["authority_effect"] == "NONE"
