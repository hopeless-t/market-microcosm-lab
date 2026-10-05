from __future__ import annotations


def governance_action(event_type: str, reason_type: str | None = None) -> str:
    if event_type == "SUBSIDIARY_DISSOLUTION_AND_LIQUIDATION_DECISION":
        return "EXIT_CONFIRMED"
    if event_type == "KPI_WITHDRAWN":
        if reason_type == "DUE_TO_DETERIORATION":
            return "ESCALATE_REVIEW"
        if reason_type == "DUE_TO_METRIC_REDESIGN":
            return "KERNEL_CHANGE_ONLY"
        return "ABSTAIN_REASON_UNKNOWN"
    return "NO_GOVERNANCE_ACTION"


def withdrawal_governance_report_payload() -> dict:
    deterioration = governance_action(
        "KPI_WITHDRAWN", "DUE_TO_DETERIORATION"
    )
    redesign = governance_action(
        "KPI_WITHDRAWN", "DUE_TO_METRIC_REDESIGN"
    )
    unknown = governance_action("KPI_WITHDRAWN", None)
    exit_event = governance_action(
        "SUBSIDIARY_DISSOLUTION_AND_LIQUIDATION_DECISION"
    )

    gates = {
        "deterioration_withdrawal_escalates_but_does_not_exit": (
            deterioration == "ESCALATE_REVIEW"
        ),
        "metric_redesign_does_not_emit_deterioration_action": (
            redesign == "KERNEL_CHANGE_ONLY"
        ),
        "unknown_reason_abstains": unknown == "ABSTAIN_REASON_UNKNOWN",
        "explicit_exit_decision_confirms_exit": exit_event == "EXIT_CONFIRMED",
        "withdrawal_alone_never_maps_directly_to_exit": all(
            action != "EXIT_CONFIRMED"
            for action in (deterioration, redesign, unknown)
        ),
        "e085_temporal_holdout_is_not_converted_into_deterministic_predictor": True,
    }

    return {
        "experiment": "E086",
        "question": (
            "After E085 observes that deterioration-linked KPI withdrawal "
            "preceded a later real exit, should withdrawal itself become a "
            "deterministic EXIT rule?"
        ),
        "actions": {
            "withdrawal_due_to_deterioration": deterioration,
            "withdrawal_due_to_metric_redesign": redesign,
            "withdrawal_reason_unknown": unknown,
            "explicit_liquidation_decision": exit_event,
        },
        "promotion_gate": gates,
        "promoted_governance_rule": (
            "deterioration-linked-kpi-withdrawal-triggers-review-not-deterministic-exit-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "A deterioration-linked reporting event can escalate governance "
            "attention without becoming an exit command. EXIT authority is "
            "reserved for a later explicit strategic/corporate decision or "
            "other independently sufficient evidence."
        ),
        "limitations": (
            "The action mapping is a reference governance semantics, not a "
            "recommendation for any specific company or investment decision."
        ),
    }
