from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SCHEMA = "market-microcosm.e024-decision-relevance-holdout/v0.1"
GENERIC_PRINCIPLE = "PRUNE_PROVEN_DECISION_IRRELEVANT_WORK"
CLAIM_CEILING = (
    "MARKET_MICROCOSM_E015_E016_E017_AS_THIRD_INDEPENDENT_"
    "PROOF_CARRYING_WORK_REDUCTION_HOLDOUT_ONLY"
)


class DecisionRelevanceHoldoutError(ValueError):
    pass


@dataclass(frozen=True)
class HoldoutQualification:
    exact_decision_preservation: bool
    positive_work_reduction: bool
    relevant_counterfactual_changes_decision: bool
    proof_fail_closed: bool
    certificate_lifecycle_fail_closed: bool
    qualified: bool

    def to_dict(self) -> dict[str, bool]:
        return {
            "exact_decision_preservation": self.exact_decision_preservation,
            "positive_work_reduction": self.positive_work_reduction,
            "relevant_counterfactual_changes_decision": (
                self.relevant_counterfactual_changes_decision
            ),
            "proof_fail_closed": self.proof_fail_closed,
            "certificate_lifecycle_fail_closed": (
                self.certificate_lifecycle_fail_closed
            ),
            "qualified": self.qualified,
        }


def qualify_reports(
    e015: dict[str, Any],
    e016: dict[str, Any],
    e017: dict[str, Any],
) -> HoldoutQualification:
    if e015.get("experiment") != "E015":
        raise DecisionRelevanceHoldoutError("e015_report_invalid")
    if e016.get("experiment") != "E016":
        raise DecisionRelevanceHoldoutError("e016_report_invalid")
    if e017.get("experiment") != "E017":
        raise DecisionRelevanceHoldoutError("e017_report_invalid")

    a15 = e015.get("aggregate")
    if not isinstance(a15, dict):
        raise DecisionRelevanceHoldoutError("e015_aggregate_missing")

    exact = (
        e015.get("promoted") is True
        and a15.get("classification_accuracy") == 1.0
        and a15.get("frontier_exact_rate") == 1.0
        and a15.get("monotonicity_violation_count") == 0
        and all(bool(v) for v in e015.get("promotion_gate", {}).values())
    )
    exhaustive = a15.get("exhaustive_queries")
    adaptive = a15.get("adaptive_queries")
    positive_reduction = (
        type(exhaustive) is int
        and type(adaptive) is int
        and exhaustive > 0
        and 0 <= adaptive < exhaustive
        and float(a15.get("query_savings_fraction", 0.0)) > 0.0
    )

    probe = e016.get("adversarial_probe")
    if not isinstance(probe, dict):
        raise DecisionRelevanceHoldoutError("e016_adversarial_probe_missing")
    relevant_counterfactual = (
        e016.get("guard_contract_passed") is True
        and e016.get("same_generation", {}).get("mode") == "adaptive"
        and e016.get("changed_generation", {}).get("mode") == "exhaustive"
        and int(probe.get("monotonicity_violation_count", 0)) > 0
        and float(probe.get("naive_classification_accuracy", 1.0)) < 1.0
    )
    proof_fail_closed = (
        e016.get("post_audit_mode") == "exhaustive"
        and all(bool(v) for v in e016.get("promotion_gate", {}).values())
    )

    failed = e017.get("failed_audit_decision")
    expiry = e017.get("expiry_decision")
    if not isinstance(failed, dict) or not isinstance(expiry, dict):
        raise DecisionRelevanceHoldoutError("e017_fail_closed_state_missing")
    lifecycle = (
        e017.get("lifecycle_contract_passed") is True
        and failed.get("state") == "REVOKED"
        and failed.get("required_mode") == "exhaustive"
        and expiry.get("state") == "EXPIRED"
        and expiry.get("required_mode") == "exhaustive"
        and all(bool(v) for v in e017.get("promotion_gate", {}).values())
    )

    qualified = (
        exact
        and positive_reduction
        and relevant_counterfactual
        and proof_fail_closed
        and lifecycle
    )
    return HoldoutQualification(
        exact_decision_preservation=exact,
        positive_work_reduction=positive_reduction,
        relevant_counterfactual_changes_decision=relevant_counterfactual,
        proof_fail_closed=proof_fail_closed,
        certificate_lifecycle_fail_closed=lifecycle,
        qualified=qualified,
    )


def build_cross_loop_certificate(
    e015: dict[str, Any],
    e016: dict[str, Any],
    e017: dict[str, Any],
    *,
    source_commit: str,
    workflow_run_id: int,
) -> dict[str, object]:
    if len(source_commit) != 40:
        raise DecisionRelevanceHoldoutError("source_commit_invalid")
    if workflow_run_id <= 0:
        raise DecisionRelevanceHoldoutError("workflow_run_id_invalid")

    q = qualify_reports(e015, e016, e017)
    a15 = e015["aggregate"]
    probe = e016["adversarial_probe"]
    stable = e017["stable_summary"]
    drift = e017["drift_summary"]

    return {
        "schema": SCHEMA,
        "generic_principle": GENERIC_PRINCIPLE,
        "certificate_id": "market-microcosm:e015-e016-e017",
        "repository": "hopeless-t/market-microcosm-lab",
        "independence_group": "repo:hopeless-t/market-microcosm-lab",
        "decision_scope": (
            "generation-scoped adaptive pair-surface evaluation with "
            "exhaustive audit fallback"
        ),
        "source_commit": source_commit,
        "workflow_run_id": workflow_run_id,
        "qualification": q.to_dict(),
        "decision_irrelevance_proven": q.qualified,
        "skip_preserves_admissible_decision": q.exact_decision_preservation,
        "proof_fail_closed": (
            q.proof_fail_closed and q.certificate_lifecycle_fail_closed
        ),
        "relevant_counterfactual_changes_decision": (
            q.relevant_counterfactual_changes_decision
        ),
        "zero_false_pruning_on_holdout": q.exact_decision_preservation,
        "e015": {
            "surface_count": a15["surface_count"],
            "exhaustive_queries": a15["exhaustive_queries"],
            "adaptive_queries": a15["adaptive_queries"],
            "query_savings_fraction": a15["query_savings_fraction"],
            "classification_accuracy": a15["classification_accuracy"],
            "frontier_exact_rate": a15["frontier_exact_rate"],
        },
        "e016": {
            "same_generation_mode": e016["same_generation"]["mode"],
            "changed_generation_mode": e016["changed_generation"]["mode"],
            "adversarial_accuracy": probe["naive_classification_accuracy"],
            "monotonicity_violation_count": probe[
                "monotonicity_violation_count"
            ],
            "post_audit_mode": e016["post_audit_mode"],
        },
        "e017": {
            "stable_actual_queries": stable["actual_queries"],
            "stable_always_exhaustive_queries": stable[
                "always_exhaustive_queries"
            ],
            "stable_query_savings_fraction": stable[
                "query_savings_fraction"
            ],
            "drift_actual_queries": drift["actual_queries"],
            "drift_always_exhaustive_queries": drift[
                "always_exhaustive_queries"
            ],
            "drift_query_savings_fraction": drift[
                "query_savings_fraction"
            ],
            "failed_audit_state": e017["failed_audit_decision"]["state"],
            "expiry_state": e017["expiry_decision"]["state"],
        },
        "evidence_handling_mode": (
            "GENERATION_SCOPED_ADAPTIVE_ONLY_WHILE_CERTIFIED_"
            "EXHAUSTIVE_ON_DRIFT_AUDIT_FAILURE_OR_EXPIRY"
        ),
        "authority_effect": "NONE",
        "auto_apply_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
    }
