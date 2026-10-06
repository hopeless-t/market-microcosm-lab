import pytest

from market_microcosm.dcre049_subset_bound import dcre049_subset_bound_report


def test_conditional_math_matches_dcre047_when_certificate_is_ignored() -> None:
    report = dcre049_subset_bound_report()
    assert report["conditional_bound"] == pytest.approx(
        6.0 * 30_825_600.0 / 12_237_200.0
    )
    assert report["conditional_bound"] > 15.0


def test_empirical_certificate_is_not_yet_satisfied() -> None:
    report = dcre049_subset_bound_report()
    cert = report["certificate"]
    assert cert.current_target_positive is True
    assert cert.historical_superset_positive is True
    assert cert.historical_target_subset_of_superset_certified is False
    assert cert.current_and_historical_target_same_population is False
    assert cert.activity_metric_endpoint_comparable is False
    assert cert.certified is False
    assert report["promoted_bound"] is None
    assert report["candidate_eta"] is None


def test_boundary_counterexample_can_make_naive_lower_bound_too_large() -> None:
    counterexample = dcre049_subset_bound_report()["counterexample"]
    assert counterexample["true_historical_target"] > counterexample["reported_historical_superset"]
    assert counterexample["naive_bound"] == pytest.approx(5.0)
    assert counterexample["true_growth"] == pytest.approx(60.0 / 14.0)
    assert counterexample["bound_invalid"] is True


def test_no_authority_upgrade_from_mathematical_theorem_alone() -> None:
    report = dcre049_subset_bound_report()
    assert report["authority_effect"] == "NONE"
