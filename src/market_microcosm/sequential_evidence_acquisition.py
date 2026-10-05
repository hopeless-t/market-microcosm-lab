from __future__ import annotations

from functools import lru_cache
from math import prod

from market_microcosm.direct_evidence_acquisition import AXES, acquisitions


BAD_PROBABILITY = {
    "cash_collection_gap": 0.05,
    "fully_loaded_delivery_margin": 0.10,
    "market_headroom": 0.30,
    "downstream_funnel_success": 0.18,
    "strategic_exit_value_gap": 0.25,
}


def authorized_actions():
    return tuple(a for a in acquisitions() if a.authorized)


def all_new_axes_safe_probability(new_axes: frozenset[str]) -> float:
    return prod(1.0 - BAD_PROBABILITY[axis] for axis in new_axes)


@lru_cache(maxsize=None)
def optimal_expected_cost(safe_axes: frozenset[str]) -> tuple[float, str | None]:
    if AXES.issubset(safe_axes):
        return 0.0, None

    best_cost = float("inf")
    best_action = None

    for action in authorized_actions():
        new_axes = action.direct_axes - safe_axes
        if not new_axes:
            continue

        continue_probability = all_new_axes_safe_probability(new_axes)
        continuation_cost, _ = optimal_expected_cost(
            frozenset(safe_axes | new_axes)
        )
        expected = action.cost + continue_probability * continuation_cost

        if (
            expected < best_cost - 1e-12
            or (
                abs(expected - best_cost) <= 1e-12
                and (
                    best_action is None
                    or action.acquisition_id < best_action
                )
            )
        ):
            best_cost = expected
            best_action = action.acquisition_id

    return best_cost, best_action


def safe_path_policy() -> list[str]:
    safe = frozenset()
    path = []
    by_id = {a.acquisition_id: a for a in authorized_actions()}

    while not AXES.issubset(safe):
        _, action_id = optimal_expected_cost(safe)
        if action_id is None:
            raise ValueError("policy terminated before SAFE")
        path.append(action_id)
        safe = frozenset(safe | by_id[action_id].direct_axes)

    return path


def expected_cost_for_order(action_ids: tuple[str, ...]) -> float:
    by_id = {a.acquisition_id: a for a in authorized_actions()}
    safe = frozenset()
    survival = 1.0
    expected = 0.0

    for action_id in action_ids:
        action = by_id[action_id]
        new_axes = action.direct_axes - safe
        if not new_axes:
            continue
        expected += survival * action.cost
        survival *= all_new_axes_safe_probability(new_axes)
        safe = frozenset(safe | new_axes)

    if not AXES.issubset(safe):
        raise ValueError("order does not cover every SAFE path axis")
    return expected


def sequential_acquisition_report_payload() -> dict:
    optimal_cost, first_action = optimal_expected_cost(frozenset())
    path = safe_path_policy()

    cost_order = (
        "gtm-pack",
        "finance-pack",
        "signed-strategy-gap-attestation",
    )
    cost_order_expected = expected_cost_for_order(cost_order)

    gates = {
        "optimal_policy_starts_with_gtm_pack": first_action == "gtm-pack",
        "optimal_safe_path_is_gtm_strategy_finance": path
        == [
            "gtm-pack",
            "signed-strategy-gap-attestation",
            "finance-pack",
        ],
        "optimal_expected_cost_is_9_0225": round(optimal_cost, 4) == 9.0225,
        "cost_only_bundle_order_is_worse": (
            round(cost_order_expected, 5) == 9.32385
            and optimal_cost < cost_order_expected
        ),
        "optimal_expected_cost_beats_static_full_portfolio": optimal_cost < 14,
        "all_safe_path_still_costs_fourteen": sum(
            next(
                a.cost
                for a in authorized_actions()
                if a.acquisition_id == action_id
            )
            for action_id in path
        )
        == 14,
    }

    return {
        "experiment": "E069",
        "question": (
            "Without knowing which warning axis is bad in advance, what "
            "authorized observation order minimizes expected decision cost "
            "while preserving complete SAFE certification?"
        ),
        "bad_probability": BAD_PROBABILITY,
        "independence_assumption": True,
        "optimal_policy": {
            "initial_expected_cost": optimal_cost,
            "initial_action": first_action,
            "safe_path": path,
        },
        "baselines": {
            "static_e067_full_portfolio_cost": 14,
            "cost_only_bundle_order": list(cost_order),
            "cost_only_bundle_order_expected_cost": cost_order_expected,
        },
        "promotion_gate": gates,
        "promoted_sequential_rule": (
            "sequential-warning-acquisition-minimizes-expected-decision-cost-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Evidence acquisition becomes a sequential stopping policy. "
            "Actions are ordered by expected decision value, not collection "
            "cost alone; WARN can stop early while the all-safe path still "
            "collects the complete authorized direct contract."
        ),
        "limitations": (
            "Failure probabilities and their independence are synthetic. "
            "Changing priors, correlations, evidence costs, or authorization "
            "must trigger policy recompilation."
        ),
    }
