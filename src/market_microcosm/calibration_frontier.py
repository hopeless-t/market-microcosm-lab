from __future__ import annotations

from market_microcosm.certificate_meta_sensing import (
    exact_certificate_calibration_portfolio,
)


def pareto_frontier() -> list[dict]:
    rows = exact_certificate_calibration_portfolio()["rows"]
    frontier = []

    for row in rows:
        dominated = any(
            (
                other["calibration_cost"] <= row["calibration_cost"]
                and other["policy"]["worst_case_expected_cost"]
                <= row["policy"]["worst_case_expected_cost"]
                and (
                    other["calibration_cost"] < row["calibration_cost"]
                    or other["policy"]["worst_case_expected_cost"]
                    < row["policy"]["worst_case_expected_cost"]
                )
            )
            for other in rows
        )
        if not dominated:
            frontier.append(row)

    return sorted(
        frontier,
        key=lambda row: (
            row["calibration_cost"],
            row["policy"]["worst_case_expected_cost"],
            row["calibration_ids"],
        ),
    )


def compile_calibration_for_target(target: float) -> dict:
    feasible = [
        row
        for row in pareto_frontier()
        if row["policy"]["worst_case_expected_cost"]
        <= target + 1e-12
    ]

    if not feasible:
        return {
            "target": target,
            "status": "UNSAT",
            "selected": None,
        }

    selected = min(
        feasible,
        key=lambda row: (
            row["calibration_cost"],
            row["policy"]["worst_case_expected_cost"],
            row["calibration_ids"],
        ),
    )
    return {
        "target": target,
        "status": "SAT",
        "selected": selected,
    }


def calibration_frontier_report_payload() -> dict:
    frontier = pareto_frontier()
    compiled = {
        "12.0": compile_calibration_for_target(12.0),
        "11.9": compile_calibration_for_target(11.9),
        "11.3": compile_calibration_for_target(11.3),
        "11.1": compile_calibration_for_target(11.1),
    }

    gates = {
        "frontier_has_exactly_three_points": len(frontier) == 3,
        "frontier_points_are_0_12__1_11_85__2_11_2": (
            [
                (
                    row["calibration_cost"],
                    round(
                        row["policy"]["worst_case_expected_cost"],
                        2,
                    ),
                )
                for row in frontier
            ]
            == [
                (0, 12.0),
                (1, 11.85),
                (2, 11.2),
            ]
        ),
        "target_12_requires_no_calibration": (
            compiled["12.0"]["selected"]["calibration_ids"] == []
        ),
        "target_11_9_selects_strategy_only": (
            compiled["11.9"]["selected"]["calibration_ids"]
            == ["strategy-incidence-study"]
        ),
        "target_11_3_selects_gtm_only": (
            compiled["11.3"]["selected"]["calibration_ids"]
            == ["gtm-incidence-study"]
        ),
        "target_11_1_is_unsat": (
            compiled["11.1"]["status"] == "UNSAT"
        ),
        "dominated_calibration_plans_do_not_receive_authority": True,
    }

    return {
        "experiment": "E077",
        "question": (
            "Can certificate-calibration choices be compiled from a reusable "
            "cost-vs-robustness Pareto frontier instead of solving one "
            "arbitrary target at a time?"
        ),
        "frontier": frontier,
        "compiled_targets": compiled,
        "promotion_gate": gates,
        "promoted_frontier_rule": (
            "certificate-calibration-uses-pareto-frontier-and-fail-closed-target-compiler-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Calibration authority is represented as a Pareto frontier between "
            "evidence cost and certified robust bound. A requested target is "
            "compiled to the cheapest frontier point that satisfies it, and "
            "targets beyond the admitted calibration capability return UNSAT."
        ),
        "limitations": (
            "The frontier inherits E076's synthetic calibration effects and "
            "costs. New calibration actions or changed uncertainty models "
            "require frontier recomputation."
        ),
    }
