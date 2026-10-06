import pytest

from market_microcosm.dcre053_joint_resource_observability import (
    dcre053_joint_resource_observability_report,
)


def test_2024_assured_dc_energy_and_water_values_are_retained() -> None:
    report = dcre053_joint_resource_observability_report()
    obs = report["observation"]
    assert obs.year == 2024
    assert obs.data_center_electricity_mwh == 30_825_600.0
    assert obs.data_center_water_consumption_million_gallons == 7_787.0
    assert obs.electricity_third_party_assured is True
    assert obs.water_third_party_assured is True


def test_conditional_aggregate_ratio_is_reproducible() -> None:
    report = dcre053_joint_resource_observability_report()
    assert report["conditional_aggregate_gallons_per_kwh"] == pytest.approx(
        0.25261470985155193
    )
    assert report["conditional_aggregate_liters_per_kwh"] == pytest.approx(
        0.9562506994838056
    )


def test_scope_identity_failure_blocks_wue_and_substitution_promotion() -> None:
    report = dcre053_joint_resource_observability_report()
    obs = report["observation"]
    assert obs.metric_scope_identity_certified is False
    assert report["derived_ratio_status"] == "CONDITIONAL_DESCRIPTIVE_RATIO_ONLY"
    assert report["promoted_wue_liters_per_kwh"] is None
    assert report["candidate_energy_water_substitution_coefficient"] is None
    assert report["causal_cooling_tradeoff_identified"] is False


def test_joint_resource_observation_does_not_upgrade_authority() -> None:
    report = dcre053_joint_resource_observability_report()
    assert report["authority_effect"] == "NONE"
