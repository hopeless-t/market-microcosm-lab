from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product


@dataclass(frozen=True)
class AuditOption:
    branch: str
    option: str
    cost: int
    residual_blast_channels: int


def branch_options() -> dict[str, tuple[AuditOption, ...]]:
    return {
        "network": (
            AuditOption("network", "none", 0, 4),
            AuditOption("network", "targeted", 2, 2),
            AuditOption("network", "deep", 4, 2),
        ),
        "identity": (
            AuditOption("identity", "none", 0, 4),
            AuditOption("identity", "targeted", 1, 2),
            AuditOption("identity", "deep", 3, 2),
        ),
        "power": (
            AuditOption("power", "none", 0, 6),
            AuditOption("power", "shallow", 1, 4),
            AuditOption("power", "deep", 3, 2),
        ),
        "vendor": (
            AuditOption("vendor", "none", 0, 2),
            AuditOption("vendor", "deep", 2, 2),
        ),
        "operator": (
            AuditOption("operator", "none", 0, 4),
            AuditOption("operator", "targeted", 2, 2),
            AuditOption("operator", "deep", 4, 2),
        ),
    }


def exact_branch_audit_allocation(
    *,
    maximum_blast_channels: int = 2,
) -> dict:
    options = branch_options()
    branches = tuple(options)
    candidates = []

    for selected in product(
        *(options[branch] for branch in branches)
    ):
        if any(
            option.residual_blast_channels
            > maximum_blast_channels
            for option in selected
        ):
            continue

        candidates.append(
            {
                "total_cost": sum(option.cost for option in selected),
                "selection": {
                    option.branch: asdict(option)
                    for option in selected
                },
                "maximum_residual_blast_channels": max(
                    option.residual_blast_channels
                    for option in selected
                ),
            }
        )

    if not candidates:
        raise ValueError("no safe branch allocation")

    selected = min(
        candidates,
        key=lambda row: (
            row["total_cost"],
            tuple(
                row["selection"][branch]["option"]
                for branch in branches
            ),
        ),
    )

    uniform_deep = {
        branch: next(
            option
            for option in options[branch]
            if option.option == "deep"
        )
        for branch in branches
    }
    uniform_deep_cost = sum(
        option.cost for option in uniform_deep.values()
    )

    return {
        "maximum_blast_channels": maximum_blast_channels,
        "safe_candidate_count": len(candidates),
        "selected": selected,
        "uniform_deep_cost": uniform_deep_cost,
        "cost_savings_vs_uniform_deep": (
            uniform_deep_cost - selected["total_cost"]
        ),
    }


def heterogeneous_audit_report_payload() -> dict:
    result = exact_branch_audit_allocation()
    selected = result["selected"]

    gates = {
        "selected_allocation_cost_is_eight": (
            selected["total_cost"] == 8
        ),
        "network_uses_targeted_audit": (
            selected["selection"]["network"]["option"] == "targeted"
        ),
        "identity_uses_targeted_audit": (
            selected["selection"]["identity"]["option"] == "targeted"
        ),
        "power_requires_deep_audit": (
            selected["selection"]["power"]["option"] == "deep"
        ),
        "vendor_requires_no_extra_audit": (
            selected["selection"]["vendor"]["option"] == "none"
        ),
        "operator_uses_targeted_audit": (
            selected["selection"]["operator"]["option"] == "targeted"
        ),
        "heterogeneous_allocation_saves_eight_vs_uniform_deep": (
            result["cost_savings_vs_uniform_deep"] == 8
        ),
        "every_branch_meets_two_channel_budget": (
            selected["maximum_residual_blast_channels"] == 2
        ),
    }

    return {
        "experiment": "E060",
        "question": (
            "If dependency branches have different residual blast bounds and "
            "audit costs, can branch-specific audit depth satisfy the same "
            "two-channel authority budget more cheaply than uniform deep audit?"
        ),
        "allocation": result,
        "promotion_gate": gates,
        "promoted_allocation_rule": (
            "recursive-lineage-audit-depth-is-allocated-per-proof-obligation-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Dependency depth is no longer one global scalar. Each branch is "
            "audited only as deeply as needed to discharge its own blast-radius "
            "proof obligation, and exact allocation minimizes total audit cost "
            "subject to the common downstream authority budget."
        ),
        "limitations": (
            "The branch options are independent in this reference. Real audits "
            "can share evidence or have coupled costs, which requires a bundle/"
            "set-cover optimizer rather than independent per-branch choices."
        ),
    }
