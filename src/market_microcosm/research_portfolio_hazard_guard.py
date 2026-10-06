from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from market_microcosm.research_portfolio_partial_staleness import ATOMS, OBSERVATION_BUDGET


ATOM_GROUP = {
    "authority-contract": "governance",
    "dependency-map": "governance",
    "cost-model": "economics",
    "workflow-shape": "workflow",
    "archive-note": "archive",
    "display-copy": "presentation",
    "source-provenance": "provenance",
}
CRITICAL_GROUPS = {"governance"}


@dataclass(frozen=True)
class HazardScenario:
    name: str
    active_hazards: frozenset[str]
    degraded_groups: frozenset[str]


TRUE_HAZARDS = frozenset(
    {"authority-contract", "dependency-map", "cost-model", "archive-note", "display-copy"}
)

SCENARIOS = (
    HazardScenario("healthy", TRUE_HAZARDS, frozenset()),
    HazardScenario(
        "false-positive-workflow",
        TRUE_HAZARDS | {"workflow-shape"},
        frozenset({"workflow"}),
    ),
    HazardScenario(
        "false-negative-dependency",
        TRUE_HAZARDS - {"dependency-map"},
        frozenset({"governance"}),
    ),
    HazardScenario(
        "combined",
        (TRUE_HAZARDS - {"dependency-map"}) | {"workflow-shape"},
        frozenset({"governance", "workflow"}),
    ),
)


def _select(
    scenario: HazardScenario, *, health_guarded: bool
) -> dict:
    mandatory = {atom.name for atom in ATOMS if atom.mandatory_for_promotion}
    forced = set(mandatory)
    active = set(scenario.active_hazards)

    if health_guarded:
        for group in scenario.degraded_groups:
            members = {atom.name for atom in ATOMS if ATOM_GROUP[atom.name] == group}
            if group in CRITICAL_GROUPS:
                forced |= members
            else:
                active -= members

    best = None
    work_units = 0
    for size in range(len(ATOMS) + 1):
        for subset in combinations(ATOMS, size):
            work_units += 1
            names = {atom.name for atom in subset}
            cost = sum(atom.observation_cost for atom in subset)
            if cost > OBSERVATION_BUDGET or not forced <= names:
                continue
            scored_names = forced | active
            score = sum(atom.decision_value for atom in subset if atom.name in scored_names)
            rank = (score, -cost, tuple(sorted(names)))
            if best is None or rank > best[:3]:
                best = (rank[0], rank[1], rank[2], subset)

    assert best is not None
    selected = best[3]
    selected_names = {atom.name for atom in selected}
    restored = sum(atom.decision_value for atom in selected if atom.stale)
    total_stale = sum(atom.decision_value for atom in ATOMS if atom.stale)
    return {
        "policy": "health-guarded-hazard" if health_guarded else "hazard-only",
        "scenario": scenario.name,
        "selected": sorted(selected_names),
        "observation_cost": sum(atom.observation_cost for atom in selected),
        "restored_decision_value": restored,
        "restored_value_coverage": restored / total_stale,
        "fresh_observation_waste_cost": sum(
            atom.observation_cost for atom in selected if not atom.stale
        ),
        "mandatory_observed": mandatory <= selected_names,
        "work_units": work_units,
    }


def _aggregate(*, health_guarded: bool) -> dict:
    rows = [_select(scenario, health_guarded=health_guarded) for scenario in SCENARIOS]
    total_restored = sum(row["restored_decision_value"] for row in rows)
    possible = len(rows) * sum(atom.decision_value for atom in ATOMS if atom.stale)
    return {
        "policy": "health-guarded-hazard" if health_guarded else "hazard-only",
        "aggregate_restored_decision_value": total_restored,
        "aggregate_possible_stale_value": possible,
        "aggregate_coverage": total_restored / possible,
        "aggregate_observation_cost": sum(row["observation_cost"] for row in rows),
        "aggregate_fresh_waste_cost": sum(row["fresh_observation_waste_cost"] for row in rows),
        "scenario_results": rows,
    }


def rpe009_report_payload() -> dict:
    naive = _aggregate(health_guarded=False)
    guarded = _aggregate(health_guarded=True)
    naive_by_name = {row["scenario"]: row for row in naive["scenario_results"]}
    guarded_by_name = {row["scenario"]: row for row in guarded["scenario_results"]}

    gates = {
        "false_positive_can_waste_budget": naive_by_name["false-positive-workflow"]["fresh_observation_waste_cost"] > 0,
        "false_positive_can_reduce_restored_value": (
            naive_by_name["false-positive-workflow"]["restored_decision_value"]
            < naive_by_name["healthy"]["restored_decision_value"]
        ),
        "false_negative_can_hide_stale_dependency": naive_by_name["false-negative-dependency"]["restored_decision_value"] < 29,
        "combined_error_is_worse_than_healthy": naive_by_name["combined"]["restored_decision_value"] < naive_by_name["healthy"]["restored_decision_value"],
        "health_guard_recovers_all_four_fixture_scenarios": all(
            row["restored_decision_value"] == 29 for row in guarded["scenario_results"]
        ),
        "health_guard_eliminates_fresh_waste_in_fixture": guarded["aggregate_fresh_waste_cost"] == 0,
        "critical_degraded_group_forces_dependency_audit": (
            "dependency-map" in guarded_by_name["false-negative-dependency"]["selected"]
        ),
        "noncritical_degraded_group_does_not_force_false_positive": (
            "workflow-shape" not in guarded_by_name["false-positive-workflow"]["selected"]
        ),
    }

    return {
        "experiment": "RPE-009",
        "title": "Atom-level hazard-channel reliability adversary",
        "fixture": {
            "scenario_count": len(SCENARIOS),
            "observation_budget": OBSERVATION_BUDGET,
            "critical_groups": sorted(CRITICAL_GROUPS),
        },
        "policies": {
            "hazard_only": naive,
            "health_guarded_hazard": guarded,
        },
        "promotion_gate": gates,
        "candidate_rule": "ATOM_HAZARDS_REQUIRE_GROUP_HEALTH_GUARDS_CRITICAL_DEGRADATION_FAILS_CLOSED_TO_AUDIT_NONCRITICAL_DEGRADATION_SUPPRESSES_UNTRUSTED_SIGNALS",
        "claim_ceiling": "DETERMINISTIC_SYNTHETIC_HAZARD_CHANNEL_FIXTURE_ONLY_NO_REAL_STALENESS_SIGNAL_RELIABILITY_CLAIM",
    }
