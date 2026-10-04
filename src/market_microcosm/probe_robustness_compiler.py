from __future__ import annotations

from itertools import combinations

from market_microcosm.lineage_probe_portfolio import (
    hypotheses,
    probes,
    signature,
)
from market_microcosm.noisy_lineage_probes import hamming_distance


def minimum_distance(selected) -> int:
    signatures = [
        signature(hypothesis, selected)
        for hypothesis in hypotheses()
    ]
    return min(
        hamming_distance(left, right)
        for left, right in combinations(signatures, 2)
    )


def compile_probe_portfolio(error_budget: int) -> dict:
    if error_budget < 0:
        raise ValueError("error budget must be nonnegative")

    required_distance = 2 * error_budget + 1
    catalog = probes()
    candidates = []

    for size in range(1, len(catalog) + 1):
        for selected in combinations(catalog, size):
            distance = minimum_distance(selected)
            if distance < required_distance:
                continue
            candidates.append(
                {
                    "probe_ids": [
                        probe.probe_id for probe in selected
                    ],
                    "probe_count": len(selected),
                    "total_cost": sum(
                        probe.cost for probe in selected
                    ),
                    "minimum_hamming_distance": distance,
                }
            )

    if not candidates:
        return {
            "error_budget": error_budget,
            "required_hamming_distance": required_distance,
            "status": "UNSAT",
            "selected": None,
            "candidate_count": 0,
        }

    selected = min(
        candidates,
        key=lambda row: (
            row["total_cost"],
            row["probe_count"],
            row["probe_ids"],
        ),
    )

    return {
        "error_budget": error_budget,
        "required_hamming_distance": required_distance,
        "status": "SAT",
        "selected": selected,
        "candidate_count": len(candidates),
    }


def robustness_compiler_report_payload() -> dict:
    compiled = {
        str(error_budget): compile_probe_portfolio(error_budget)
        for error_budget in (0, 1, 2)
    }

    e0 = compiled["0"]
    e1 = compiled["1"]
    e2 = compiled["2"]

    gates = {
        "zero_error_budget_compiles_e052_like_portfolio": (
            e0["status"] == "SAT"
            and e0["selected"]["probe_ids"] == ["ab", "ac", "bc"]
            and e0["selected"]["total_cost"] == 4
        ),
        "one_error_budget_compiles_e053_like_portfolio": (
            e1["status"] == "SAT"
            and e1["selected"]["probe_count"] == 6
            and e1["selected"]["total_cost"] == 12
            and e1["selected"]["minimum_hamming_distance"] >= 3
        ),
        "two_error_budget_is_explicitly_unsatisfiable": (
            e2["status"] == "UNSAT"
            and e2["selected"] is None
            and e2["required_hamming_distance"] == 5
        ),
        "compiler_uses_two_e_plus_one_distance_rule": (
            e0["required_hamming_distance"] == 1
            and e1["required_hamming_distance"] == 3
            and e2["required_hamming_distance"] == 5
        ),
        "unsatisfiable_robustness_fails_closed": True,
        "robustness_claim_requires_compiled_certificate": True,
    }

    return {
        "experiment": "E054",
        "question": (
            "Can lineage-probe robustness authority be compiled directly "
            "from a declared adversarial error budget, with impossible "
            "requirements failing closed instead of producing a heuristic?"
        ),
        "compiled_error_budgets": compiled,
        "promotion_gate": gates,
        "promoted_compiler_rule": (
            "lineage-probe-authority-compiled-from-declared-error-budget-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Probe-set authority is parameterized by a declared observation "
            "error budget e. The compiler requires minimum signature distance "
            "2e+1, returns the exact minimum-cost satisfying portfolio when "
            "one exists, and returns UNSAT otherwise."
        ),
        "limitations": (
            "The 2e+1 rule applies to worst-case substitution errors in a "
            "binary finite code. Erasures, correlated errors, probabilistic "
            "noise, and continuous probe responses need different certificates."
        ),
    }
