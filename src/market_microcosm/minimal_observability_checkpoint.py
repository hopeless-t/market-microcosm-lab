from __future__ import annotations


WINDOW_MONTHS = 6


def rolling_sum_from_arr(arr: float) -> float:
    return arr * WINDOW_MONTHS / 12.0


def reconstruct_newest_mrr(
    *,
    previous_arr: float,
    current_arr: float,
    outgoing_oldest_mrr: float,
) -> float:
    previous_sum = rolling_sum_from_arr(previous_arr)
    current_sum = rolling_sum_from_arr(current_arr)
    return current_sum - previous_sum + outgoing_oldest_mrr


def unresolved_pairs_without_boundary(
    *,
    previous_arr: float,
    current_arr: float,
    minimum_mrr: int = 0,
    maximum_mrr: int = 10,
) -> tuple[tuple[int, int], ...]:
    delta = (
        rolling_sum_from_arr(current_arr)
        - rolling_sum_from_arr(previous_arr)
    )

    pairs = []
    for outgoing in range(minimum_mrr, maximum_mrr + 1):
        for newest in range(minimum_mrr, maximum_mrr + 1):
            if abs((newest - outgoing) - delta) < 1e-12:
                pairs.append((outgoing, newest))

    return tuple(pairs)


def boundary_checkpoint_reference() -> dict:
    previous_window = (10, 8, 6, 4, 2, 0)
    newest_mrr = 2
    current_window = previous_window[1:] + (newest_mrr,)

    previous_arr = (
        sum(previous_window) / WINDOW_MONTHS * 12.0
    )
    current_arr = (
        sum(current_window) / WINDOW_MONTHS * 12.0
    )

    unresolved = unresolved_pairs_without_boundary(
        previous_arr=previous_arr,
        current_arr=current_arr,
    )
    reconstructed = reconstruct_newest_mrr(
        previous_arr=previous_arr,
        current_arr=current_arr,
        outgoing_oldest_mrr=previous_window[0],
    )

    return {
        "previous_window": list(previous_window),
        "current_window": list(current_window),
        "previous_arr": previous_arr,
        "current_arr": current_arr,
        "true_outgoing_oldest_mrr": previous_window[0],
        "true_newest_mrr": newest_mrr,
        "unresolved_pairs_without_boundary": [
            list(pair) for pair in unresolved
        ],
        "unresolved_pair_count": len(unresolved),
        "reconstructed_newest_mrr_with_boundary": reconstructed,
    }


def minimal_observability_checkpoint_report_payload() -> dict:
    reference = boundary_checkpoint_reference()

    gates = {
        "two_rolling_arr_values_remain_ambiguous": (
            reference["unresolved_pair_count"] > 1
        ),
        "ambiguity_includes_multiple_current_mrr_values": (
            len(
                {
                    pair[1]
                    for pair in reference[
                        "unresolved_pairs_without_boundary"
                    ]
                }
            )
            > 1
        ),
        "one_boundary_checkpoint_restores_exact_current_mrr": (
            reference[
                "reconstructed_newest_mrr_with_boundary"
            ]
            == reference["true_newest_mrr"]
        ),
        "checkpoint_is_one_scalar_not_full_path": True,
        "observation_contract_exposes_reconstruction_formula": True,
    }

    return {
        "experiment": "E041",
        "question": (
            "What is a minimal extra checkpoint that restores one-step "
            "current-state observability for a fixed-width rolling ARR?"
        ),
        "identity": (
            "S_t = S_(t-1) - outgoing_oldest_mrr + newest_mrr"
        ),
        "reference": reference,
        "promotion_gate": gates,
        "promoted_checkpoint_rule": (
            "rolling-window-boundary-checkpoint-restores-observability-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "For one-step reconstruction of the newest MRR from consecutive "
            "rolling ARR values, retain the outgoing boundary MRR. This single "
            "scalar checkpoint is sufficient; retaining the full six-month "
            "path is unnecessary for that reconstruction task."
        ),
        "limitations": (
            "The checkpoint restores the newest scalar under a known fixed "
            "window and exact metric definition. It does not reconstruct all "
            "interior months, separate product mixtures, or solve noisy/"
            "redefined metrics without additional state."
        ),
    }
