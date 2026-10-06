from market_microcosm.dcre057_contract_vs_realized_load import (
    dcre057_contract_vs_realized_load_report,
)


def test_contractual_commitments_are_observed_but_not_quantified() -> None:
    report = dcre057_contract_vs_realized_load_report()
    surface = report["surface"]
    assert surface.minimum_purchase_commitment_exists is True
    assert surface.take_or_pay_exists is True
    assert surface.minimum_purchase_commitment_mw is None
    assert surface.continuous_delivery_hours_per_year == 8760


def test_delivery_availability_does_not_identify_realized_use() -> None:
    report = dcre057_contract_vs_realized_load_report()
    surface = report["surface"]
    assert surface.customer_interval_meter_series_observed is False
    assert surface.realized_load_factor is None
    assert report["contracted_minimum_is_realized_load"] is False
    assert report["delivery_availability_is_energy_used"] is False
    assert report["realized_load_factor_identified"] is False


def test_contract_surface_does_not_create_site_annual_energy() -> None:
    report = dcre057_contract_vs_realized_load_report()
    assert report["google_the_dalles_annual_mwh"] is None
    assert report["authority_effect"] == "NONE"
