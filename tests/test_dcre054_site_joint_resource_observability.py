from market_microcosm.dcre054_site_joint_resource_observability import (
    dcre054_site_joint_resource_report,
)


def test_official_surface_overlap_exists_for_multiple_named_locations() -> None:
    report = dcre054_site_joint_resource_report()
    assert report["water_location_series_observed"] is True
    assert report["campus_pue_series_observed"] is True
    assert report["matched_site_count"] >= 4
    assert all(surface.pue_observed for surface in report["surfaces"])
    assert all(
        surface.water_consumption_million_gallons_2024 >= 0.0
        for surface in report["surfaces"]
    )


def test_missing_absolute_site_electricity_blocks_site_wue() -> None:
    report = dcre054_site_joint_resource_report()
    assert report["site_absolute_electricity_series_observed"] is False
    assert report["missing_variable"] == "SITE_ABSOLUTE_ELECTRICITY_MWH"
    assert all(
        surface.site_electricity_mwh_2024 is None
        for surface in report["surfaces"]
    )
    assert report["identified_site_wue_count"] == 0


def test_pue_cannot_substitute_for_absolute_electricity_volume() -> None:
    report = dcre054_site_joint_resource_report()
    assert all(surface.site_wue_identified is False for surface in report["surfaces"])
    assert report["site_energy_water_substitution_identified"] is False


def test_site_observability_audit_does_not_upgrade_authority() -> None:
    report = dcre054_site_joint_resource_report()
    assert report["authority_effect"] == "NONE"
