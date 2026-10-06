from __future__ import annotations

from itertools import combinations


CHANNEL_VALUE = {
    "governance": 10,
    "economics": 7,
    "workflow": 8,
    "presentation": 1,
    "provenance": 4,
}

DECLARED_DOMAIN = {
    "governance": "declared-governance",
    "economics": "declared-economics",
    "workflow": "declared-workflow",
    "presentation": "declared-presentation",
    "provenance": "declared-provenance",
}

HIDDEN_DOMAIN = {
    "governance": "shared-metadata-registry",
    "economics": "shared-metadata-registry",
    "workflow": "workflow-source",
    "presentation": "presentation-source",
    "provenance": "provenance-source",
}

SHOCK_PROBABILITY = 0.01


def minimum_domains_to_forge(selected_channels: tuple[str, ...], domain_map: dict[str, str]) -> int:
    domains = sorted({domain_map[channel] for channel in selected_channels})
    for size in range(len(domains) + 1):
        for shocked in combinations(domains, size):
            compromised = {
                channel
                for channel in selected_channels
                if domain_map[channel] in shocked
            }
            if len(compromised) == len(selected_channels):
                return size
    raise AssertionError("unreachable")


def exact_forge_probability(selected_channels: tuple[str, ...], domain_map: dict[str, str]) -> float:
    domains = sorted(set(domain_map.values()))
    probability = 0.0
    for size in range(len(domains) + 1):
        for shocked in combinations(domains, size):
            shocked_set = set(shocked)
            compromised = {
                channel
                for channel in selected_channels
                if domain_map[channel] in shocked_set
            }
            if len(compromised) != len(selected_channels):
                continue
            probability += (
                SHOCK_PROBABILITY**size
                * (1.0 - SHOCK_PROBABILITY) ** (len(domains) - size)
            )
    return probability


def _probe_result(name: str, selected: tuple[str, ...], domain_map: dict[str, str]) -> dict:
    return {
        "policy": name,
        "selected_channels": list(selected),
        "declared_distinct_channel_count": len(set(selected)),
        "effective_failure_domain_count": len({domain_map[channel] for channel in selected}),
        "minimum_domain_shocks_to_forge_healthy": minimum_domains_to_forge(selected, domain_map),
        "exact_forge_probability": exact_forge_probability(selected, domain_map),
        "covered_decision_value": sum(CHANNEL_VALUE[channel] for channel in selected),
    }


def rpe010_report_payload() -> dict:
    value_first_pair = ("governance", "economics")
    dependency_aware_pair = ("governance", "workflow")

    nominal = _probe_result("value-first-nominal", value_first_pair, DECLARED_DOMAIN)
    hidden = _probe_result("value-first-hidden-common-mode", value_first_pair, HIDDEN_DOMAIN)
    dependency_aware = _probe_result(
        "dependency-aware-hidden-topology", dependency_aware_pair, HIDDEN_DOMAIN
    )

    hidden_value_at_risk = CHANNEL_VALUE["governance"] + CHANNEL_VALUE["economics"]

    gates = {
        "nominal_labels_appear_independent": nominal["effective_failure_domain_count"] == 2,
        "hidden_topology_collapses_two_labels_to_one_domain": hidden["effective_failure_domain_count"] == 1,
        "hidden_common_mode_reduces_forge_boundary": (
            hidden["minimum_domain_shocks_to_forge_healthy"]
            < nominal["minimum_domain_shocks_to_forge_healthy"]
        ),
        "hidden_common_mode_inflates_forge_probability": hidden["exact_forge_probability"] > nominal["exact_forge_probability"],
        "dependency_aware_pair_restores_two_domain_boundary": dependency_aware["minimum_domain_shocks_to_forge_healthy"] == 2,
        "dependency_aware_pair_reduces_hidden_forge_probability": dependency_aware["exact_forge_probability"] < hidden["exact_forge_probability"],
        "common_mode_can_cover_material_decision_value": hidden_value_at_risk >= 17,
    }

    return {
        "experiment": "RPE-010",
        "title": "Hidden common mode in semantic observation health",
        "fixture": {
            "shock_probability_per_independent_domain": SHOCK_PROBABILITY,
            "declared_domain_map": DECLARED_DOMAIN,
            "hidden_domain_map": HIDDEN_DOMAIN,
            "hidden_common_mode_value_at_risk": hidden_value_at_risk,
        },
        "policies": {
            "nominal_value_first": nominal,
            "hidden_common_mode_value_first": hidden,
            "hidden_topology_dependency_aware": dependency_aware,
        },
        "comparison": {
            "forge_probability_inflation_factor": hidden["exact_forge_probability"] / nominal["exact_forge_probability"],
            "dependency_aware_probability_reduction_fraction": 1.0 - (
                dependency_aware["exact_forge_probability"] / hidden["exact_forge_probability"]
            ),
        },
        "promotion_gate": gates,
        "candidate_rule": "CERTIFY_SPARSE_SEMANTIC_OBSERVATION_BY_EVIDENCED_FAILURE_DOMAINS_NOT_CHANNEL_LABELS",
        "claim_ceiling": "EXACT_SYNTHETIC_INDEPENDENT_DOMAIN_MODEL_ONLY_NO_REAL_PROVIDER_OR_SOURCE_INDEPENDENCE_CLAIM",
    }
