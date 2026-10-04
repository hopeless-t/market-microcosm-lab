from __future__ import annotations

from itertools import combinations

from market_microcosm.lineage_probe_portfolio import (
    hypotheses,
    probes,
    signature,
)


def hamming_distance(
    left: tuple[bool, ...],
    right: tuple[bool, ...],
) -> int:
    return sum(a != b for a, b in zip(left, right))


def minimum_signature_distance(
    selected,
) -> int:
    signatures = [
        signature(hypothesis, selected)
        for hypothesis in hypotheses()
    ]
    return min(
        hamming_distance(left, right)
        for left, right in combinations(signatures, 2)
    )


def exact_one_error_tolerant_portfolio() -> dict:
    catalog = probes()
    candidates: list[dict] = []

    for size in range(1, len(catalog) + 1):
        for selected in combinations(catalog, size):
            distance = minimum_signature_distance(selected)
            if distance < 3:
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
        raise ValueError("no one-error-tolerant portfolio")

    selected = min(
        candidates,
        key=lambda row: (
            row["total_cost"],
            row["probe_count"],
            row["probe_ids"],
        ),
    )

    return {
        "candidate_count": len(candidates),
        "selected": selected,
    }


def nearest_hypothesis(
    observed: tuple[bool, ...],
    selected,
) -> dict:
    distances = []
    for hypothesis in hypotheses():
        expected = signature(hypothesis, selected)
        distances.append(
            {
                "hypothesis_id": hypothesis.hypothesis_id,
                "distance": hamming_distance(observed, expected),
            }
        )

    best_distance = min(row["distance"] for row in distances)
    best = [
        row for row in distances
        if row["distance"] == best_distance
    ]

    return {
        "best_distance": best_distance,
        "unique": len(best) == 1,
        "decoded_hypothesis": (
            best[0]["hypothesis_id"]
            if len(best) == 1
            else None
        ),
        "distances": distances,
    }


def exhaustive_single_error_decode_check() -> dict:
    selected = probes()
    checks = []

    for hypothesis in hypotheses():
        expected = signature(hypothesis, selected)

        variants = [("no-error", expected)]
        for index in range(len(expected)):
            corrupted = list(expected)
            corrupted[index] = not corrupted[index]
            variants.append(
                (f"flip-{index}", tuple(corrupted))
            )

        for error_id, observed in variants:
            decoded = nearest_hypothesis(observed, selected)
            checks.append(
                {
                    "hypothesis_id": hypothesis.hypothesis_id,
                    "error_id": error_id,
                    "decoded_hypothesis": decoded[
                        "decoded_hypothesis"
                    ],
                    "best_distance": decoded["best_distance"],
                    "unique": decoded["unique"],
                    "correct": (
                        decoded["unique"]
                        and decoded["decoded_hypothesis"]
                        == hypothesis.hypothesis_id
                    ),
                }
            )

    return {
        "case_count": len(checks),
        "all_correct": all(row["correct"] for row in checks),
        "checks": checks,
    }


def minimal_portfolio_noise_counterexample() -> dict:
    selected = tuple(
        probe
        for probe in probes()
        if probe.probe_id in {"ab", "ac", "bc"}
    )
    none = next(
        hypothesis
        for hypothesis in hypotheses()
        if hypothesis.hypothesis_id == "none"
    )
    bcd = next(
        hypothesis
        for hypothesis in hypotheses()
        if hypothesis.hypothesis_id == "shared-bcd"
    )

    none_signature = signature(none, selected)
    bcd_signature = signature(bcd, selected)

    corrupted = list(none_signature)
    corrupted[2] = not corrupted[2]
    corrupted_tuple = tuple(corrupted)

    return {
        "selected_probe_ids": [
            probe.probe_id for probe in selected
        ],
        "minimum_hamming_distance": minimum_signature_distance(
            selected
        ),
        "true_hypothesis": "none",
        "true_signature": list(none_signature),
        "single_error_observation": list(corrupted_tuple),
        "confusable_hypothesis": "shared-bcd",
        "confusable_signature": list(bcd_signature),
        "single_error_causes_exact_alias": (
            corrupted_tuple == bcd_signature
        ),
    }


def noisy_lineage_probe_report_payload() -> dict:
    minimal = minimal_portfolio_noise_counterexample()
    robust = exact_one_error_tolerant_portfolio()
    decode = exhaustive_single_error_decode_check()

    gates = {
        "e052_minimal_portfolio_has_distance_one": (
            minimal["minimum_hamming_distance"] == 1
        ),
        "single_probe_error_can_alias_wrong_hypothesis": (
            minimal["single_error_causes_exact_alias"] is True
        ),
        "one_error_tolerance_requires_distance_three": (
            robust["selected"]["minimum_hamming_distance"] >= 3
        ),
        "exact_robust_portfolio_uses_all_six_probes": (
            robust["selected"]["probe_count"] == 6
        ),
        "robust_portfolio_cost_is_twelve": (
            robust["selected"]["total_cost"] == 12
        ),
        "all_single_error_cases_decode_correctly": (
            decode["all_correct"] is True
        ),
    }

    return {
        "experiment": "E053",
        "question": (
            "Does the minimum-cost noiseless lineage-probe portfolio remain "
            "safe under one probe-observation error, and what exact portfolio "
            "is required to correct any single error in the reference world?"
        ),
        "e052_noise_counterexample": minimal,
        "one_error_tolerant_search": robust,
        "exhaustive_single_error_decode": decode,
        "promotion_gate": gates,
        "promoted_noise_rule": (
            "lineage-probe-error-tolerance-requires-distance-three-signatures-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Lineage experiment design now separates identification efficiency "
            "from error-correcting robustness. Minimum-cost noiseless probe "
            "sets cannot inherit noise tolerance without an explicit signature "
            "distance certificate."
        ),
        "limitations": (
            "The reference corrects one binary probe error with a finite "
            "hypothesis code. Real probes can have correlated, asymmetric, or "
            "continuous noise and may require repetition or probabilistic "
            "decoding rather than Hamming nearest-neighbor recovery."
        ),
    }
