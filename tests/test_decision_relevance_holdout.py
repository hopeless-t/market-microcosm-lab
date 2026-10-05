from __future__ import annotations

from copy import deepcopy
import unittest

from market_microcosm.decision_relevance_holdout import (
    build_cross_loop_certificate,
    qualify_reports,
)


def reports():
    e015 = {
        "experiment": "E015",
        "promoted": True,
        "aggregate": {
            "surface_count": 18,
            "exhaustive_queries": 882,
            "adaptive_queries": 205,
            "query_savings_fraction": 0.7675736961451247,
            "classification_accuracy": 1.0,
            "frontier_exact_rate": 1.0,
            "monotonicity_violation_count": 0,
        },
        "promotion_gate": {
            "exact_cell_classification": True,
            "exact_frontier_recovery": True,
            "exact_interaction_only_counts": True,
            "query_savings_at_least_50_percent": True,
            "zero_monotonicity_violations": True,
        },
    }
    e016 = {
        "experiment": "E016",
        "guard_contract_passed": True,
        "same_generation": {"mode": "adaptive"},
        "changed_generation": {"mode": "exhaustive"},
        "adversarial_probe": {
            "monotonicity_violation_count": 23,
            "naive_classification_accuracy": 0.9795918367346939,
        },
        "post_audit_mode": "exhaustive",
        "promotion_gate": {
            "e015_was_promoted": True,
            "same_generation_allows_adaptive": True,
            "generation_change_falls_back_to_exhaustive": True,
            "adversarial_nonmonotonicity_detected_by_exhaustive_audit": True,
            "naive_adaptive_is_imperfect_on_adversarial_surface": True,
            "audit_revokes_adaptive_path": True,
        },
    }
    e017 = {
        "experiment": "E017",
        "lifecycle_contract_passed": True,
        "stable_summary": {
            "actual_queries": 5168,
            "always_exhaustive_queries": 10584,
            "query_savings_fraction": 0.5117157974300832,
        },
        "drift_summary": {
            "actual_queries": 5845,
            "always_exhaustive_queries": 10584,
            "query_savings_fraction": 0.4477513227513228,
        },
        "failed_audit_decision": {
            "state": "REVOKED",
            "required_mode": "exhaustive",
        },
        "expiry_decision": {
            "state": "EXPIRED",
            "required_mode": "exhaustive",
        },
        "promotion_gate": {
            "stable_schedule_saves_at_least_50_percent": True,
            "stable_schedule_uses_exhaustive_on_audit_epochs": True,
            "generation_drift_forces_exhaustive": True,
            "failed_audit_revokes": True,
            "skipped_audit_hard_expires": True,
            "e016_guard_contract_was_valid": True,
        },
    }
    return e015, e016, e017


class DecisionRelevanceHoldoutTests(unittest.TestCase):
    def test_reference_shape_qualifies(self):
        e015, e016, e017 = reports()
        q = qualify_reports(e015, e016, e017)
        self.assertTrue(q.exact_decision_preservation)
        self.assertTrue(q.positive_work_reduction)
        self.assertTrue(q.relevant_counterfactual_changes_decision)
        self.assertTrue(q.proof_fail_closed)
        self.assertTrue(q.certificate_lifecycle_fail_closed)
        self.assertTrue(q.qualified)

    def test_imperfect_baseline_does_not_qualify(self):
        e015, e016, e017 = reports()
        e015 = deepcopy(e015)
        e015["aggregate"]["classification_accuracy"] = 0.99
        q = qualify_reports(e015, e016, e017)
        self.assertFalse(q.exact_decision_preservation)
        self.assertFalse(q.qualified)

    def test_no_counterfactual_sensitivity_does_not_qualify(self):
        e015, e016, e017 = reports()
        e016 = deepcopy(e016)
        e016["changed_generation"]["mode"] = "adaptive"
        q = qualify_reports(e015, e016, e017)
        self.assertFalse(q.relevant_counterfactual_changes_decision)
        self.assertFalse(q.qualified)

    def test_failed_audit_must_restore_full_work(self):
        e015, e016, e017 = reports()
        e016 = deepcopy(e016)
        e016["post_audit_mode"] = "adaptive"
        q = qualify_reports(e015, e016, e017)
        self.assertFalse(q.proof_fail_closed)
        self.assertFalse(q.qualified)

    def test_expired_certificate_must_restore_full_work(self):
        e015, e016, e017 = reports()
        e017 = deepcopy(e017)
        e017["expiry_decision"]["required_mode"] = "adaptive"
        q = qualify_reports(e015, e016, e017)
        self.assertFalse(q.certificate_lifecycle_fail_closed)
        self.assertFalse(q.qualified)

    def test_certificate_is_descriptive_and_never_auto_applies(self):
        e015, e016, e017 = reports()
        cert = build_cross_loop_certificate(
            e015,
            e016,
            e017,
            source_commit="a" * 40,
            workflow_run_id=123,
        )
        self.assertTrue(cert["decision_irrelevance_proven"])
        self.assertTrue(cert["skip_preserves_admissible_decision"])
        self.assertTrue(cert["proof_fail_closed"])
        self.assertTrue(cert["relevant_counterfactual_changes_decision"])
        self.assertTrue(cert["zero_false_pruning_on_holdout"])
        self.assertEqual(cert["authority_effect"], "NONE")
        self.assertFalse(cert["auto_apply_allowed"])
        self.assertEqual(cert["e015"]["adaptive_queries"], 205)
        self.assertEqual(cert["e015"]["exhaustive_queries"], 882)


if __name__ == "__main__":
    unittest.main()
