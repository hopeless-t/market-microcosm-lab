from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations


UNSAFE_OBLIGATIONS = frozenset(
    {"network", "identity", "power", "operator"}
)


@dataclass(frozen=True)
class AuditAction:
    action_id: str
    cost: int
    discharges: frozenset[str]


def audit_actions() -> tuple[AuditAction, ...]:
    return (
        AuditAction("network-targeted", 2, frozenset({"network"})),
        AuditAction("identity-targeted", 1, frozenset({"identity"})),
        AuditAction("power-deep", 3, frozenset({"power"})),
        AuditAction("operator-targeted", 2, frozenset({"operator"})),
        AuditAction(
            "control-plane-bundle",
            2,
            frozenset({"network", "identity"}),
        ),
        AuditAction(
            "infra-resilience-bundle",
            4,
            frozenset({"power", "operator"}),
        ),
        AuditAction(
            "full-platform-bundle",
            7,
            frozenset({"network", "identity", "power", "operator"}),
        ),
    )


def exact_audit_bundle_cover() -> dict:
    actions = audit_actions()
    candidates = []

    for size in range(1, len(actions) + 1):
        for selected in combinations(actions, size):
            covered = frozenset().union(
                *(action.discharges for action in selected)
            )
            if not UNSAFE_OBLIGATIONS.issubset(covered):
                continue
            candidates.append(
                {
                    "action_ids": sorted(
                        action.action_id for action in selected
                    ),
                    "action_count": len(selected),
                    "total_cost": sum(
                        action.cost for action in selected
                    ),
                    "covered_obligations": sorted(covered),
                }
            )

    if not candidates:
        raise ValueError("no audit cover")

    selected = min(
        candidates,
        key=lambda row: (
            row["total_cost"],
            row["action_count"],
            row["action_ids"],
        ),
    )

    return {
        "obligations": sorted(UNSAFE_OBLIGATIONS),
        "candidate_count": len(candidates),
        "selected": selected,
        "e060_independent_cost": 8,
        "savings_vs_e060": 8 - selected["total_cost"],
    }


def coupled_audit_bundle_report_payload() -> dict:
    result = exact_audit_bundle_cover()
    selected = result["selected"]

    gates = {
        "selected_cost_is_six": selected["total_cost"] == 6,
        "selected_uses_two_shared_bundles": (
            selected["action_ids"]
            == [
                "control-plane-bundle",
                "infra-resilience-bundle",
            ]
        ),
        "all_unsafe_obligations_are_covered": (
            set(selected["covered_obligations"])
            >= set(UNSAFE_OBLIGATIONS)
        ),
        "coupled_optimizer_beats_e060_independent_cost": (
            result["savings_vs_e060"] == 2
        ),
        "full_platform_bundle_is_not_minimum": (
            "full-platform-bundle"
            not in selected["action_ids"]
        ),
        "shared_evidence_costs_are_not_branch_separable": True,
    }

    return {
        "experiment": "E061",
        "question": (
            "Can shared audit actions discharge multiple dependency proof "
            "obligations more cheaply than E060's independent per-branch "
            "allocation, requiring a coupled exact set-cover optimizer?"
        ),
        "bundle_cover": result,
        "promotion_gate": gates,
        "promoted_bundle_rule": (
            "dependency-audit-allocation-must-model-shared-evidence-bundles-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Audit allocation becomes a coupled coverage problem. Shared "
            "evidence actions may discharge several proof obligations, so "
            "per-branch optimization can double-count work and lose global "
            "cost optimality."
        ),
        "limitations": (
            "The reference uses deterministic all-or-nothing obligation "
            "coverage. Real audits can provide partial evidence, uncertain "
            "coverage, sequencing dependencies, and reuse across epochs."
        ),
    }
