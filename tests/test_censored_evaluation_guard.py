from market_microcosm.censored_evaluation_guard import (
    censored_evaluation_report_payload,
    coverage_aware_score,
    naive_complete_case_score,
)


def test_complete_case_accuracy_hides_coverage() -> None:
    naive = naive_complete_case_score()
    aware = coverage_aware_score()
    assert naive["numeric_accuracy"] == 1.0
    assert aware["numeric_accuracy_on_observed_labels"] == 1.0
    assert aware["numeric_label_coverage"] == 0.8
    assert aware["informative_withdrawal_cases"] == 2


def test_partial_evaluation_does_not_invent_censored_labels() -> None:
    row = coverage_aware_score()
    assert row["unscored_cases_are_counted_as_errors"] is False
    assert row["unscored_cases_are_counted_as_correct"] is False
    assert row["authority"] == "PARTIAL_EVALUATION_ONLY"


def test_e083_promotion_contract() -> None:
    payload = censored_evaluation_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_evaluation_rule"] == (
        "informatively-censored-evaluation-must-report-coverage-and-partial-authority-v1"
    )
