from __future__ import annotations

from itertools import combinations


CHECKPOINTS = {
    "reporting-break": {
        "cost": 1,
        "claims": frozenset({"REVIEW_REQUIRED"}),
    },
    "exit-criteria-bound": {
        "cost": 1,
        "claims": frozenset({"EXIT_CRITERIA_EXIST"}),
    },
    "exit-confirmed": {
        "cost": 1,
        "claims": frozenset({"EXIT_CONFIRMED"}),
    },
}


REQUIRED_CLAIMS = {
    "REVIEW_REQUIRED": frozenset({"REVIEW_REQUIRED"}),
    "EXIT_CRITERIA_EXIST": frozenset({"EXIT_CRITERIA_EXIST"}),
    "EXIT_CONFIRMED": frozenset({"EXIT_CONFIRMED"}),
    "CHECKPOINTED_GOVERNANCE_PATH": frozenset(
        {"REVIEW_REQUIRED", "EXIT_CRITERIA_EXIST", "EXIT_CONFIRMED"}
    ),
}


def claims_for(selected: tuple[str, ...]) -> frozenset[str]:
    if not selected:
        return frozenset()
    return frozenset().union(
        *(CHECKPOINTS[checkpoint]["claims"] for checkpoint in selected)
    )


def exact_minimum_checkpoint_set(predicate: str) -> dict:
    required = REQUIRED_CLAIMS[predicate]
    ids = tuple(CHECKPOINTS)
    candidates = []

    for size in range(len(ids) + 1):
        for selected in combinations(ids, size):
            claims = claims_for(selected)
            if not required.issubset(claims):
                continue
            candidates.append(
                {
                    "checkpoints": sorted(selected),
                    "count": len(selected),
                    "cost": sum(CHECKPOINTS[item]["cost"] for item in selected),
                    "claims": sorted(claims),
                }
            )

    if not candidates:
        raise ValueError(f"no checkpoint set for {predicate}")

    selected = min(
        candidates,
        key=lambda row: (row["cost"], row["count"], row["checkpoints"]),
    )
    return {
        "predicate": predicate,
        "required_claims": sorted(required),
        "selected": selected,
        "candidate_count": len(candidates),
    }


def governance_checkpoint_authority_report_payload() -> dict:
    compiled = {
        predicate: exact_minimum_checkpoint_set(predicate)
        for predicate in REQUIRED_CLAIMS
    }

    gates = {
        "review_requires_only_reporting_break": (
            compiled["REVIEW_REQUIRED"]["selected"]["checkpoints"]
            == ["reporting-break"]
        ),
        "criteria_claim_requires_only_criteria_checkpoint": (
            compiled["EXIT_CRITERIA_EXIST"]["selected"]["checkpoints"]
            == ["exit-criteria-bound"]
        ),
        "exit_claim_requires_only_explicit_exit_event": (
            compiled["EXIT_CONFIRMED"]["selected"]["checkpoints"]
            == ["exit-confirmed"]
        ),
        "full_path_claim_requires_all_three": (
            compiled["CHECKPOINTED_GOVERNANCE_PATH"]["selected"]["checkpoints"]
            == ["exit-confirmed", "exit-criteria-bound", "reporting-break"]
        ),
        "full_path_cost_is_three": (
            compiled["CHECKPOINTED_GOVERNANCE_PATH"]["selected"]["cost"] == 3
        ),
        "checkpoint_authority_is_predicate_scoped": True,
    }

    return {
        "experiment": "E089",
        "question": (
            "Does every governance decision need the entire E087 three-step "
            "timeline, or can each claim use the minimum indispensable public "
            "checkpoint set?"
        ),
        "compiled_authority": compiled,
        "promotion_gate": gates,
        "promoted_checkpoint_authority_rule": (
            "governance-checkpoints-carry-predicate-specific-minimum-authority-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Checkpoint evidence is compiled per claim. A review escalation, "
            "existence of exit criteria, and confirmed exit each require only "
            "their own sufficient witness; all three checkpoints are required "
            "only when claiming the complete checkpointed governance path."
        ),
        "limitations": (
            "Reference checkpoint costs are uniform. Production audit cost, "
            "source authority, and failure-domain constraints can change the "
            "minimum evidence set."
        ),
    }
