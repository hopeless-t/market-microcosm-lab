import pytest

from market_microcosm.dcre061_independent_rate_crosscheck import (
    dcre061_independent_rate_crosscheck_report,
)


def test_eia_independently_verifies_low_residential_rate_outcome() -> None:
    report = dcre061_independent_rate_crosscheck_report()
    obs = report["observation"]
    assert obs.year == 2024
    assert obs.utility_residential_cents_per_kwh == 7.72
    assert obs.state_residential_cents_per_kwh == 14.70
    assert obs.utility_to_state_ratio == pytest.approx(7.72 / 14.70)
    assert obs.percent_below_state == pytest.approx(1.0 - 7.72 / 14.70)
    assert report["utility_rate_below_state_average"] is True
    assert report["independent_low_rate_outcome_verified"] is True


def test_independent_outcome_does_not_identify_governance_causality() -> None:
    report = dcre061_independent_rate_crosscheck_report()
    assert report["mechanism_caused_low_rate"] is None
    assert report["causal_effectiveness_identified"] is False
    assert report["authority_effect"] == "NONE"
