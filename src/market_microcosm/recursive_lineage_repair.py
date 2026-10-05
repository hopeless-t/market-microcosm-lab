from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations


@dataclass(frozen=True)
class RootPlacement:
    root_id: str
    current_provider: str
    migration_cost: int


def root_placements() -> tuple[RootPlacement, ...]:
    return (
        RootPlacement("root-0", "shared-observability-plane", 4),
        RootPlacement("root-1", "shared-observability-plane", 2),
        RootPlacement("root-2", "shared-observability-plane", 3),
        RootPlacement("root-3", "provider-d", 5),
        RootPlacement("root-4", "provider-e", 5),
    )


def placement_after_migration(
    migrated_roots: frozenset[str],
) -> dict[str, str]:
    placement = {}
    for root in root_placements():
        if root.root_id in migrated_roots:
            placement[root.root_id] = f"independent-{root.root_id}"
        else:
            placement[root.root_id] = root.current_provider
    return placement


def maximum_channels_per_provider(
    placement: dict[str, str],
    *,
    channels_per_root: int = 2,
) -> int:
    provider_counts: dict[str, int] = {}
    for provider in placement.values():
        provider_counts[provider] = (
            provider_counts.get(provider, 0) + channels_per_root
        )
    return max(provider_counts.values())


def exact_minimum_repartition() -> dict:
    roots = root_placements()
    candidates = []

    for size in range(len(roots) + 1):
        for selected in combinations(roots, size):
            migrated = frozenset(root.root_id for root in selected)
            placement = placement_after_migration(migrated)
            blast = maximum_channels_per_provider(placement)
            if blast > 2:
                continue
            candidates.append(
                {
                    "migrated_roots": sorted(migrated),
                    "migration_count": len(migrated),
                    "total_cost": sum(
                        root.migration_cost for root in selected
                    ),
                    "placement": placement,
                    "maximum_channels_per_provider": blast,
                }
            )

    if not candidates:
        raise ValueError("no safe repartition")

    selected = min(
        candidates,
        key=lambda row: (
            row["total_cost"],
            row["migration_count"],
            row["migrated_roots"],
        ),
    )

    return {
        "candidate_count": len(candidates),
        "selected": selected,
    }


def provider_fault_check() -> dict:
    selected = exact_minimum_repartition()["selected"]
    placement = selected["placement"]
    providers = sorted(set(placement.values()))
    cases = []

    for provider in providers:
        affected_roots = sorted(
            root_id
            for root_id, assigned in placement.items()
            if assigned == provider
        )
        flipped_channels = 2 * len(affected_roots)
        cases.append(
            {
                "provider": provider,
                "affected_roots": affected_roots,
                "flipped_channels": flipped_channels,
                "within_two_bit_budget": flipped_channels <= 2,
            }
        )

    return {
        "provider_count": len(providers),
        "case_count": len(cases),
        "all_within_budget": all(
            case["within_two_bit_budget"] for case in cases
        ),
        "cases": cases,
    }


def recursive_lineage_repair_report_payload() -> dict:
    synthesis = exact_minimum_repartition()
    check = provider_fault_check()
    selected = synthesis["selected"]

    gates = {
        "two_roots_are_migrated": (
            selected["migration_count"] == 2
        ),
        "minimum_cost_repair_is_five": (
            selected["total_cost"] == 5
        ),
        "selected_roots_are_one_and_two": (
            selected["migrated_roots"] == ["root-1", "root-2"]
        ),
        "every_provider_owns_at_most_one_measurement_root": (
            selected["maximum_channels_per_provider"] == 2
        ),
        "all_single_provider_faults_fit_two_bit_budget": (
            check["all_within_budget"] is True
        ),
        "repair_changes_topology_not_error_budget": True,
    }

    return {
        "experiment": "E058",
        "question": (
            "After E057 discovers a super-root spanning three measurement "
            "roots, what is the minimum-cost topology repair that restores "
            "the existing two-bit fault budget without weakening it?"
        ),
        "synthesis": synthesis,
        "single_provider_fault_check": check,
        "promotion_gate": gates,
        "promoted_repair_rule": (
            "recursive-lineage-common-mode-repair-by-minimum-cost-repartition-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "A discovered recursive common mode triggers topology synthesis, "
            "not a silent increase in tolerated blast radius. The optimizer "
            "moves the minimum-cost set of measurement roots onto independent "
            "providers until every single provider fault remains inside the "
            "existing certified bit budget."
        ),
        "limitations": (
            "The candidate repair action is simplified to moving a root onto "
            "a fresh independent provider. Real migrations have capacity, "
            "latency, vendor, regional, and hidden-lineage constraints."
        ),
    }
