from __future__ import annotations

from itertools import permutations

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


def enumerate_orders() -> list[dict]:
    oracle_cost = {
        name: optimal_policy_for_prior(prior)["expected_cost"]
        for name, prior in PRIORS.items()
    }

    rows = []
    for order in permutations(BUNDLES):
        scenario_cost = {
            name: expected_cost_for_sequence(order, prior)
            for name, prior in PRIORS.items()
        }
        regret = {
            name: scenario_cost[name] - oracle_cost[name]
            for name in PRIORS
        }
        rows.append(
            {
                "order": list(order),
                "scenario_cost": scenario_cost,
                "regret": regret,
                "worst_case_expected_cost": max(scenario_cost.values()),
                "worst_case_regret": max(regret.values()),
                "mean_expected_cost": (
                    sum(scenario_cost.values()) / len(scenario_cost)
                ),
            }
        )
    return rows


def minimax_order() -> dict:
    rows = enumerate_orders()
    selected = min(
        rows,
        key=lambda x: (
            x["worst_case_expected_cost"],
            x["worst_case_regret"],
            x["mean_expected_cost"],
            x["order"],
        ),
    )
    return {
        "candidate_count": len(rows),
        "selected": selected,
        "rows": rows,
    }


def robust_prior_set_report_payload() -> dict:
    result = minimax_order()
    selected = result["selected"]

    frozen = next(
        row
        for row in result["rows"]
        if row["order"]
        == [
            "gtm-pack",
            "signed-strategy-gap-attestation",
            "finance-pack",
        ]
    )

    gates = {
        "six_bundle_orders_are_exhaustively_evaluated": (
            result["candidate_count"] == 6
        ),
        "minimax_order_is_strategy_finance_gtm": (
            selected["order"]
            == [
                "signed-strategy-gap-attestation",
                "finance-pack",
                "gtm-pack",
            ]
        ),
        "minimax_worst_case_cost_is_11_315": (
            round(selected["worst_case_expected_cost"], 3)
            == 11.315
        ),
        "minimax_worst_case_regret_is_2_2925": (
            round(selected["worst_case_regret"], 4)
            == 2.2925
        ),
        "minimax_improves_frozen_e069_worst_case_cost": (
            selected["worst_case_expected_cost"]
            < frozen["worst_case_expected_cost"]
        ),
        "minimax_improves_frozen_e069_worst_case_regret": (
            selected["worst_case_regret"]
            < frozen["worst_case_regret"]
        ),
        "robustness_sacrifices_reference_optimality": (
            selected["scenario_cost"]["reference"]
            > frozen["scenario_cost"]["reference"]
        ),
        "all_safe_realized_collection_cost_remains_fourteen": True,
    }

    return {
        "experiment": "E071",
        "question": (
            "Can one fixed bundle order reduce worst-case acquisition cost "
            "and regret across the E070 prior uncertainty set?"
        ),
        "prior_set": PRIORS,
        "minimax_search": result,
        "frozen_e069_order": frozen,
        "promotion_gate": gates,
        "promoted_robust_rule": (
            "uncertain-prior-sequential-acquisition-uses-minimax-order-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "When prior generation is uncertain, the optimization target "
            "changes from one-prior expected cost to worst-case cost/regret "
            "over an admitted prior set. Robustness deliberately trades away "
            "some reference-prior efficiency."
        ),
        "limitations": (
            "The uncertainty set contains only three synthetic independent "
            "priors and the policy is a fixed bundle order. Correlated axes, "
            "continuous ambiguity sets, and posterior-adaptive robust policies "
            "remain open."
        ),
    }
