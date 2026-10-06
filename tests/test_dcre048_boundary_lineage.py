from market_microcosm.dcre048_boundary_lineage import dcre048_boundary_lineage_audit


def test_visible_total_electricity_overlaps_are_numerically_stable() -> None:
    report = dcre048_boundary_lineage_audit()
    audit = report["audit"]
    assert audit.compared_years == (2019, 2020, 2021, 2022, 2023)
    assert audit.overlap_values_equal is True
    assert report["visible_total_electricity_lineage_status"] == "OVERLAP_STABLE"


def test_recalculation_policy_prevents_overclaiming_from_overlap_stability() -> None:
    report = dcre048_boundary_lineage_audit()
    audit = report["audit"]
    assert audit.recalculation_policy_exists is True
    assert audit.energy_metric_recalculations_disclosed is True
    assert audit.current_report_restates_2019_total_electricity is False
    assert audit.full_lineage_closed is False


def test_missing_2019_dc_denominator_and_compute_definition_keep_bound_conditional() -> None:
    report = dcre048_boundary_lineage_audit()
    audit = report["audit"]
    assert audit.data_center_2019_electricity_disclosed is False
    assert audit.compute_metric_definition_public is False
    assert report["full_cross_report_lineage_status"] == "OPEN"
    assert report["promote_dcre047_bound"] is False
    assert report["candidate_eta"] is None
    assert report["authority_effect"] == "NONE"
