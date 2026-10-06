import pytest

from market_microcosm.dcre047_partial_identification import (
    dcre047_partial_identification_report,
)


def test_conditional_electricity_ratio_lower_bound_uses_total_as_upper_bound() -> None:
    report = dcre047_partial_identification_report()
    bound = report["conditional_bound"]
    assert bound.electricity_ratio_lower_bound == pytest.approx(
        30_825_600.0 / 12_237_200.0
    )
    assert bound.electricity_ratio_lower_bound > 2.5


def test_conditional_compute_growth_bound_exceeds_fifteen_x() -> None:
    report = dcre047_partial_identification_report()
    bound = report["conditional_bound"]
    assert bound.compute_growth_lower_bound == pytest.approx(
        6.0 * 30_825_600.0 / 12_237_200.0
    )
    assert bound.compute_growth_lower_bound > 15.0


def test_unverified_cross_report_assumptions_block_promotion() -> None:
    report = dcre047_partial_identification_report()
    bound = report["conditional_bound"]
    assert bound.endpoint_year_alignment is True
    assert bound.assumptions_verified is False
    assert report["promoted_compute_growth_lower_bound"] is None
    assert report["candidate_eta"] is None
    assert set(report["blocking_assumptions"]) == {
        "DENOMINATOR_SCOPE_EQUIVALENCE",
        "REPORTING_BOUNDARY_COMPATIBILITY",
        "COMPUTE_METRIC_STABILITY",
    }


def test_conditional_math_is_retained_without_authority_upgrade() -> None:
    report = dcre047_partial_identification_report()
    assert report["strict_conditional_statement"].startswith(
        "compute_2024/compute_2019 > 15."
    )
    assert report["authority_effect"] == "NONE"
