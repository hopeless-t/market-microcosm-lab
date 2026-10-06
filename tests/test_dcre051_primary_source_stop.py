from market_microcosm.dcre051_primary_source_stop import (
    dcre051_primary_source_stop_audit,
)


def test_fy2019_total_electricity_is_third_party_assured() -> None:
    report = dcre051_primary_source_stop_audit()
    historical = report["historical_endpoint"]
    assert historical.year == 2019
    assert historical.total_electricity_mwh == 12_237_198.0
    assert historical.third_party_assured is True
    assert report["audit"].historical_total_assured is True


def test_fy2024_data_center_electricity_is_present_in_assurance_schedule() -> None:
    report = dcre051_primary_source_stop_audit()
    current = report["current_endpoint"]
    assert current.year == 2024
    assert current.data_center_electricity_mwh == 30_825_600.0
    assert current.total_electricity_mwh == 32_179_900.0
    assert current.third_party_assured is True
    assert report["audit"].current_data_center_value_assured is True


def test_exact_2019_data_center_split_remains_unobserved() -> None:
    report = dcre051_primary_source_stop_audit()
    audit = report["audit"]
    assert audit.historical_data_center_exact_observed is False
    assert report["exact_2019_dc_denominator_status"] == (
        "PUBLICLY_UNOBSERVED_IN_CHECKED_PRIMARY_SOURCES"
    )
    assert report["promoted_2019_dc_mwh"] is None


def test_boundary_lineage_is_not_certified_by_assurance_alone() -> None:
    report = dcre051_primary_source_stop_audit()
    audit = report["audit"]
    assert audit.boundary_wording_identical is False
    assert audit.cross_boundary_subset_certified is False
    assert report["promoted_dcre047_bound"] is None
    assert report["candidate_eta"] is None


def test_primary_source_search_has_a_stop_rule_and_pivots() -> None:
    report = dcre051_primary_source_stop_audit()
    audit = report["audit"]
    assert len(audit.checked_surfaces) == 4
    assert audit.stop_condition_met is True
    assert report["next_action"] == "PIVOT_FROM_DENOMINATOR_SEARCH"
    assert report["authority_effect"] == "NONE"
