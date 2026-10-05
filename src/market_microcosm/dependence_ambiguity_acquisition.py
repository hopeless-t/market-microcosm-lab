from __future__ import annotations

from itertools import permutations

from market_microcosm.direct_evidence_acquisition import acquisitions
from market_microcosm.sequential_evidence_acquisition import (
    BAD_PROBABILITY,
    expected_cost_for_order as reference_expected_cost_for_order,
)


BUNDLES = (
    "finance-pack",
    "gtm-pack",
    "signed-strategy-gap-attestation",
)


def authorized_bundle_map():
    return {
        action.acquisition_id: action
        for action in acquisitions()
        if action.authorized and action.acquisition_id in BUNDLES
    }


def frechet_upper_all_safe(axes: frozenset[str]) -> float:
    if not axes:
        return 1.0
    return 1.0 - max(BAD_PROBABILITY[axis] for axis in axes)


def worst_case_expected_cost(order: tuple[str, ...]) -> float:
    by_id = authorized_bundle_map()
    observed = frozenset()
    expected = 0.0

    for action_id in order:
        action = by_id[action_id]
        expected += frechet_upper_all_safe(observed) * action.cost
        observed = frozenset(observed | action.direct_axes)

    return expected


def nested_bad_event_atoms() -> list[dict]:
    thresholds = sorted(set(BAD_PROBABILITY.values()))
    bounds = [0.0, *thresholds, 1.0]
    atoms = []

    for low, high in zip(bounds, bounds[1:]):
        if high <= low:
            continue
        midpoint = (low + high) / 2.0
        bad_axes = sorted(
            axis
            for axis, probability in BAD_PROBABILITY.items()
            if midpoint < probability
        )
        atoms.append(
            {
                "probability": high - low,
                "bad_axes": bad_axes,
            }
        )

    return atoms


def atom_marginals() -> dict[str, float]:
    rows = nested_bad_event_atoms()
    return {
        axis: sum(
            row["probability"]
            for row in rows
            if axis in row["bad_axes"]
        )
        for axis in BAD_PROBABILITY
    }


def atom_expected_cost(order: tuple[str, ...]) -> float:
    by_id = authorized_bundle_map()
    total = 0.0

    for atom in nested_bad_event_atoms():
        bad_axes = set(atom["bad_axes"])
        realized = 0.0

        for action_id in order:
            action = by_id[action_id]
            realized += action.cost
            if bad_axes.intersection(action.direct_axes):
                break

        total += atom["probability"] * realized

    return total


def dependence_ambiguity_search() -> dict:
    rows = []

    for order in permutations(BUNDLES):
        worst = worst_case_expected_cost(order)
        witness = atom_expected_cost(order)
        reference = reference_expected_cost_for_order(order)
        rows.append(
            {
                "order": list(order),
                "worst_case_expected_cost": worst,
                "nested_witness_expected_cost": witness,
                "reference_independent_expected_cost": reference,
                "bound_is_tight": abs(worst - witness) < 1e-12,
            }
        )

    best_worst = min(row["worst_case_expected_cost"] for row in rows)
    minimax = [
        row
        for row in rows
        if abs(row["worst_case_expected_cost"] - best_worst) < 1e-12
    ]
    selected = min(
        minimax,
        key=lambda row: (
            row["reference_independent_expected_cost"],
            row["order"],
        ),
    )

    return {
        "candidate_count": len(rows),
        "rows": rows,
        "minimax_tie_count": len(minimax),
        "selected": selected,
        "nested_witness_atoms": nested_bad_event_atoms(),
        "nested_witness_marginals": atom_marginals(),
    }


def dependence_ambiguity_report_payload() -> dict:
    result = dependence_ambiguity_search()
    selected = result["selected"]

    tied_orders = sorted(
        row["order"]
        for row in result["rows"]
        if abs(
            row["worst_case_expected_cost"]
            - selected["worst_case_expected_cost"]
        )
        < 1e-12
    )

    gates = {
        "all_six_orders_are_exhaustively_evaluated": (
            result["candidate_count"] == 6
        ),
        "nested_witness_preserves_all_marginals": all(
            abs(
                result["nested_witness_marginals"][axis]
                - BAD_PROBABILITY[axis]
            )
            < 1e-12
            for axis in BAD_PROBABILITY
        ),
        "frechet_bound_is_tight_for_every_order": all(
            row["bound_is_tight"] for row in result["rows"]
        ),
        "two_gtm_first_orders_tie_at_worst_case_eleven": (
            result["minimax_tie_count"] == 2
            and tied_orders
            == [
                [
                    "gtm-pack",
                    "finance-pack",
                    "signed-strategy-gap-attestation",
                ],
                [
                    "gtm-pack",
                    "signed-strategy-gap-attestation",
                    "finance-pack",
                ],
            ]
            and round(selected["worst_case_expected_cost"], 3) == 11.0
        ),
        "reference_efficiency_tiebreak_recovers_e069_order": (
            selected["order"]
            == [
                "gtm-pack",
                "signed-strategy-gap-attestation",
                "finance-pack",
            ]
        ),
        "selected_reference_cost_is_9_0225": (
            round(selected["reference_independent_expected_cost"], 4)
            == 9.0225
        ),
    }

    return {
        "experiment": "E074",
        "question": (
            "With the E069 marginals fixed but arbitrary joint dependence, "
            "which complete bundle order minimizes tight worst-case expected "
            "decision cost?"
        ),
        "marginals": BAD_PROBABILITY,
        "ambiguity_model": (
            "all joint distributions consistent with the fixed axis marginals"
        ),
        "search": result,
        "promotion_gate": gates,
        "promoted_ambiguity_rule": (
            "fixed-marginal-dependence-ambiguity-uses-frechet-minimax-order-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Dependence uncertainty can be handled without selecting one joint "
            "model. Frechet upper bounds provide tight prefix-safe probabilities, "
            "and a nested bad-event construction witnesses the worst case. "
            "Worst-case optimization leaves two GTM-first orders tied; reference "
            "efficiency breaks the tie in favor of the E069 order."
        ),
        "limitations": (
            "The ambiguity set fixes the E069 marginals exactly and varies only "
            "dependence. It does not include marginal drift, evidence error, or "
            "authorization/cost changes."
        ),
    }
