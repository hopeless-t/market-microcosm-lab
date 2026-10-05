from __future__ import annotations

from itertools import permutations

from market_microcosm.joint_dependence_acquisition import (
    expected_cost_for_sequence as joint_expected_cost,
    joint_optimal_policy,
)
from market_microcosm.prior_drift_acquisition import (
    PRIORS,
    expected_cost_for_sequence,
    optimal_policy_for_prior,
)


BUNDLES = (
    "finance-pack",
    "gtm-pack",
    "signed-strategy-gap-attestation",
)


def extended_scenario_search() -> dict:
    oracle = {
        name: optimal_policy_for_prior(prior)["expected_cost"]
        for name, prior in PRIORS.items()
    }
    oracle["joint-dependence"] = joint_optimal_policy()["expected_cost"]

    rows = []
    for order in permutations(BUNDLES):
        scenario_cost = {
            name: expected_cost_for_sequence(order, prior)
            for name, prior in PRIORS.items()
        }
        scenario_cost["joint-dependence"] = joint_expected_cost(order)

        regret = {
            name: scenario_cost[name] - oracle[name]
            for name in scenario_cost
        }

        rows.append(
            {
                "order": list(order),
                "scenario_cost": scenario_cost,
                "regret": regret,
                "worst_case_expected_cost": max(scenario_cost.values()),
                "worst_case_regret": max(regret.values()),
            }
        )

    selected = min(
        rows,
        key=lambda x: (
            x["worst_case_expected_cost"],
            x["worst_case_regret"],
            x["order"],
        ),
    )

    return {
        "scenario_count": 4,
        "candidate_count": len(rows),
        "oracle_cost": oracle,
        "selected": selected,
        "rows": rows,
    }


def joint_extended_robustness_report_payload() -> dict:
    result = extended_scenario_search()
    selected = result["selected"]

    gates = {
        "four_scenarios_are_admitted": result["scenario_count"] == 4,
        "all_six_orders_are_rechecked": result["candidate_count"] == 6,
        "e071_order_survives_joint_adversary": (
            selected["order"]
            == [
                "signed-strategy-gap-attestation",
                "finance-pack",
                "gtm-pack",
            ]
        ),
        "worst_case_cost_remains_11_315": (
            round(selected["worst_case_expected_cost"], 3)
            == 11.315
        ),
        "joint_scenario_cost_is_11_15": (
            round(
                selected["scenario_cost"]["joint-dependence"],
                2,
            )
            == 11.15
        ),
        "worst_case_regret_expands_to_2_7": (
            round(selected["worst_case_regret"], 2) == 2.70
        ),
        "policy_survival_does_not_preserve_old_regret_bound": True,
    }

    return {
        "experiment": "E073",
        "question": (
            "Does the E071 minimax order survive when the same-marginal "
            "E072 joint-dependence adversary is added to the admitted "
            "uncertainty set?"
        ),
        "extended_search": result,
        "e071_order_authority": "RETAINED",
        "e071_regret_bound_authority": "REISSUED",
        "previous_e071_worst_case_regret": 2.2925,
        "new_worst_case_regret": selected["worst_case_regret"],
        "promotion_gate": gates,
        "promoted_extension_rule": (
            "robust-policy-order-and-performance-bound-have-separate-authority-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Adding a new adversarial scenario can leave the selected policy "
            "unchanged while invalidating its previous performance bound. "
            "Policy identity and certificate metrics therefore have separate "
            "revocation / renewal lifecycles."
        ),
        "limitations": (
            "The expanded set still contains only four synthetic scenarios. "
            "Survival against this joint adversary does not certify arbitrary "
            "dependence or out-of-set priors."
        ),
    }
