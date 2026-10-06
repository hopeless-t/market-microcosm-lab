from market_microcosm.dcre050_exact_denominator import dcre050_exact_denominator_audit


def test_2019_is_visible_in_chart_but_absent_from_numeric_table() -> None:
    report = dcre050_exact_denominator_audit()
    surface = report["surface"]
    assert 2019 in surface.chart_years
    assert 2019 not in surface.table_years
    assert surface.chart_has_exact_numeric_labels is False
    assert surface.exact_2019_denominator_observed is False


def test_known_table_series_begins_in_2020() -> None:
    report = dcre050_exact_denominator_audit()
    assert report["known_table_values_mwh"][2020] == 14_426_600.0
    assert report["known_table_values_mwh"][2024] == 30_825_600.0
    assert tuple(report["known_table_values_mwh"]) == (2020, 2021, 2022, 2023, 2024)


def test_chart_digitization_is_not_used_to_invent_exact_2019_value() -> None:
    report = dcre050_exact_denominator_audit()
    surface = report["surface"]
    assert surface.chart_digitization_authorized is False
    assert report["exact_2019_dc_denominator_status"] == "UNOBSERVED"
    assert report["promoted_2019_dc_mwh"] is None
    assert report["promoted_dcre047_bound"] is None
    assert report["candidate_eta"] is None
    assert report["authority_effect"] == "NONE"
