from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class SemanticAtom:
    name: str
    observation_cost: int
    decision_value: int
    evidence_age: int
    stale: bool
    hazard_signal: bool
    mandatory_for_promotion: bool = False


ATOMS = (
    SemanticAtom("authority-contract", 3, 12, 2, True, True, True),
    SemanticAtom("dependency-map", 2, 10, 3, True, True),
    SemanticAtom("cost-model", 2, 7, 5, True, True),
    SemanticAtom("workflow-shape", 2, 8, 1, False, False),
    SemanticAtom("archive-note", 1, 0, 12, True, True),
    SemanticAtom("display-copy", 1, 1, 10, True, True),
    SemanticAtom("source-provenance", 2, 4, 8, False, False),
)

OBSERVATION_BUDGET = 7


def _summarize(name: str, selected: tuple[SemanticAtom, ...]) -> dict:
    selected_names = {atom.name for atom in selected}
    mandatory_names = {atom.name for atom in ATOMS if atom.mandatory_for_promotion}
    restored_value = sum(atom.decision_value for atom in selected if atom.stale)
    total_stale_value = sum(atom.decision_value for atom in ATOMS if atom.stale)
    cost = sum(atom.observation_cost for atom in selected)
    return {
        "policy": name,
        "selected": sorted(selected_names),
        "observation_cost": cost,
        "budget_feasible": cost <= OBSERVATION_BUDGET,
        "mandatory_observed": mandatory_names <= selected_names,
        "restored_decision_value": restored_value,
        "total_stale_decision_value": total_stale_value,
        "restored_value_coverage": restored_value / total_stale_value,
        "fresh_observation_waste_cost": sum(
            atom.observation_cost for atom in selected if not atom.stale
        ),
    }


def observe_whole_object() -> dict:
    return _summarize("observe-whole-object", ATOMS)


def oldest_first() -> dict:
    selected: list[SemanticAtom] = []
    spent = 0
    for atom in sorted(ATOMS, key=lambda item: (-item.evidence_age, item.name)):
        if spent + atom.observation_cost > OBSERVATION_BUDGET:
            continue
        selected.append(atom)
        spent += atom.observation_cost
    return _summarize("oldest-first", tuple(selected))


def mandatory_then_value_density() -> dict:
    mandatory = [atom for atom in ATOMS if atom.mandatory_for_promotion]
    selected = list(mandatory)
    spent = sum(atom.observation_cost for atom in selected)
    remaining = [atom for atom in ATOMS if not atom.mandatory_for_promotion]
    for atom in sorted(
        remaining,
        key=lambda item: (-(item.decision_value / item.observation_cost), item.name),
    ):
        if spent + atom.observation_cost > OBSERVATION_BUDGET:
            continue
        selected.append(atom)
        spent += atom.observation_cost
    return _summarize("mandatory-then-value-density", tuple(selected))


def _exact(*, use_hidden_staleness: bool) -> dict:
    best: tuple[int, int, tuple[str, ...], tuple[SemanticAtom, ...]] | None = None
    work_units = 0
    mandatory_names = {atom.name for atom in ATOMS if atom.mandatory_for_promotion}
    for size in range(len(ATOMS) + 1):
        for subset in combinations(ATOMS, size):
            work_units += 1
            names = {atom.name for atom in subset}
            cost = sum(atom.observation_cost for atom in subset)
            if cost > OBSERVATION_BUDGET or not mandatory_names <= names:
                continue
            if use_hidden_staleness:
                value = sum(atom.decision_value for atom in subset if atom.stale)
            else:
                value = sum(atom.decision_value for atom in subset if atom.hazard_signal)
            rank = (value, -cost, tuple(sorted(names)))
            if best is None or rank > best[:3]:
                best = (rank[0], rank[1], rank[2], subset)
    assert best is not None
    result = _summarize(
        "hidden-staleness-oracle" if use_hidden_staleness else "hazard-aware-exact-budget",
        best[3],
    )
    result["objective_value"] = best[0]
    result["work_units"] = work_units
    return result


def hidden_staleness_oracle() -> dict:
    return _exact(use_hidden_staleness=True)


def hazard_aware_exact_budget() -> dict:
    return _exact(use_hidden_staleness=False)


def rpe008_report_payload() -> dict:
    whole = observe_whole_object()
    oldest = oldest_first()
    density = mandatory_then_value_density()
    hazard = hazard_aware_exact_budget()
    oracle = hidden_staleness_oracle()

    gates = {
        "whole_object_refresh_exceeds_budget": not whole["budget_feasible"],
        "oldest_first_misses_mandatory_atom": not oldest["mandatory_observed"],
        "oldest_first_restores_less_value_than_hazard_exact": oldest["restored_decision_value"] < hazard["restored_decision_value"],
        "value_density_wastes_fresh_observation": density["fresh_observation_waste_cost"] > 0,
        "value_density_is_suboptimal": density["restored_decision_value"] < oracle["restored_decision_value"],
        "hazard_exact_preserves_mandatory_atom": hazard["mandatory_observed"],
        "hazard_exact_matches_hidden_oracle_in_fixture": (
            hazard["selected"] == oracle["selected"]
            and hazard["restored_decision_value"] == oracle["restored_decision_value"]
        ),
        "hazard_exact_respects_budget": hazard["budget_feasible"],
    }

    return {
        "experiment": "RPE-008",
        "title": "Partial staleness and observation-budget allocation",
        "fixture": {
            "atom_count": len(ATOMS),
            "observation_budget": OBSERVATION_BUDGET,
            "total_full_refresh_cost": sum(atom.observation_cost for atom in ATOMS),
            "total_stale_decision_value": sum(atom.decision_value for atom in ATOMS if atom.stale),
        },
        "policies": {
            "observe_whole_object": whole,
            "oldest_first": oldest,
            "mandatory_then_value_density": density,
            "hazard_aware_exact_budget": hazard,
            "hidden_staleness_oracle": oracle,
        },
        "promotion_gate": gates,
        "candidate_rule": "REOBSERVE_DECISION_RELEVANT_STALE_ATOMS_NOT_WHOLE_OBJECTS_PRESERVE_MANDATORY_AUTHORITY_ATOMS",
        "claim_ceiling": "EXACT_SMALL_SYNTHETIC_ATOM_PORTFOLIO_ONLY_NO_REAL_STALENESS_DETECTOR_CLAIM",
    }
