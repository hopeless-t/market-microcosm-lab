from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

from market_microcosm.research_portfolio_ecology import DESTINATION_COST


@dataclass(frozen=True)
class SemanticSpark:
    spark_id: str
    true_meaning: str
    surface_topic: str
    invariant_key: str
    demanded: tuple[tuple[str, int], ...]


SEMANTIC_SPARKS = (
    SemanticSpark(
        "A1",
        "working-set",
        "memory",
        "bounded-working-set",
        (("finite-ram-lab", 9), ("next-generation-github", 7)),
    ),
    SemanticSpark(
        "A2",
        "working-set",
        "cache",
        "bounded-working-set",
        (("finite-ram-lab", 6), ("market-microcosm-lab", 5)),
    ),
    SemanticSpark(
        "B1",
        "workflow-dsl",
        "workflow",
        "executable-workflow",
        (("catfood-semantic-forge", 8), ("market-microcosm-lab", 6)),
    ),
    SemanticSpark(
        "B2",
        "workflow-dsl",
        "workflow",
        "executable-workflow",
        (("catfood-semantic-forge", 4),),
    ),
    SemanticSpark(
        "C1",
        "resource-rebound",
        "efficiency",
        "rebound-resource-budget",
        (("market-microcosm-lab", 9),),
    ),
    SemanticSpark(
        "D1",
        "proof-status",
        "efficiency",
        "epistemic-proof-status",
        (("market-microcosm-lab", 8),),
    ),
    SemanticSpark(
        "E1",
        "labor-transition",
        "transition",
        "human-transition",
        (("market-microcosm-lab", 8), ("recursive-flourishing-lab", 6)),
    ),
    SemanticSpark(
        "E2",
        "labor-transition",
        "transition",
        "human-transition",
        (("market-microcosm-lab", 4),),
    ),
)


def _ground_truth_map() -> dict[str, str]:
    return {spark.spark_id: f"truth:{spark.true_meaning}" for spark in SEMANTIC_SPARKS}


def _surface_topic_map() -> dict[str, str]:
    return {spark.spark_id: f"topic:{spark.surface_topic}" for spark in SEMANTIC_SPARKS}


def _no_merge_map() -> dict[str, str]:
    return {spark.spark_id: f"spark:{spark.spark_id}" for spark in SEMANTIC_SPARKS}


def _invariant_guard_map() -> dict[str, str]:
    return {spark.spark_id: f"invariant:{spark.invariant_key}" for spark in SEMANTIC_SPARKS}


def _evaluate(cluster_map: dict[str, str]) -> dict[str, int | float | list[str]]:
    sparks_by_id = {spark.spark_id: spark for spark in SEMANTIC_SPARKS}
    members: dict[str, list[SemanticSpark]] = defaultdict(list)
    for spark_id, cluster in cluster_map.items():
        members[cluster].append(sparks_by_id[spark_id])

    false_merge_pairs = 0
    ambiguous_clusters: list[str] = []
    for cluster, cluster_members in members.items():
        meanings = {spark.true_meaning for spark in cluster_members}
        if len(meanings) > 1:
            ambiguous_clusters.append(cluster)
        for left, right in combinations(cluster_members, 2):
            if left.true_meaning != right.true_meaning:
                false_merge_pairs += 1

    clusters_by_true_meaning: dict[str, set[str]] = defaultdict(set)
    for spark in SEMANTIC_SPARKS:
        clusters_by_true_meaning[spark.true_meaning].add(cluster_map[spark.spark_id])
    false_split_meanings = sorted(
        meaning for meaning, clusters in clusters_by_true_meaning.items() if len(clusters) > 1
    )

    materialized = {
        (cluster_map[spark.spark_id], destination)
        for spark in SEMANTIC_SPARKS
        for destination, _ in spark.demanded
    }
    review_cost = sum(DESTINATION_COST[destination] for _, destination in materialized)

    total_value = sum(value for spark in SEMANTIC_SPARKS for _, value in spark.demanded)
    verified_value = 0
    for spark in SEMANTIC_SPARKS:
        cluster = cluster_map[spark.spark_id]
        cluster_meanings = {member.true_meaning for member in members[cluster]}
        if len(cluster_meanings) == 1:
            verified_value += sum(value for _, value in spark.demanded)

    projection_clusters_by_truth_edge: dict[tuple[str, str], set[str]] = defaultdict(set)
    for spark in SEMANTIC_SPARKS:
        for destination, _ in spark.demanded:
            projection_clusters_by_truth_edge[(spark.true_meaning, destination)].add(
                cluster_map[spark.spark_id]
            )
    duplicate_semantic_projections = sum(
        max(0, len(clusters) - 1) for clusters in projection_clusters_by_truth_edge.values()
    )

    return {
        "canonical_objects": len(members),
        "materializations": len(materialized),
        "review_cost": review_cost,
        "false_merge_pairs": false_merge_pairs,
        "ambiguous_cluster_count": len(ambiguous_clusters),
        "ambiguous_clusters": sorted(ambiguous_clusters),
        "false_split_meaning_count": len(false_split_meanings),
        "false_split_meanings": false_split_meanings,
        "duplicate_semantic_projections": duplicate_semantic_projections,
        "nominal_decision_value_coverage": 1.0,
        "verified_decision_value_coverage": verified_value / total_value,
        "semantic_value_loss": 1.0 - (verified_value / total_value),
    }


def rpe002_report_payload() -> dict:
    reference = _evaluate(_ground_truth_map())
    topic = _evaluate(_surface_topic_map())
    no_merge = _evaluate(_no_merge_map())
    guarded = _evaluate(_invariant_guard_map())

    gates = {
        "surface_topic_creates_false_merge": topic["false_merge_pairs"] > 0,
        "surface_topic_creates_false_split": topic["false_split_meaning_count"] > 0,
        "nominal_coverage_can_hide_semantic_loss": (
            topic["nominal_decision_value_coverage"] == 1.0
            and topic["verified_decision_value_coverage"] < 1.0
        ),
        "no_merge_is_safe_but_more_expensive": (
            no_merge["false_merge_pairs"] == 0
            and no_merge["verified_decision_value_coverage"] == 1.0
            and no_merge["review_cost"] > reference["review_cost"]
        ),
        "invariant_guard_avoids_false_merge": guarded["false_merge_pairs"] == 0,
        "invariant_guard_avoids_false_split": guarded["false_split_meaning_count"] == 0,
        "invariant_guard_preserves_verified_value": guarded["verified_decision_value_coverage"] == 1.0,
        "invariant_guard_matches_reference_cost_in_fixture": guarded["review_cost"] == reference["review_cost"],
    }

    return {
        "experiment": "RPE-002",
        "title": "Semantic canonicalization adversary",
        "fixture": {
            "sparks": len(SEMANTIC_SPARKS),
            "true_meanings": len({spark.true_meaning for spark in SEMANTIC_SPARKS}),
            "total_decision_value": sum(
                value for spark in SEMANTIC_SPARKS for _, value in spark.demanded
            ),
        },
        "policies": {
            "ground_truth_reference": reference,
            "surface_topic_canonicalizer": topic,
            "no_merge_fail_closed": no_merge,
            "invariant_guarded_canonicalizer": guarded,
        },
        "comparison": {
            "surface_topic_verified_value_loss_pct": round(
                100.0 * float(topic["semantic_value_loss"]), 3
            ),
            "no_merge_cost_premium_vs_reference_pct": round(
                100.0
                * (int(no_merge["review_cost"]) - int(reference["review_cost"]))
                / int(reference["review_cost"]),
                3,
            ),
            "guarded_cost_delta_vs_reference": int(guarded["review_cost"])
            - int(reference["review_cost"]),
        },
        "promotion_gate": gates,
        "candidate_rule": "MERGE_ONLY_WITH_SEMANTIC_EQUIVALENCE_EVIDENCE_OTHERWISE_FAIL_CLOSED_TO_SEPARATE_MEANINGS",
        "claim_ceiling": "DETERMINISTIC_SYNTHETIC_SIGNATURE_FIXTURE_ONLY_NO_REAL_CANONICALIZER_ACCURACY_CLAIM",
    }
