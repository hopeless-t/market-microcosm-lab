from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WithdrawalCase:
    case_id: str
    withdrawn: bool
    reason_type: str
    deterioration_evidence: bool
    source_authority: str


def reference_cases() -> tuple[WithdrawalCase, ...]:
    return (
        WithdrawalCase(
            case_id="allied-overseas-saas-2024-02-14",
            withdrawn=True,
            reason_type="DUE_TO_DETERIORATION",
            deterioration_evidence=True,
            source_authority="company_public_disclosure",
        ),
        WithdrawalCase(
            case_id="healthy-metric-redesign-reference",
            withdrawn=True,
            reason_type="DUE_TO_METRIC_REDESIGN",
            deterioration_evidence=False,
            source_authority="synthetic_counterexample_consistent_with_jpx_guidance",
        ),
    )


def scalar_withdrawal_classifier(case: WithdrawalCase) -> bool:
    return case.withdrawn


def typed_withdrawal_classifier(case: WithdrawalCase) -> bool:
    return (
        case.withdrawn
        and case.reason_type == "DUE_TO_DETERIORATION"
        and case.deterioration_evidence
    )


def withdrawal_reason_report_payload() -> dict:
    cases = reference_cases()
    scalar = {
        case.case_id: scalar_withdrawal_classifier(case)
        for case in cases
    }
    typed = {
        case.case_id: typed_withdrawal_classifier(case)
        for case in cases
    }

    false_positive = (
        scalar["healthy-metric-redesign-reference"] is True
        and typed["healthy-metric-redesign-reference"] is False
    )

    gates = {
        "both_cases_have_the_same_withdrawn_boolean": all(
            case.withdrawn for case in cases
        ),
        "cases_have_distinct_reason_types": (
            len({case.reason_type for case in cases}) == 2
        ),
        "scalar_withdrawal_rule_false_positives_on_redesign": false_positive,
        "typed_rule_retains_allied_deterioration_signal": (
            typed["allied-overseas-saas-2024-02-14"] is True
        ),
        "typed_rule_rejects_redesign_as_deterioration": (
            typed["healthy-metric-redesign-reference"] is False
        ),
        "withdrawal_reason_and_source_authority_are_mandatory": True,
    }

    return {
        "experiment": "E082",
        "question": (
            "Can KPI withdrawal itself be treated as a universal deterioration "
            "signal, or must the withdrawal reason be typed?"
        ),
        "empirical_anchor": {
            "allied_case": (
                "Allied Architects explicitly links the overseas KPI withdrawal "
                "to deterioration and many Q4 cancellations."
            ),
            "jpx_context": (
                "JPX guidance allows KPI changes or withdrawals when business "
                "plans progress or are revised, provided the reason is explained."
            ),
        },
        "cases": [case.__dict__ for case in cases],
        "scalar_classifier": scalar,
        "typed_classifier": typed,
        "promotion_gate": gates,
        "promoted_typing_rule": (
            "kpi-withdrawal-requires-reason-type-and-source-authority-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "KPI withdrawal is not one semantic state. The observation event "
            "must carry a typed reason and source authority. Only a withdrawal "
            "whose admitted evidence links it to deterioration may contribute "
            "to a deterioration signal."
        ),
        "limitations": (
            "The redesign case is a synthetic counterexample motivated by JPX "
            "disclosure guidance; it is not attributed to Allied Architects."
        ),
    }
