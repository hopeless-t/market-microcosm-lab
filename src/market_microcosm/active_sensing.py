from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.robust_abstention import (
    RobustDecision,
    robust_threshold_decision,
)
from market_microcosm.decision_sufficient_observability import Interval


@dataclass(frozen=True)
class CandidateObservation:
    name: str
    cost: int
    resulting_interval: Interval | None
    direct_predicate_result: str | None = None


def candidate_observations() -> tuple[CandidateObservation, ...]:
    return (
        CandidateObservation(
            name="refine_previous_arr_only",
            cost=1,
            resulting_interval=Interval(1.7, 2.5),
        ),
        CandidateObservation(
            name="refine_current_arr_only",
            cost=1,
            resulting_interval=Interval(1.5, 2.3),
        ),
        CandidateObservation(
            name="exact_outgoing_boundary_only",
            cost=1,
            resulting_interval=Interval(1.5, 2.5),
        ),
        CandidateObservation(
            name="exact_current_mrr",
            cost=5,
            resulting_interval=Interval(2.0, 2.0),
        ),
        CandidateObservation(
            name="predicate_native_ledger_check",
            cost=2,
            resulting_interval=None,
            direct_predicate_result="CERTIFIED_TRUE",
        ),
    )


def evaluate_candidate(
    candidate: CandidateObservation,
    *,
    threshold: float = 2.0,
) -> dict:
    if candidate.direct_predicate_result is not None:
        result = candidate.direct_predicate_result
    else:
        assert candidate.resulting_interval is not None
        result = robust_threshold_decision(
            candidate.resulting_interval,
            threshold=threshold,
        ).result

    return {
        "name": candidate.name,
        "cost": candidate.cost,
        "result": result,
        "resolves_predicate": result in {
            "CERTIFIED_TRUE",
            "CERTIFIED_FALSE",
        },
        "resulting_interval": (
            [
                candidate.resulting_interval.low,
                candidate.resulting_interval.high,
            ]
            if candidate.resulting_interval is not None
            else None
        ),
        "direct_predicate_result": candidate.direct_predicate_result,
    }


def cheapest_resolving_observation() -> dict:
    evaluated = tuple(
        evaluate_candidate(candidate)
        for candidate in candidate_observations()
    )
    resolving = tuple(
        row for row in evaluated
        if row["resolves_predicate"]
    )
    if not resolving:
        raise ValueError("no resolving observation candidate")

    selected = min(
        resolving,
        key=lambda row: (row["cost"], row["name"]),
    )

    return {
        "candidates": list(evaluated),
        "selected": selected,
        "resolving_candidate_count": len(resolving),
    }


def active_sensing_report_payload() -> dict:
    selection = cheapest_resolving_observation()
    selected = selection["selected"]

    cheap_nonresolving = tuple(
        row
        for row in selection["candidates"]
        if row["cost"] == 1
    )

    exact_state = next(
        row
        for row in selection["candidates"]
        if row["name"] == "exact_current_mrr"
    )

    gates = {
        "cheap_local_refinements_remain_ambiguous": all(
            row["resolves_predicate"] is False
            for row in cheap_nonresolving
        ),
        "exact_state_query_resolves_but_is_more_expensive": (
            exact_state["resolves_predicate"] is True
            and exact_state["cost"] > selected["cost"]
        ),
        "predicate_native_query_is_selected": (
            selected["name"] == "predicate_native_ledger_check"
        ),
        "selected_query_resolves_predicate": (
            selected["resolves_predicate"] is True
        ),
        "query_selection_is_decision_scoped": True,
        "do_not_collect_full_state_when_cheaper_sufficient_evidence_exists": True,
    }

    return {
        "experiment": "E045",
        "question": (
            "After an authorized ABSTAIN, which additional observation should "
            "be requested if the goal is to resolve one decision predicate "
            "at minimum declared information cost?"
        ),
        "decision": {
            "predicate": "current MRR >= 2",
            "prior_interval": [1.5, 2.5],
            "prior_result": "ABSTAIN",
        },
        "candidate_search": selection,
        "promotion_gate": gates,
        "promoted_active_sensing_rule": (
            "request-cheapest-predicate-sufficient-observation-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "ABSTAIN triggers targeted active sensing. Candidate observations "
            "are scored by whether they resolve the requested predicate and "
            "their declared information/collection cost. Full-state queries "
            "lose priority when cheaper predicate-native evidence is sufficient."
        ),
        "limitations": (
            "Candidate costs are synthetic policy weights, not monetary "
            "estimates. A production system must derive costs from latency, "
            "privacy, operator burden, access authority, and measurement risk."
        ),
    }
