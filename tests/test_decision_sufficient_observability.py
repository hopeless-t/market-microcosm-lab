from market_microcosm.decision_sufficient_observability import (
    decision_sufficiency_reference,
    decision_sufficient_observability_report_payload,
)


def test_rounding_yields_state_interval_not_point() -> None:
    row = decision_sufficiency_reference()

    assert row["newest_mrr_interval_with_exact_boundary"] == [1.5, 2.5]
    assert row["newest_mrr_interval_with_rounded_boundary"] == [1.0, 3.0]


def test_coarse_activity_predicate_is_still_certified() -> None:
    row = decision_sufficiency_reference()

    assert row["predicates"]["active_gt_0"]["exact_boundary"] == (
        "CERTIFIED_TRUE"
    )
    assert row["predicates"]["active_gt_0"]["rounded_boundary"] == (
        "CERTIFIED_TRUE"
    )


def test_finer_threshold_remains_ambiguous() -> None:
    row = decision_sufficiency_reference()

    assert row["predicates"]["at_least_2"]["exact_boundary"] == "AMBIGUOUS"
    assert row["predicates"]["at_least_2"]["rounded_boundary"] == "AMBIGUOUS"


def test_e043_promotion_contract() -> None:
    payload = decision_sufficient_observability_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_observability_rule"] == (
        "observability-authority-is-decision-predicate-scoped-v1"
    )
