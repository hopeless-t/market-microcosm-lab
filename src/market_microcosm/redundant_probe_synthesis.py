from __future__ import annotations

from itertools import combinations, product

from market_microcosm.lineage_probe_portfolio import (
    hypotheses,
    probes,
    signature,
)
from market_microcosm.noisy_lineage_probes import hamming_distance


MAX_REPETITIONS_PER_PROBE = 5


def expanded_signature(
    hypothesis,
    repetition_counts: tuple[int, ...],
) -> tuple[bool, ...]:
    base = signature(hypothesis, probes())
    bits = []
    for value, count in zip(base, repetition_counts):
        bits.extend([value] * count)
    return tuple(bits)


def expanded_minimum_distance(
    repetition_counts: tuple[int, ...],
) -> int:
    signatures = [
        expanded_signature(hypothesis, repetition_counts)
        for hypothesis in hypotheses()
    ]
    return min(
        hamming_distance(left, right)
        for left, right in combinations(signatures, 2)
    )


def exact_redundancy_synthesis(
    *,
    required_distance: int = 5,
) -> dict:
    catalog = probes()
    candidates = []

    for counts in product(
        range(MAX_REPETITIONS_PER_PROBE + 1),
        repeat=len(catalog),
    ):
        if sum(counts) == 0:
            continue

        distance = expanded_minimum_distance(counts)
        if distance < required_distance:
            continue

        total_cost = sum(
            count * probe.cost
            for count, probe in zip(counts, catalog)
        )
        candidates.append(
            {
                "repetition_counts": {
                    probe.probe_id: count
                    for probe, count in zip(catalog, counts)
                },
                "channel_count": sum(counts),
                "total_cost": total_cost,
                "minimum_hamming_distance": distance,
            }
        )

    if not candidates:
        raise ValueError("no redundant design satisfies distance")

    selected = min(
        candidates,
        key=lambda row: (
            row["total_cost"],
            row["channel_count"],
            tuple(row["repetition_counts"].values()),
        ),
    )

    return {
        "required_distance": required_distance,
        "max_repetitions_per_probe": MAX_REPETITIONS_PER_PROBE,
        "candidate_count": len(candidates),
        "selected": selected,
    }


def nearest_hypothesis(
    observed: tuple[bool, ...],
    repetition_counts: tuple[int, ...],
) -> dict:
    rows = []
    for hypothesis in hypotheses():
        expected = expanded_signature(
            hypothesis,
            repetition_counts,
        )
        rows.append(
            {
                "hypothesis_id": hypothesis.hypothesis_id,
                "distance": hamming_distance(observed, expected),
            }
        )

    best_distance = min(row["distance"] for row in rows)
    best = [
        row for row in rows
        if row["distance"] == best_distance
    ]
    return {
        "unique": len(best) == 1,
        "decoded_hypothesis": (
            best[0]["hypothesis_id"]
            if len(best) == 1
            else None
        ),
        "best_distance": best_distance,
    }


def exhaustive_two_error_decode_check() -> dict:
    selected = exact_redundancy_synthesis()["selected"]
    catalog = probes()
    counts = tuple(
        selected["repetition_counts"][probe.probe_id]
        for probe in catalog
    )
    channel_count = sum(counts)

    checks = []
    for hypothesis in hypotheses():
        expected = expanded_signature(hypothesis, counts)

        error_sets = [tuple()]
        error_sets.extend((index,) for index in range(channel_count))
        error_sets.extend(
            combinations(range(channel_count), 2)
        )

        for error_indices in error_sets:
            observed = list(expected)
            for index in error_indices:
                observed[index] = not observed[index]

            decoded = nearest_hypothesis(
                tuple(observed),
                counts,
            )
            checks.append(
                {
                    "hypothesis_id": hypothesis.hypothesis_id,
                    "error_indices": list(error_indices),
                    "correct": (
                        decoded["unique"]
                        and decoded["decoded_hypothesis"]
                        == hypothesis.hypothesis_id
                    ),
                }
            )

    return {
        "channel_count": channel_count,
        "case_count": len(checks),
        "all_correct": all(row["correct"] for row in checks),
    }


def redundancy_synthesis_report_payload() -> dict:
    synthesis = exact_redundancy_synthesis()
    decode = exhaustive_two_error_decode_check()
    selected = synthesis["selected"]

    gates = {
        "expanded_measurement_design_restores_sat": (
            selected is not None
        ),
        "selected_distance_is_five": (
            selected["minimum_hamming_distance"] == 5
        ),
        "selected_channel_count_is_ten": (
            selected["channel_count"] == 10
        ),
        "selected_total_cost_is_twenty": (
            selected["total_cost"] == 20
        ),
        "selected_repetition_vector_matches_exact_reference": (
            selected["repetition_counts"]
            == {
                "ab": 1,
                "ac": 2,
                "ad": 2,
                "bc": 2,
                "bd": 2,
                "cd": 1,
            }
        ),
        "all_zero_one_two_error_cases_decode_correctly": (
            decode["all_correct"] is True
            and decode["case_count"] == 280
        ),
    }

    return {
        "experiment": "E055",
        "question": (
            "When the original six-probe measurement alphabet is UNSAT for "
            "two-error correction, can independent repeated measurement "
            "channels be synthesized to restore the required distance-five "
            "authority at minimum declared cost?"
        ),
        "synthesis": synthesis,
        "exhaustive_decode": decode,
        "promotion_gate": gates,
        "promoted_redundancy_rule": (
            "unsat-probe-robustness-may-expand-independent-measurement-channels-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "UNSAT now triggers measurement-design expansion rather than "
            "silent robustness downgrade. Independent repeated channels can "
            "increase hypothesis-code distance; the expanded design is then "
            "recompiled and exhaustively decoded against the declared error "
            "budget."
        ),
        "limitations": (
            "Repeated channels are assumed to have independent substitution "
            "errors. Shared sensors, transforms, operators, or upstream data "
            "can correlate repeated measurements and invalidate the expanded "
            "bit-error model."
        ),
    }
