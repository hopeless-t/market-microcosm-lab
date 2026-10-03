from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SurfaceBenchmark:
    pair_key: str
    mechanism_name: str
    monotonicity_violations: int
    exhaustive_queries: int
    adaptive_queries: int
    query_savings_fraction: float
    classification_accuracy: float
    frontier_exact: bool
    exhaustive_frontier: tuple[int, int] | None
    adaptive_frontier: tuple[int, int] | None
    exhaustive_interaction_only_cells: int
    adaptive_interaction_only_cells: int
    interaction_only_count_exact: bool


def _pair_key(axis_a: str, axis_b: str) -> str:
    return f"{axis_a}__{axis_b}"


def _surface_rows(report: dict, *, pair_key: str, mechanism_name: str) -> tuple[dict, ...]:
    axis_a, axis_b = pair_key.split("__", maxsplit=1)
    return tuple(
        row
        for row in report["cells"]
        if row["axis_a"] == axis_a
        and row["axis_b"] == axis_b
        and row["mechanism_name"] == mechanism_name
    )


def failure_surface(
    report: dict,
    *,
    pair_key: str,
    mechanism_name: str,
    survival_threshold: float = 0.90,
) -> dict[tuple[int, int], bool]:
    rows = _surface_rows(report, pair_key=pair_key, mechanism_name=mechanism_name)
    return {
        (int(row["level_a"]), int(row["level_b"])): (
            float(row["survival_rate"]) < survival_threshold
        )
        for row in rows
    }


def monotonicity_violations(
    surface: dict[tuple[int, int], bool],
    *,
    max_level: int,
) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    violations: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for (level_a, level_b), failed in surface.items():
        if failed:
            for higher_a in range(level_a, max_level + 1):
                for higher_b in range(level_b, max_level + 1):
                    target = (higher_a, higher_b)
                    if target in surface and not surface[target]:
                        violations.add(((level_a, level_b), target))
        else:
            for lower_a in range(level_a + 1):
                for lower_b in range(level_b + 1):
                    target = (lower_a, lower_b)
                    if target in surface and surface[target]:
                        violations.add((target, (level_a, level_b)))
    return tuple(sorted(violations))


def staircase_inference(
    surface: dict[tuple[int, int], bool],
    *,
    max_level: int,
) -> tuple[
    tuple[tuple[int, int], ...],
    dict[int, int],
    dict[tuple[int, int], bool],
]:
    queried: list[tuple[int, int]] = []
    thresholds: dict[int, int] = {}
    level_b = max_level

    for level_a in range(max_level + 1):
        if level_b < 0:
            thresholds[level_a] = 0
            continue
        while level_b >= 0:
            point = (level_a, level_b)
            queried.append(point)
            if surface[point]:
                level_b -= 1
                continue
            break
        thresholds[level_a] = level_b + 1

    inferred = {
        (level_a, candidate_b): candidate_b >= thresholds[level_a]
        for level_a in range(max_level + 1)
        for candidate_b in range(max_level + 1)
    }
    return tuple(queried), thresholds, inferred


def first_frontier(
    surface: dict[tuple[int, int], bool],
) -> tuple[int, int] | None:
    failing = [point for point, failed in surface.items() if failed]
    if not failing:
        return None
    return min(
        failing,
        key=lambda point: (
            point[0] + point[1],
            max(point),
            abs(point[0] - point[1]),
            point[0],
            point[1],
        ),
    )


def interaction_only_count(
    report: dict,
    *,
    pair_key: str,
    mechanism_name: str,
    inferred_surface: dict[tuple[int, int], bool],
    survival_threshold: float = 0.90,
) -> int:
    rows = _surface_rows(report, pair_key=pair_key, mechanism_name=mechanism_name)
    by_point = {
        (int(row["level_a"]), int(row["level_b"])): row
        for row in rows
    }
    count = 0
    for point, failed in inferred_surface.items():
        if not failed:
            continue
        row = by_point[point]
        if (
            float(row["single_a_survival"]) >= survival_threshold
            and float(row["single_b_survival"]) >= survival_threshold
        ):
            count += 1
    return count


def benchmark_surface(
    report: dict,
    *,
    pair_key: str,
    mechanism_name: str,
    max_level: int,
) -> SurfaceBenchmark:
    truth = failure_surface(report, pair_key=pair_key, mechanism_name=mechanism_name)
    violations = monotonicity_violations(truth, max_level=max_level)
    queried, _, inferred = staircase_inference(truth, max_level=max_level)

    total = len(truth)
    correct = sum(int(inferred[point] == failed) for point, failed in truth.items())
    truth_frontier = first_frontier(truth)
    inferred_frontier = first_frontier(inferred)

    truth_interaction_count = interaction_only_count(
        report,
        pair_key=pair_key,
        mechanism_name=mechanism_name,
        inferred_surface=truth,
    )
    inferred_interaction_count = interaction_only_count(
        report,
        pair_key=pair_key,
        mechanism_name=mechanism_name,
        inferred_surface=inferred,
    )

    return SurfaceBenchmark(
        pair_key=pair_key,
        mechanism_name=mechanism_name,
        monotonicity_violations=len(violations),
        exhaustive_queries=total,
        adaptive_queries=len(queried),
        query_savings_fraction=1.0 - len(queried) / total if total else 0.0,
        classification_accuracy=correct / total if total else 0.0,
        frontier_exact=truth_frontier == inferred_frontier,
        exhaustive_frontier=truth_frontier,
        adaptive_frontier=inferred_frontier,
        exhaustive_interaction_only_cells=truth_interaction_count,
        adaptive_interaction_only_cells=inferred_interaction_count,
        interaction_only_count_exact=truth_interaction_count == inferred_interaction_count,
    )


def adaptive_sampling_report_payload(report: dict) -> dict:
    max_level = int(report["grid_max_level"])
    pair_keys = [_pair_key(str(pair[0]), str(pair[1])) for pair in report["pairs"]]
    mechanism_names = sorted({str(row["mechanism_name"]) for row in report["cells"]})

    surfaces = tuple(
        benchmark_surface(
            report,
            pair_key=pair_key,
            mechanism_name=mechanism_name,
            max_level=max_level,
        )
        for pair_key in pair_keys
        for mechanism_name in mechanism_names
    )

    exhaustive_queries = sum(x.exhaustive_queries for x in surfaces)
    adaptive_queries = sum(x.adaptive_queries for x in surfaces)
    all_monotone = all(x.monotonicity_violations == 0 for x in surfaces)
    all_classified = all(x.classification_accuracy == 1.0 for x in surfaces)
    all_frontiers = all(x.frontier_exact for x in surfaces)
    all_interaction_counts = all(x.interaction_only_count_exact for x in surfaces)
    savings = 1.0 - adaptive_queries / exhaustive_queries if exhaustive_queries else 0.0

    promotion_gate = {
        "zero_monotonicity_violations": all_monotone,
        "exact_cell_classification": all_classified,
        "exact_frontier_recovery": all_frontiers,
        "exact_interaction_only_counts": all_interaction_counts,
        "query_savings_at_least_50_percent": savings >= 0.50,
    }

    return {
        "experiment": "E015",
        "source_experiment": "E014",
        "candidate": "monotone-staircase-boundary-sampler-v1",
        "surfaces": [asdict(x) for x in surfaces],
        "aggregate": {
            "surface_count": len(surfaces),
            "exhaustive_queries": exhaustive_queries,
            "adaptive_queries": adaptive_queries,
            "query_savings_fraction": savings,
            "mean_queries_per_surface": adaptive_queries / len(surfaces) if surfaces else 0.0,
            "classification_accuracy": (
                sum(x.classification_accuracy for x in surfaces) / len(surfaces)
                if surfaces else 0.0
            ),
            "frontier_exact_rate": (
                sum(int(x.frontier_exact) for x in surfaces) / len(surfaces)
                if surfaces else 0.0
            ),
            "monotonicity_violation_count": sum(
                x.monotonicity_violations for x in surfaces
            ),
        },
        "promotion_gate": promotion_gate,
        "promoted": all(promotion_gate.values()),
    }
