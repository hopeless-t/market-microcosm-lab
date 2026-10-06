from market_microcosm.dcre060_mechanism_outcome_cooccurrence import (
    dcre060_mechanism_outcome_cooccurrence_report,
)


def test_mechanism_bundle_and_favorable_outcome_claims_coexist() -> None:
    report = dcre060_mechanism_outcome_cooccurrence_report()
    assert report["mechanism_bundle_observed"] is True
    assert report["favorable_outcome_claims_coexist"] is True
    assert all(claim.source_reported for claim in report["outcome_claims"])


def test_cooccurrence_does_not_identify_causal_effectiveness() -> None:
    report = dcre060_mechanism_outcome_cooccurrence_report()
    assert report["all_outcomes_independently_verified"] is False
    assert report["counterfactual_observed"] is False
    assert report["mechanism_caused_favorable_outcomes"] is None
    assert report["causal_effectiveness_identified"] is False


def test_outcome_cooccurrence_audit_does_not_upgrade_authority() -> None:
    assert dcre060_mechanism_outcome_cooccurrence_report()["authority_effect"] == "NONE"
