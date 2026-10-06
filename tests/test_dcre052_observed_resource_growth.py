import pytest

from market_microcosm.dcre052_observed_resource_growth import (
    dcre052_observed_resource_growth_report,
)


def test_observed_data_center_electricity_more_than_doubled_2020_to_2024() -> None:
    report = dcre052_observed_resource_growth_report()
    growth = report["growth"]
    assert growth.start_mwh == 14_426_600.0
    assert growth.end_mwh == 30_825_600.0
    assert growth.growth_ratio == pytest.approx(30_825_600.0 / 14_426_600.0)
    assert growth.growth_ratio > 2.0
    assert growth.cagr == pytest.approx(0.20902947041822806)


def test_fleet_pue_did_not_worsen_over_same_calendar_window() -> None:
    report = dcre052_observed_resource_growth_report()
    context = report["efficiency_context"]
    assert context.pue_by_year == {
        2020: 1.10,
        2021: 1.10,
        2022: 1.10,
        2023: 1.10,
        2024: 1.09,
    }
    assert context.pue_non_worsening is True


def test_scope_mismatch_blocks_it_energy_decomposition_and_causal_rebound() -> None:
    report = dcre052_observed_resource_growth_report()
    context = report["efficiency_context"]
    assert context.scope_identity_certified is False
    assert report["derived_it_energy_series"] is None
    assert report["causal_rebound_identified"] is False
    assert report["candidate_eta"] is None


def test_observation_is_promoted_only_as_consistency_statement() -> None:
    report = dcre052_observed_resource_growth_report()
    assert report["observed_consistency_statement"] == (
        "TOTAL_DC_ELECTRICITY_MORE_THAN_DOUBLED_WHILE_FLEET_PUE_DID_NOT_WORSEN"
    )
    assert report["authority_effect"] == "NONE"
