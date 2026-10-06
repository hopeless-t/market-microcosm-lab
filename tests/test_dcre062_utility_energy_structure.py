import pytest

from market_microcosm.dcre062_utility_energy_structure import (
    dcre062_utility_energy_structure_report,
)


def test_eia_2024_sector_sales_sum_to_utility_total() -> None:
    report = dcre062_utility_energy_structure_report()
    structure = report["structure"]
    assert structure.total_mwh == 1_530_602.0
    assert structure.industrial_mwh == 1_263_389.0
    assert structure.commercial_mwh == 121_887.0
    assert structure.residential_mwh == 145_326.0
    assert structure.industrial_customers == 190
    assert report["sector_sum_matches_total"] is True


def test_industrial_sector_is_large_but_not_retyped_as_data_center_load() -> None:
    report = dcre062_utility_energy_structure_report()
    assert report["industrial_share"] == pytest.approx(1_263_389.0 / 1_530_602.0)
    assert report["industrial_share"] > 0.82
    assert report["industrial_majority_of_sales"] is True
    assert report["industrial_equals_data_center"] is False
    assert report["exact_data_center_share"] is None


def test_eia_energy_volume_strengthens_system_level_observation_only() -> None:
    report = dcre062_utility_energy_structure_report()
    assert report["utility_total_exceeds_one_twh"] is True
    assert report["independent_system_energy_crosscheck"] is True
    assert report["customer_specific_causality_identified"] is False
    assert report["authority_effect"] == "NONE"
