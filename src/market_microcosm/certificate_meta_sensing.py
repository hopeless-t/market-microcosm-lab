from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations

from market_microcosm.dependence_ambiguity_acquisition import BUNDLES
from market_microcosm.direct_evidence_acquisition import acquisitions
from market_microcosm.interval_dependence_ambiguity import (
    MARGINAL_INTERVALS,
)
from market_microcosm.sequential_evidence_acquisition import (
    expected_cost_for_order as reference_expected_cost_for_order,
)


TARGET_WORST_CASE_COST = 11.3


@dataclass(frozen=True)
class CalibrationAction:
    action_id: str
    cost: int
    lower_bound_updates: tuple[tuple[str, float], ...]


def calibration_actions() -> tuple[CalibrationAction, ...]:
    return (
        CalibrationAction(
            "gtm-incidence-study",
            2,
            (
                ("market_headroom", 0.28),
                ("downstream_funnel_success", 0.16),
            ),
        ),
        CalibrationAction(
            "strategy-incidence-study",
            1,
            (("strategic_exit_value_gap", 0.23),),
        ),
        CalibrationAction(
            "finance-incidence-study",
            1,
            (
                ("cash_collection_gap", 0.06),
                ("fully_loaded_delivery_margin", 0.12),
            ),
        ),
        CalibrationAction(
            "broad-incidence-study",
            4,
            (
                ("cash_collection_gap", 0.06),
                ("fully_loaded_delivery_margin", 0.12),
                ("market_headroom", 0.28),
                ("downstream_funnel_success", 0.16),
                ("strategic_exit_value_gap", 0.23),
            ),
        ),
    )


def updated_lower_bounds(
    selected: tuple[CalibrationAction, ...],
) -> dict[str, float]:
    lower = {
        axis: interval[0]
        for axis, interval in MARGINAL_INTERVALS.items()
    }
    for action in selected:
        for axis, value in action.lower_bound_updates:
            lower[axis] = max(lower[axis], value)
    return lower


def worst_case_order_cost(
    order: tuple[str, ...],
    lower: dict[str, float],
) -> float:
    by_id = {
        action.acquisition_id: action
        for action in acquisitions()
        if action.authorized and action.acquisition_id in BUNDLES
    }
    observed = frozenset()
    expected = 0.0

    for action_id in order:
        action = by_id[action_id]
        safe_upper = (
            1.0
            if not observed
            else 1.0 - max(lower[axis] for axis in observed)
        )
        expected += safe_upper * action.cost
        observed = frozenset(observed | action.direct_axes)

    return expected


def robust_policy_after_calibration(
    lower: dict[str, float],
) -> dict:
    rows = []
    for order in permutations(BUNDLES):
        rows.append(
            {
                "order": list(order),
                "worst_case_expected_cost": worst_case_order_cost(
                    order, lower
                ),
                "reference_expected_cost": (
                    reference_expected_cost_for_order(order)
                ),
            }
        )

    best = min(row["worst_case_expected_cost"] for row in rows)
    minimax = [
        row
        for row in rows
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
        "rows": rows,
        "selected": selected,
        "minimax_tie_count": len(minimax),
    }


def exact_certificate_calibration_portfolio() -> dict:
    catalog = calibration_actions()
    rows = []

    for count in range(len(catalog) + 1):
        for selected in combinations(catalog, count):
            lower = updated_lower_bounds(selected)
            policy = robust_policy_after_calibration(lower)
            rows.append(
                {
                    "calibration_ids": sorted(
                        action.action_id for action in selected
                    ),
                    "calibration_cost": sum(
                        action.cost for action in selected
                    ),
                    "lower_bounds": lower,
                    "policy": policy["selected"],
                    "meets_target": (
                        policy["selected"]["worst_case_expected_cost"]
                        <= TARGET_WORST_CASE_COST + 1e-12
                    ),
                }
            )

    satisfying = [row for row in rows if row["meets_target"]]
    if not satisfying:
        raise ValueError("no calibration portfolio meets target")

    selected = min(
        satisfying,
        key=lambda row: (
            row["calibration_cost"],
            row["policy"]["worst_case_expected_cost"],
            row["calibration_ids"],
        ),
    )

    return {
        "target_worst_case_cost": TARGET_WORST_CASE_COST,
        "candidate_count": len(rows),
        "selected": selected,
        "baseline": next(
            row for row in rows if not row["calibration_ids"]
        ),
        "rows": rows,
    }


def certificate_meta_sensing_report_payload() -> dict:
    result = exact_certificate_calibration_portfolio()
    selected = result["selected"]
    baseline = result["baseline"]

    gates = {
        "baseline_worst_case_is_twelve": (
            round(
                baseline["policy"]["worst_case_expected_cost"], 3
            )
            == 12.0
        ),
        "minimum_calibration_is_gtm_incidence_only": (
            selected["calibration_ids"]
            == ["gtm-incidence-study"]
        ),
        "minimum_calibration_cost_is_two": (
            selected["calibration_cost"] == 2
        ),
        "calibrated_worst_case_is_11_2": (
            round(
                selected["policy"]["worst_case_expected_cost"], 3
            )
            == 11.2
        ),
        "target_11_3_is_met": selected["meets_target"] is True,
        "selected_policy_remains_gtm_strategy_finance": (
            selected["policy"]["order"]
            == [
                "gtm-pack",
                "signed-strategy-gap-attestation",
                "finance-pack",
            ]
        ),
        "certificate_sensing_is_targeted_not_full_prior_recovery": True,
    }

    return {
        "experiment": "E076",
        "question": (
            "Which additional calibration evidence should be acquired at "
            "minimum cost to tighten the E075 robust collection-cost "
            "certificate below a declared target?"
        ),
        "calibration_search": result,
        "promotion_gate": gates,
        "promoted_meta_sensing_rule": (
            "acquire-minimum-calibration-evidence-to-meet-certificate-target-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Active sensing is applied to the certificate itself. The system "
            "does not estimate every uncertain prior equally; it acquires the "
            "minimum calibration evidence whose effect is sufficient to meet "
            "the declared robustness-bound target."
        ),
        "limitations": (
            "Calibration actions and their bound updates are synthetic. "
            "Production value-of-information requires real sampling designs, "
            "uncertainty propagation, and evidence acquisition costs."
        ),
    }
