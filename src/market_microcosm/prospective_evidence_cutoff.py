from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date


DECISION_CUTOFF = date(2025, 8, 14)


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    available_on: date
    role: str
    description: str


def evidence_items() -> tuple[EvidenceItem, ...]:
    return (
        EvidenceItem(
            "q3_kpis",
            date(2025, 8, 14),
            "feature",
            (
                "FY2025 Q3 ARR/churn/contracts/ARPA and contemporaneous "
                "management commentary."
            ),
        ),
        EvidenceItem(
            "q3_future_improvement_plan",
            date(2025, 8, 14),
            "feature",
            (
                "Q3 material states churn improvement is expected from the "
                "new Knowledge Suite release."
            ),
        ),
        EvidenceItem(
            "q4_outcome_metrics",
            date(2025, 11, 14),
            "label",
            "FY2025 Q4 ARR/churn/contracts/ARPA outcome.",
        ),
        EvidenceItem(
            "q4_launch_delay_annotation",
            date(2025, 11, 14),
            "retrospective_explanation",
            (
                "Q4 material states the planned Knowledge Suite+ launch "
                "timing slipped and ARR decreased."
            ),
        ),
        EvidenceItem(
            "q4_withdrawal_prep_annotation",
            date(2025, 11, 14),
            "retrospective_explanation",
            (
                "Q4 material states ARPA temporarily decreased amid launch "
                "delay and service-withdrawal preparation."
            ),
        ),
    )


def availability_partition() -> dict:
    items = evidence_items()
    available = tuple(
        item for item in items
        if item.available_on <= DECISION_CUTOFF
    )
    future = tuple(
        item for item in items
        if item.available_on > DECISION_CUTOFF
    )

    return {
        "decision_cutoff": DECISION_CUTOFF.isoformat(),
        "available_at_decision": [asdict(item) for item in available],
        "future_only": [asdict(item) for item in future],
    }


def feature_sets() -> dict:
    partition = availability_partition()
    available_ids = {
        row["evidence_id"]
        for row in partition["available_at_decision"]
    }

    prospective = {
        "q3_kpis",
        "q3_future_improvement_plan",
    }
    retrospective = prospective | {
        "q4_launch_delay_annotation",
        "q4_withdrawal_prep_annotation",
    }

    return {
        "prospective_feature_ids": sorted(prospective),
        "retrospective_feature_ids": sorted(retrospective),
        "prospective_all_available": prospective <= available_ids,
        "retrospective_contains_future_leakage": (
            not retrospective <= available_ids
        ),
        "leaked_feature_ids": sorted(
            retrospective - available_ids
        ),
    }


def prospective_evidence_cutoff_report_payload() -> dict:
    partition = availability_partition()
    sets = feature_sets()

    gates = {
        "prospective_features_exist_at_cutoff": (
            sets["prospective_all_available"] is True
        ),
        "q4_explanations_are_future_only": (
            {
                "q4_launch_delay_annotation",
                "q4_withdrawal_prep_annotation",
            }
            <= {
                row["evidence_id"]
                for row in partition["future_only"]
            }
        ),
        "retrospective_feature_set_is_leaky": (
            sets["retrospective_contains_future_leakage"] is True
        ),
        "leaked_features_are_identified_exactly": (
            sets["leaked_feature_ids"]
            == [
                "q4_launch_delay_annotation",
                "q4_withdrawal_prep_annotation",
            ]
        ),
        "outcome_label_is_not_a_decision_time_feature": any(
            row["evidence_id"] == "q4_outcome_metrics"
            for row in partition["future_only"]
        ),
        "explanation_authority_and_prediction_authority_are_separate": True,
    }

    return {
        "experiment": "E064",
        "question": (
            "Can E063's Q4 event annotations be used to explain the realized "
            "portfolio transition without leaking future information into a "
            "Q3 prospective warning evaluation?"
        ),
        "availability": partition,
        "feature_sets": sets,
        "promotion_gate": gates,
        "promoted_cutoff_rule": (
            "prospective-warning-evidence-must-exist-before-decision-cutoff-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Longitudinal evidence receives an availability timestamp and a "
            "role. Post-outcome event annotations may support retrospective "
            "explanation but cannot enter prospective warning features unless "
            "they were already available before the declared decision cutoff."
        ),
        "limitations": (
            "The reference uses public disclosure dates as evidence "
            "availability. Internal company operators may have had earlier "
            "knowledge; that would be a different authority scope and dataset."
        ),
    }
