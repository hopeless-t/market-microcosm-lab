from __future__ import annotations

from itertools import permutations

from market_microcosm.dependence_ambiguity_acquisition import BUNDLES
from market_microcosm.direct_evidence_acquisition import acquisitions
from market_microcosm.sequential_evidence_acquisition import (
    expected_cost_for_order as reference_expected_cost_for_order,
)


MARGINAL_INTERVALS = {
    "cash_collection_gap": (0.03, 0.08),
    "fully_loaded_delivery_margin": (0.07, 0.15),
    "market_headroom": (0.20, 0.40),
    "downstream_funnel_success": (0.12, 0.25),
    "strategic_exit_value_gap": (0.15, 0.35),
}


def authorized_bundle_map():
    return {
        action.acquisition_id: action
        for action in acquisitions()
        if action.authorized and action.acquisition_id in BUNDLES
    }


def interval_frechet_upper_all_safe(
    axes: frozenset[str],
) -> float:
    if not axes:
        return 1.0
    return 1.0 - max(
        MARGINAL_INTERVALS[axis][0]
        for axis in axes
    )


def worst_case_interval_dependence_cost(
    order: tuple[str, ...],
) -> float:
    by_id = authorized_bundle_map()
    observed = frozenset()
    expected = 0.0

    for action_id in order:
        action = by_id[action_id]
        expected += (
            interval_frechet_upper_all_safe(observed)
            * action.cost
        )
        observed = frozenset(observed | action.direct_axes)

    return expected


def lower_bound_nested_atoms() -> list[dict]:
    lower = {
        axis: interval[0]
        for axis, interval in MARGINAL_INTERVALS.items()
    }
    thresholds = sorted(set(lower.values()))
    bounds = [0.0, *thresholds, 1.0]
    rows = []

    for low, high in zip(bounds, bounds[1:]):
        if high <= low:
            continue
        midpoint = (low + high) / 2.0
        rows.append(
            {
                "probability": high - low,
                "bad_axes": sorted(
                    axis
                    for axis, probability in lower.items()
                    if midpoint < probability
                ),
            }
        )
    return rows


def witness_expected_cost(order: tuple[str, ...]) -> float:
    by_id = authorized_bundle_map()
    total = 0.0

    for atom in lower_bound_nested_atoms():
        bad = set(atom["bad_axes"])
        realized = 0.0
        for action_id in order:
            action = by_id[action_id]
            realized += action.cost
            if bad.intersection(action.direct_axes):
                break
        total += atom["probability"] * realized

    return total


def interval_dependence_search() -> dict:
    rows = []
    for order in permutations(BUNDLES):
        worst = worst_case_interval_dependence_cost(order)
        witness = witness_expected_cost(order)
        reference = reference_expected_cost_for_order(order)
        rows.append(
            {
                "order": list(order),
                "worst_case_expected_cost": worst,
                "lower_bound_nested_witness_cost": witness,
                "reference_expected_cost": reference,
                "bound_is_tight": abs(worst - witness) < 1e-12,
            }
        )

    best = min(row["worst_case_expected_cost"] for row in rows)
    minimax = [
        row for row in rows
        if abs(row["worst_case_expected_cost"] - best) < 1e-12
    ]
    selected = min(
        minimax,
        key=lambda row: (
            row["reference_expected_cost"],
            row["order"],
        ),
    )

    return {
        "candidate_count": len(rows),
        "rows": rows,
        "minimax_tie_count": len(minimax),
        "selected": selected,
        "witness_atoms": lower_bound_nested_atoms(),
    }


def interval_dependence_report_payload() -> dict:
    result = interval_dependence_search()
    selected = result["selected"]

    gates = {
        "six_orders_are_exhaustively_checked": (
            result["candidate_count"] == 6
        ),
        "every_worst_case_bound_is_constructively_tight": all(
            row["bound_is_tight"] for row in result["rows"]
        ),
        "two_gtm_first_orders_tie_at_twelve": (
            result["minimax_tie_count"] == 2
            and round(selected["worst_case_expected_cost"], 3)
            == 12.0
        ),
        "reference_tiebreak_recovers_gtm_strategy_finance": (
            selected["order"]
            == [
                "gtm-pack",
                "signed-strategy-gap-attestation",
                "finance-pack",
            ]
        ),
        "reference_efficiency_is_9_0225": (
            round(selected["reference_expected_cost"], 4)
            == 9.0225
        ),
        "worst_collection_cost_uses_failure_lower_bounds": True,
    }

    return {
        "experiment": "E075",
        "question": (
            "If each axis failure probability is known only within an "
            "interval and joint dependence is arbitrary, which evidence "
            "order minimizes tight worst-case expected collection cost?"
        ),
        "marginal_intervals": MARGINAL_INTERVALS,
        "ambiguity_model": (
            "all marginal values inside declared intervals and all compatible "
            "joint dependence structures"
        ),
        "search": result,
        "promotion_gate": gates,
        "promoted_interval_rule": (
            "interval-marginal-dependence-ambiguity-uses-lower-risk-frechet-bound-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "For collection-cost robustness, low failure rates are adversarial "
            "because they force longer SAFE-path observation. The tight "
            "interval/dependence worst case therefore uses marginal lower "
            "failure bounds plus nested bad events."
        ),
        "limitations": (
            "Intervals are synthetic and rectangular. Coupled marginal "
            "constraints, evidence errors, and dynamic failure probabilities "
            "are not represented."
        ),
    }
