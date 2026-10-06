from market_microcosm.dcre059_institutional_mechanism_map import (
    dcre059_institutional_mechanism_map,
)


def test_multiple_real_governance_mechanisms_are_observed() -> None:
    report = dcre059_institutional_mechanism_map()
    assert report["mechanisms_exist"] is True
    assert report["observed_mechanism_count"] >= 7
    assert all(row.maps_to_market_failure for row in report["mechanisms"])


def test_mechanism_observation_does_not_identify_effectiveness() -> None:
    report = dcre059_institutional_mechanism_map()
    assert report["causal_effectiveness_identified"] is False
    assert report["counterfactual_without_mechanisms_observed"] is False
    assert report["policy_recommendation_authorized"] is False


def test_institutional_map_does_not_upgrade_authority() -> None:
    assert dcre059_institutional_mechanism_map()["authority_effect"] == "NONE"
