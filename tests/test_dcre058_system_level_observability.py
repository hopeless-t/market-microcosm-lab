import pytest

from market_microcosm.dcre058_system_level_observability import (
    dcre058_system_level_observability_report,
)


def test_nwcpud_load_growth_more_than_tripled() -> None:
    report = dcre058_system_level_observability_report()
    obs = report["observation"]
    assert obs.start_mw == 90.0
    assert obs.end_mw == 277.0
    assert obs.growth_ratio == pytest.approx(277.0 / 90.0)
    assert report["utility_load_more_than_tripled"] is True


def test_data_center_attribution_stays_qualitative() -> None:
    report = dcre058_system_level_observability_report()
    obs = report["observation"]
    assert obs.data_centers_reported_as_substantial_driver is True
    assert report["source_attribution_level"] == "QUALITATIVE_SUBSTANTIAL_DRIVER"
    assert report["exact_data_center_share"] is None
    assert report["customer_specific_causality_identified"] is False


def test_system_level_planning_pressure_can_be_promoted_without_customer_mwh() -> None:
    report = dcre058_system_level_observability_report()
    assert report["system_level_planning_pressure_observed"] is True
    assert report["authority_effect"] == "NONE"
