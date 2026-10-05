from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class EmpiricalCase:
    case_id: str
    arr_down_churn_up: bool
    reporting_break_due_to_deterioration: bool
    persistent_profitability_failure: bool
    competitive_advantage_failure: bool
    later_recovery_observed: bool
    escalation_required: bool


def empirical_cases() -> tuple[EmpiricalCase, ...]:
    return (
        EmpiricalCase(
            case_id="GVA_transient_stress",
            arr_down_churn_up=True,
            reporting_break_due_to_deterioration=False,
            persistent_profitability_failure=False,
            competitive_advantage_failure=False,
            later_recovery_observed=True,
            escalation_required=False,
        ),
        EmpiricalCase(
            case_id="BBD_portfolio_transition",
            arr_down_churn_up=False,
            reporting_break_due_to_deterioration=False,
            persistent_profitability_failure=False,
            competitive_advantage_failure=False,
            later_recovery_observed=False,
            escalation_required=False,
        ),
        EmpiricalCase(
            case_id="Allied_overseas_deterioration",
            arr_down_churn_up=False,
            reporting_break_due_to_deterioration=True,
            persistent_profitability_failure=True,
            competitive_advantage_failure=False,
            later_recovery_observed=False,
            escalation_required=True,
        ),
        EmpiricalCase(
            case_id="Jooto_growth_viability_failure",
            arr_down_churn_up=False,
            reporting_break_due_to_deterioration=False,
            persistent_profitability_failure=True,
            competitive_advantage_failure=True,
            later_recovery_observed=False,
            escalation_required=True,
        ),
    )


def scalar_sign_rule(case: EmpiricalCase) -> bool:
    return case.arr_down_churn_up


def typed_mechanism_rule(case: EmpiricalCase) -> bool:
    reporting_escalation = case.reporting_break_due_to_deterioration
    viability_failure = (
        case.persistent_profitability_failure
        and case.competitive_advantage_failure
    )
    return reporting_escalation or viability_failure


def score(rule) -> dict:
    tp = fp = tn = fn = 0
    rows = []
    for case in empirical_cases():
        predicted = rule(case)
        actual = case.escalation_required
        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
        elif not predicted and actual:
            fn += 1
        else:
            tn += 1
        rows.append(
            {
                "case_id": case.case_id,
                "predicted_escalation": predicted,
                "actual_escalation": actual,
            }
        )
    return {
        "confusion": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
        "accuracy": (tp + tn) / len(rows),
        "rows": rows,
    }


def empirical_warning_tournament_report_payload() -> dict:
    scalar = score(scalar_sign_rule)
    typed = score(typed_mechanism_rule)

    gates = {
        "scalar_rule_false_positives_on_gva_recovery_control": (
            scalar["confusion"]["fp"] == 1
        ),
        "scalar_rule_misses_allied_and_jooto": (
            scalar["confusion"]["fn"] == 2
        ),
        "typed_rule_exact_on_four_case_suite": (
            typed["accuracy"] == 1.0
            and typed["confusion"] == {"tp": 2, "fp": 0, "tn": 2, "fn": 0}
        ),
        "gva_negative_control_remains_non_escalation": any(
            row["case_id"] == "GVA_transient_stress"
            and row["predicted_escalation"] is False
            for row in typed["rows"]
        ),
        "bbd_transition_is_not_forced_into_failure": any(
            row["case_id"] == "BBD_portfolio_transition"
            and row["predicted_escalation"] is False
            for row in typed["rows"]
        ),
        "real_case_suite_is_mechanism_test_not_prevalence_estimate": True,
    }

    return {
        "experiment": "E098",
        "question": (
            "Does a real-case warning rule that uses typed mechanism evidence "
            "avoid the false positive created by one-quarter ARR/churn stress "
            "while still escalating stronger Allied and Jooto evidence?"
        ),
        "cases": [asdict(case) for case in empirical_cases()],
        "scalar_sign_rule": scalar,
        "typed_mechanism_rule": typed,
        "promotion_gate": gates,
        "promoted_empirical_warning_rule": (
            "real-case-warning-escalation-requires-typed-mechanism-evidence-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "The warning layer gains a real recovery negative control. One-quarter "
            "ARR/churn stress remains an observation, while escalation authority "
            "requires stronger typed mechanism evidence such as deterioration-linked "
            "reporting break or persistent profitability plus competitive-advantage failure."
        ),
        "limitations": (
            "The four-case suite is intentionally tiny and hand-typed from public evidence. "
            "Exact fit is a semantic regression test, not validated predictive accuracy."
        ),
    }
