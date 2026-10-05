from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastCase:
    case_id: str
    prediction: str
    numeric_label_available: bool
    numeric_label: str | None
    informative_withdrawal_event: bool


def reference_cases() -> tuple[ForecastCase, ...]:
    scored = tuple(
        ForecastCase(
            case_id=f"stable-{index}",
            prediction="STABLE",
            numeric_label_available=True,
            numeric_label="STABLE",
            informative_withdrawal_event=False,
        )
        for index in range(8)
    )
    censored = (
        ForecastCase(
            case_id="withdrawn-a",
            prediction="STABLE",
            numeric_label_available=False,
            numeric_label=None,
            informative_withdrawal_event=True,
        ),
        ForecastCase(
            case_id="withdrawn-b",
            prediction="STABLE",
            numeric_label_available=False,
            numeric_label=None,
            informative_withdrawal_event=True,
        ),
    )
    return scored + censored


def naive_complete_case_score() -> dict:
    cases = [case for case in reference_cases() if case.numeric_label_available]
    correct = sum(case.prediction == case.numeric_label for case in cases)
    return {
        "numeric_accuracy": correct / len(cases),
        "scored_cases": len(cases),
        "reported_coverage": None,
        "informative_censoring_reported": False,
        "authority": "UNSOUND_IF_PRESENTED_AS_FULL_EVALUATION",
    }


def coverage_aware_score() -> dict:
    cases = reference_cases()
    scored = [case for case in cases if case.numeric_label_available]
    correct = sum(case.prediction == case.numeric_label for case in scored)
    censored = [case for case in cases if not case.numeric_label_available]
    informative = [case for case in censored if case.informative_withdrawal_event]

    coverage = len(scored) / len(cases)
    authority = (
        "FULL_EVALUATION"
        if coverage == 1.0
        else "PARTIAL_EVALUATION_ONLY"
    )
    return {
        "numeric_accuracy_on_observed_labels": correct / len(scored),
        "numeric_label_coverage": coverage,
        "scored_cases": len(scored),
        "total_cases": len(cases),
        "informative_withdrawal_cases": len(informative),
        "unscored_cases_are_counted_as_errors": False,
        "unscored_cases_are_counted_as_correct": False,
        "authority": authority,
    }


def censored_evaluation_report_payload() -> dict:
    naive = naive_complete_case_score()
    aware = coverage_aware_score()

    gates = {
        "naive_observed_label_accuracy_is_one": (
            naive["numeric_accuracy"] == 1.0
        ),
        "numeric_label_coverage_is_only_eighty_percent": (
            aware["numeric_label_coverage"] == 0.8
        ),
        "two_informative_withdrawal_cases_are_visible": (
            aware["informative_withdrawal_cases"] == 2
        ),
        "censored_cases_are_neither_correct_nor_error": (
            aware["unscored_cases_are_counted_as_errors"] is False
            and aware["unscored_cases_are_counted_as_correct"] is False
        ),
        "authority_is_partial_not_full": (
            aware["authority"] == "PARTIAL_EVALUATION_ONLY"
        ),
        "accuracy_requires_coverage_and_censoring_context": True,
    }

    return {
        "experiment": "E083",
        "question": (
            "When numeric outcome labels disappear through informative KPI "
            "withdrawal, can complete-case accuracy still be presented as a "
            "full evaluation?"
        ),
        "naive_complete_case": naive,
        "coverage_aware": aware,
        "promotion_gate": gates,
        "promoted_evaluation_rule": (
            "informatively-censored-evaluation-must-report-coverage-and-partial-authority-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Numeric evaluation authority now carries coverage and censoring "
            "state. High observed-label accuracy cannot be promoted to full "
            "evaluation when state-dependent reporting removes outcome labels."
        ),
        "limitations": (
            "The finite reference does not identify the hidden numeric outcomes. "
            "Censored cases are deliberately neither scored correct nor scored wrong."
        ),
    }
