from __future__ import annotations

from functools import lru_cache

from market_microcosm.direct_evidence_acquisition import AXES, acquisitions
from market_microcosm.sequential_evidence_acquisition import BAD_PROBABILITY


AXIS_ORDER = (
    "cash_collection_gap",
    "fully_loaded_delivery_margin",
    "market_headroom",
    "downstream_funnel_success",
    "strategic_exit_value_gap",
)

JOINT_DISTRIBUTION = {
    (False, False, False, False, False): 0.37,
    (False, False, False, True, False): 0.18,
    (False, False, True, False, False): 0.05,
    (False, False, True, False, True): 0.25,
    (False, True, False, False, False): 0.10,
    (True, False, False, False, False): 0.05,
}

FROZEN_E069_PATH = (
    "gtm-pack",
    "signed-strategy-gap-attestation",
    "finance-pack",
)


def authorized_actions():
    return tuple(a for a in acquisitions() if a.authorized)


def marginal_bad_probability() -> dict[str, float]:
    return {
        axis: sum(
            probability
            for world, probability in JOINT_DISTRIBUTION.items()
            if world[AXIS_ORDER.index(axis)]
        )
        for axis in AXIS_ORDER
    }


def probability_all_safe(required_safe: frozenset[str]) -> float:
    return sum(
        probability
        for world, probability in JOINT_DISTRIBUTION.items()
        if all(
            not world[AXIS_ORDER.index(axis)]
            for axis in required_safe
        )
    )


def expected_cost_for_sequence(sequence: tuple[str, ...]) -> float:
    by_id = {a.acquisition_id: a for a in authorized_actions()}
    safe = frozenset()
    expected = 0.0

    for action_id in sequence:
        action = by_id[action_id]
        new_axes = action.direct_axes - safe
        if not new_axes:
            continue
        expected += probability_all_safe(safe) * action.cost
        safe = frozenset(safe | new_axes)

    if not AXES.issubset(safe):
        raise ValueError("sequence cannot certify SAFE")
    return expected


def joint_optimal_policy() -> dict:
    actions = authorized_actions()
    by_id = {a.acquisition_id: a for a in actions}

    @lru_cache(maxsize=None)
    def value(safe_axes: frozenset[str]) -> tuple[float, str | None]:
        if AXES.issubset(safe_axes):
            return 0.0, None

        denominator = probability_all_safe(safe_axes)
        best_cost = float("inf")
        best_action = None

        for action in actions:
            new_axes = action.direct_axes - safe_axes
            if not new_axes:
                continue

            next_safe = frozenset(safe_axes | new_axes)
            continue_probability = (
                probability_all_safe(next_safe) / denominator
            )
            continuation, _ = value(next_safe)
            candidate = action.cost + continue_probability * continuation

            if (
                candidate < best_cost - 1e-12
                or (
                    abs(candidate - best_cost) <= 1e-12
                    and (
                        best_action is None
                        or action.acquisition_id < best_action
                    )
                )
            ):
                best_cost = candidate
                best_action = action.acquisition_id

        return best_cost, best_action

    safe = frozenset()
    path = []
    initial_cost, initial_action = value(safe)

    while not AXES.issubset(safe):
        _, action_id = value(safe)
        if action_id is None:
            raise ValueError("policy ended before SAFE")
        path.append(action_id)
        safe = frozenset(safe | by_id[action_id].direct_axes)

    return {
        "expected_cost": initial_cost,
        "initial_action": initial_action,
        "safe_path": path,
    }


def joint_dependence_report_payload() -> dict:
    marginals = marginal_bad_probability()
    joint = JOINT_DISTRIBUTION[
        (False, False, True, False, True)
    ]
    independent_product = (
        marginals["market_headroom"]
        * marginals["strategic_exit_value_gap"]
    )

    frozen_cost = expected_cost_for_sequence(FROZEN_E069_PATH)
    optimal = joint_optimal_policy()
    regret = frozen_cost - optimal["expected_cost"]

    gates = {
        "joint_distribution_sums_to_one": (
            abs(sum(JOINT_DISTRIBUTION.values()) - 1.0) < 1e-12
        ),
        "marginals_match_e069_exactly": all(
            abs(marginals[axis] - BAD_PROBABILITY[axis]) < 1e-12
            for axis in AXIS_ORDER
        ),
        "headroom_exit_dependence_differs_from_independence": (
            round(joint, 3) == 0.25
            and round(independent_product, 3) == 0.075
        ),
        "frozen_e069_joint_cost_is_9_2": (
            round(frozen_cost, 2) == 9.20
        ),
        "joint_optimum_reorders_finance_before_strategy": (
            optimal["safe_path"]
            == [
                "gtm-pack",
                "finance-pack",
                "signed-strategy-gap-attestation",
            ]
        ),
        "joint_optimum_cost_is_8_45": (
            round(optimal["expected_cost"], 2) == 8.45
        ),
        "marginal_only_policy_regret_is_0_75": (
            round(regret, 2) == 0.75
        ),
    }

    return {
        "experiment": "E072",
        "question": (
            "Do identical marginal axis-failure probabilities identify the "
            "same sequential evidence policy when the joint dependence "
            "structure changes?"
        ),
        "marginals": marginals,
        "joint_distribution": [
            {
                "world": dict(zip(AXIS_ORDER, world)),
                "probability": probability,
            }
            for world, probability in JOINT_DISTRIBUTION.items()
        ],
        "dependence_witness": {
            "joint_headroom_and_exit_bad": joint,
            "independent_product": independent_product,
        },
        "frozen_e069": {
            "safe_path": list(FROZEN_E069_PATH),
            "expected_cost_under_joint": frozen_cost,
        },
        "joint_aware_optimum": optimal,
        "regret": regret,
        "promotion_gate": gates,
        "promoted_joint_rule": (
            "sequential-acquisition-requires-joint-failure-model-not-marginals-only-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Marginal failure probabilities do not identify a sequential "
            "acquisition policy. Joint dependence changes conditional risk "
            "after safe observations and can reorder later evidence requests "
            "even when every marginal remains unchanged."
        ),
        "limitations": (
            "The joint world is a finite synthetic counterexample. Production "
            "use needs evidence for dependence structure or a robust ambiguity "
            "set rather than assuming this particular joint distribution."
        ),
    }
