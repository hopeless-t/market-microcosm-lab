from __future__ import annotations

from functools import lru_cache
from math import prod

from market_microcosm.direct_evidence_acquisition import AXES, acquisitions


PRIORS = {
    "reference": {
        "cash_collection_gap": 0.05,
        "fully_loaded_delivery_margin": 0.10,
        "market_headroom": 0.30,
        "downstream_funnel_success": 0.18,
        "strategic_exit_value_gap": 0.25,
    },
    "finance-shift": {
        "cash_collection_gap": 0.35,
        "fully_loaded_delivery_margin": 0.30,
        "market_headroom": 0.05,
        "downstream_funnel_success": 0.05,
        "strategic_exit_value_gap": 0.10,
    },
    "strategy-shift": {
        "cash_collection_gap": 0.05,
        "fully_loaded_delivery_margin": 0.05,
        "market_headroom": 0.05,
        "downstream_funnel_success": 0.05,
        "strategic_exit_value_gap": 0.50,
    },
}

FROZEN_E069_SAFE_PATH = (
    "gtm-pack",
    "signed-strategy-gap-attestation",
    "finance-pack",
)


def authorized_actions():
    return tuple(a for a in acquisitions() if a.authorized)


def expected_cost_for_sequence(
    sequence: tuple[str, ...],
    prior: dict[str, float],
) -> float:
    by_id = {a.acquisition_id: a for a in authorized_actions()}
    safe = frozenset()
    survival = 1.0
    expected = 0.0

    for action_id in sequence:
        action = by_id[action_id]
        new_axes = action.direct_axes - safe
        if not new_axes:
            continue
        expected += survival * action.cost
        survival *= prod(1.0 - prior[axis] for axis in new_axes)
        safe = frozenset(safe | new_axes)

    if not AXES.issubset(safe):
        raise ValueError("sequence cannot certify SAFE")
    return expected


def optimal_policy_for_prior(prior: dict[str, float]) -> dict:
    actions = authorized_actions()
    by_id = {a.acquisition_id: a for a in actions}

    @lru_cache(maxsize=None)
    def value(safe_axes: frozenset[str]) -> tuple[float, str | None]:
        if AXES.issubset(safe_axes):
            return 0.0, None

        best_cost = float("inf")
        best_action = None

        for action in actions:
            new_axes = action.direct_axes - safe_axes
            if not new_axes:
                continue

            continue_probability = prod(
                1.0 - prior[axis] for axis in new_axes
            )
            continuation, _ = value(
                frozenset(safe_axes | new_axes)
            )
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


def prior_drift_report_payload() -> dict:
    rows = {}
    threshold = 1.0

    for name, prior in PRIORS.items():
        frozen_cost = expected_cost_for_sequence(
            FROZEN_E069_SAFE_PATH,
            prior,
        )
        reoptimized = optimal_policy_for_prior(prior)
        regret = frozen_cost - reoptimized["expected_cost"]

        rows[name] = {
            "prior": prior,
            "frozen_e069_expected_cost": frozen_cost,
            "reoptimized": reoptimized,
            "regret": regret,
            "exceeds_revocation_threshold": regret > threshold,
        }

    gates = {
        "reference_policy_remains_optimal_under_reference_prior": (
            round(rows["reference"]["regret"], 8) == 0.0
        ),
        "finance_shift_changes_first_action_to_finance_pack": (
            rows["finance-shift"]["reoptimized"]["initial_action"]
            == "finance-pack"
        ),
        "finance_shift_regret_exceeds_three_point_seven": (
            rows["finance-shift"]["regret"] > 3.7
        ),
        "strategy_shift_changes_first_action_to_strategy": (
            rows["strategy-shift"]["reoptimized"]["initial_action"]
            == "signed-strategy-gap-attestation"
        ),
        "strategy_shift_regret_exceeds_one_point_five": (
            rows["strategy-shift"]["regret"] > 1.5
        ),
        "both_shifted_generations_revoke_frozen_policy": (
            rows["finance-shift"]["exceeds_revocation_threshold"]
            and rows["strategy-shift"]["exceeds_revocation_threshold"]
        ),
    }

    return {
        "experiment": "E070",
        "question": (
            "Does E069 sequential-policy authority survive a change in the "
            "declared warning-axis failure distribution?"
        ),
        "frozen_policy": list(FROZEN_E069_SAFE_PATH),
        "revocation_regret_threshold": threshold,
        "scenarios": rows,
        "e069_policy_authority_under_shift": "REVOKED",
        "promotion_gate": gates,
        "promoted_prior_rule": (
            "sequential-acquisition-policy-authority-is-prior-generation-scoped-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Sequential acquisition authority is scoped to the prior "
            "generation that earned it. Distribution drift can change the "
            "optimal first observation and create material regret, so the "
            "policy must be recompiled or revoked."
        ),
        "limitations": (
            "The scenario priors are synthetic and preserve independent axes. "
            "Correlated failures, uncertain priors, and posterior learning "
            "require a stronger robust or Bayesian policy layer."
        ),
    }
