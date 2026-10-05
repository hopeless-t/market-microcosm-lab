from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class Spark:
    spark_id: str
    meaning: str
    candidate_destinations: tuple[str, ...]
    demanded: tuple[tuple[str, int], ...]


DESTINATION_COST = {
    "finite-ram-lab": 5,
    "next-generation-github": 4,
    "market-microcosm-lab": 4,
    "catfood-pcg-lab": 3,
    "catfood-semantic-forge": 5,
    "field-report-app": 6,
    "harness-component-economics": 3,
    "recursive-flourishing-lab": 4,
}


SPARKS = (
    Spark(
        "S1",
        "working-set",
        ("finite-ram-lab", "next-generation-github", "market-microcosm-lab", "catfood-pcg-lab"),
        (("finite-ram-lab", 9), ("next-generation-github", 7)),
    ),
    Spark(
        "S2",
        "working-set",
        ("market-microcosm-lab", "finite-ram-lab"),
        (("market-microcosm-lab", 5),),
    ),
    Spark(
        "S3",
        "workflow-dsl",
        ("catfood-semantic-forge", "market-microcosm-lab", "field-report-app"),
        (("catfood-semantic-forge", 8),),
    ),
    Spark(
        "S4",
        "workflow-dsl",
        ("market-microcosm-lab", "next-generation-github"),
        (("market-microcosm-lab", 6),),
    ),
    Spark(
        "S5",
        "resource-rebound",
        ("market-microcosm-lab", "finite-ram-lab", "harness-component-economics"),
        (("market-microcosm-lab", 9),),
    ),
    Spark(
        "S6",
        "proof-status",
        ("catfood-semantic-forge", "market-microcosm-lab", "next-generation-github"),
        (("catfood-semantic-forge", 7), ("market-microcosm-lab", 8)),
    ),
    Spark(
        "S7",
        "dormant-social-capital",
        ("market-microcosm-lab", "recursive-flourishing-lab"),
        (),
    ),
    Spark(
        "S8",
        "quiet-db-access",
        ("next-generation-github", "field-report-app"),
        (("field-report-app", 7),),
    ),
    Spark(
        "S9",
        "labor-transition",
        ("market-microcosm-lab", "recursive-flourishing-lab"),
        (("market-microcosm-lab", 8),),
    ),
    Spark(
        "S10",
        "labor-transition",
        ("recursive-flourishing-lab", "market-microcosm-lab"),
        (),
    ),
)


def demanded_edges() -> dict[tuple[str, str], int]:
    values: dict[tuple[str, str], int] = defaultdict(int)
    for spark in SPARKS:
        for destination, value in spark.demanded:
            values[(spark.meaning, destination)] += value
    return dict(values)


def _metrics(
    materialized: list[tuple[str, str]], *, canonical_reservoir: bool
) -> dict[str, int | float]:
    demand = demanded_edges()
    unique = set(materialized)
    covered = set(demand) & unique
    all_meanings = {spark.meaning for spark in SPARKS}
    demanded_meanings = {meaning for meaning, _ in demand}
    dormant_meanings = all_meanings - demanded_meanings

    total_possible_value = sum(demand.values())
    covered_value = sum(demand[edge] for edge in covered)

    return {
        "admitted_sparks": len(SPARKS),
        "canonical_meanings_retained": len(all_meanings) if canonical_reservoir else 0,
        "materializations": len(materialized),
        "unique_materializations": len(unique),
        "duplicate_materializations": len(materialized) - len(unique),
        "review_cost": sum(DESTINATION_COST[destination] for _, destination in materialized),
        "demand_edges": len(demand),
        "covered_demand_edges": len(covered),
        "demand_edge_coverage": len(covered) / len(demand),
        "decision_value_coverage": covered_value / total_possible_value,
        "canonical_dormant_meanings_retained": len(dormant_meanings) if canonical_reservoir else 0,
    }


def direct_fanout() -> dict[str, int | float]:
    materialized = [
        (spark.meaning, destination)
        for spark in SPARKS
        for destination in spark.candidate_destinations
    ]
    return _metrics(materialized, canonical_reservoir=False)


def hard_one_projection_per_spark() -> dict[str, int | float]:
    materialized = [
        (spark.meaning, spark.candidate_destinations[0])
        for spark in SPARKS
    ]
    return _metrics(materialized, canonical_reservoir=False)


def canonical_on_demand() -> dict[str, int | float]:
    materialized = list(demanded_edges())
    return _metrics(materialized, canonical_reservoir=True)


def canonical_exact_budget(review_budget: int = 30) -> dict[str, int | float]:
    demand = demanded_edges()
    edges = sorted(demand)
    best: tuple[int, int, tuple[tuple[str, str], ...]] | None = None

    for size in range(len(edges) + 1):
        for candidate in combinations(edges, size):
            cost = sum(DESTINATION_COST[destination] for _, destination in candidate)
            if cost > review_budget:
                continue
            value = sum(demand[edge] for edge in candidate)
            rank = (value, -cost, candidate)
            if best is None or rank > best:
                best = rank

    assert best is not None
    selected = list(best[2])
    result = _metrics(selected, canonical_reservoir=True)
    result["review_budget"] = review_budget
    result["budget_slack"] = review_budget - int(result["review_cost"])
    return result


def rpe001_report_payload() -> dict:
    direct = direct_fanout()
    hard_cap = hard_one_projection_per_spark()
    on_demand = canonical_on_demand()
    budgeted = canonical_exact_budget()

    direct_cost = int(direct["review_cost"])
    on_demand_cost = int(on_demand["review_cost"])

    gates = {
        "curiosity_admission_unchanged": all(
            result["admitted_sparks"] == len(SPARKS)
            for result in (direct, hard_cap, on_demand, budgeted)
        ),
        "on_demand_preserves_all_current_demand": on_demand["demand_edge_coverage"] == 1.0,
        "on_demand_reduces_review_cost": on_demand_cost < direct_cost,
        "on_demand_removes_duplicate_materialization": on_demand["duplicate_materializations"] == 0,
        "hard_cap_demonstrates_suppression_failure": hard_cap["demand_edge_coverage"] < 1.0,
        "budgeted_policy_respects_review_budget": budgeted["review_cost"] <= budgeted["review_budget"],
        "canonical_policy_retains_dormant_option": on_demand["canonical_dormant_meanings_retained"] > 0,
    }

    return {
        "experiment": "RPE-001",
        "title": "Curiosity admission vs downstream materialization",
        "fixture": {
            "sparks": len(SPARKS),
            "canonical_meanings": len({spark.meaning for spark in SPARKS}),
            "current_demand_edges": len(demanded_edges()),
            "review_budget": 30,
        },
        "policies": {
            "direct_fanout": direct,
            "hard_one_projection_per_spark": hard_cap,
            "canonical_on_demand": on_demand,
            "canonical_exact_budget": budgeted,
        },
        "comparison": {
            "on_demand_review_cost_reduction_vs_direct_pct": round(
                100.0 * (direct_cost - on_demand_cost) / direct_cost, 3
            ),
            "hard_cap_coverage_loss_pct": round(
                100.0 * (1.0 - float(hard_cap["demand_edge_coverage"])), 3
            ),
            "budgeted_decision_value_coverage_pct": round(
                100.0 * float(budgeted["decision_value_coverage"]), 3
            ),
        },
        "promotion_gate": gates,
        "candidate_rule": "ADMIT_CURIOSITY_FREELY_MATERIALIZE_DECISION_RELEVANT_PROJECTIONS_ON_DEMAND",
        "claim_ceiling": "DETERMINISTIC_SYNTHETIC_FIXTURE_ONLY_NO_REAL_REPOSITORY_PRODUCTIVITY_CLAIM",
    }
