from market_microcosm.dcre043_empirical_boundary import (
    FORECAST,
    OBSERVED,
    calibration_contract,
    empirical_anchors,
    unknown_structural_parameters,
)


def test_empirical_sources_are_typed_observed_or_forecast() -> None:
    anchors = empirical_anchors()
    assert anchors
    assert {row.evidence_class for row in anchors} == {OBSERVED, FORECAST}
    assert all(row.source_url.startswith("https://") for row in anchors)


def test_google_efficiency_and_growth_are_separate_observations_not_eta() -> None:
    rows = {row.key: row for row in empirical_anchors()}
    assert rows["google_dc_electricity_growth_2024_yoy"].values == (27.0,)
    assert rows["google_compute_per_electricity_5y_lower_bound"].values == (6.0,)
    assert "causal_demand_elasticity_eta" in unknown_structural_parameters()


def test_lbl_range_remains_forecast_envelope() -> None:
    rows = {row.key: row for row in empirical_anchors()}
    lbl = rows["lbl_us_data_center_electricity_share_2030"]
    assert lbl.evidence_class == FORECAST
    assert lbl.values == (9.5, 11.8, 15.3)


def test_contract_forbids_automatic_synthetic_parameter_calibration() -> None:
    contract = calibration_contract()
    assert contract["automatic_synthetic_parameter_writes"] == ()
    assert "infer_causal_elasticity_from_company_efficiency_and_growth" in contract["forbidden_uses"]
    assert "scenario_envelope_stress_tests" in contract["allowed_uses"]
