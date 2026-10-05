from __future__ import annotations

from collections.abc import Callable

from market_microcosm.censored_accuracy_interval import censored_accuracy_interval_report_payload
from market_microcosm.censored_evaluation_guard import censored_evaluation_report_payload
from market_microcosm.cross_company_sign_replication import cross_company_sign_replication_report_payload
from market_microcosm.disclosure_selection_bias import disclosure_selection_bias_report_payload
from market_microcosm.empirical_warning_tournament import empirical_warning_tournament_report_payload
from market_microcosm.exit_residual_value import residual_value_report_payload
from market_microcosm.exit_runoff_state_machine import exit_runoff_report_payload
from market_microcosm.governance_checkpoint_authority import governance_checkpoint_authority_report_payload
from market_microcosm.governance_checkpoint_timeline import governance_checkpoint_report_payload
from market_microcosm.governance_evidence_availability import governance_evidence_availability_report_payload
from market_microcosm.informative_kpi_withdrawal import informative_missingness_report_payload
from market_microcosm.japanese_saas_failure_taxonomy import taxonomy_report_payload
from market_microcosm.jooto_viability_counterexample import jooto_viability_report_payload
from market_microcosm.kpi_withdrawal_reason_typing import withdrawal_reason_report_payload
from market_microcosm.post_exit_horizon_guard import post_exit_horizon_report_payload
from market_microcosm.post_exit_profitability import post_exit_profitability_report_payload
from market_microcosm.replacement_kpi_bridge import replacement_kpi_bridge_report_payload
from market_microcosm.reporting_kernel_state import reporting_kernel_report_payload
from market_microcosm.transient_kpi_stress_negative_control import transient_kpi_stress_report_payload
from market_microcosm.withdrawal_exit_holdout import withdrawal_exit_holdout_report_payload
from market_microcosm.withdrawal_governance_action import withdrawal_governance_report_payload


EXPERIMENTS: tuple[tuple[str, Callable[[], dict], str], ...] = (
    ("E079", informative_missingness_report_payload, "promoted_missingness_rule"),
    ("E080", reporting_kernel_report_payload, "promoted_kernel_rule"),
    ("E081", disclosure_selection_bias_report_payload, "promoted_selection_rule"),
    ("E082", withdrawal_reason_report_payload, "promoted_typing_rule"),
    ("E083", censored_evaluation_report_payload, "promoted_evaluation_rule"),
    ("E084", censored_accuracy_interval_report_payload, "promoted_interval_rule"),
    ("E085", withdrawal_exit_holdout_report_payload, "promoted_holdout_rule"),
    ("E086", withdrawal_governance_report_payload, "promoted_governance_rule"),
    ("E087", governance_checkpoint_report_payload, "promoted_checkpoint_rule"),
    ("E088", governance_evidence_availability_report_payload, "promoted_availability_rule"),
    ("E089", governance_checkpoint_authority_report_payload, "promoted_checkpoint_authority_rule"),
    ("E090", post_exit_profitability_report_payload, "promoted_exit_rule"),
    ("E091", replacement_kpi_bridge_report_payload, "promoted_bridge_rule"),
    ("E092", post_exit_horizon_report_payload, "promoted_horizon_rule"),
    ("E093", jooto_viability_report_payload, "promoted_viability_rule"),
    ("E094", exit_runoff_report_payload, "promoted_exit_state_rule"),
    ("E095", residual_value_report_payload, "promoted_residual_value_rule"),
    ("E096", taxonomy_report_payload, "promoted_taxonomy_rule"),
    ("E097", transient_kpi_stress_report_payload, "promoted_negative_control_rule"),
    ("E098", empirical_warning_tournament_report_payload, "promoted_empirical_warning_rule"),
)


def phase_report_payload() -> dict:
    rows = []
    for experiment, factory, promotion_key in EXPERIMENTS:
        payload = factory()
        gates = payload.get("promotion_gate", {})
        rows.append(
            {
                "experiment": experiment,
                "all_promotion_gates_pass": bool(gates) and all(gates.values()),
                "promoted_rule": payload.get(promotion_key),
            }
        )

    return {
        "phase": "E079-E098",
        "experiment_count": len(rows),
        "all_experiments_promoted": all(
            row["all_promotion_gates_pass"] and row["promoted_rule"]
            for row in rows
        ),
        "experiments": rows,
        "phase_invariants": {
            "hidden_kpi_values_are_never_imputed": True,
            "reporting_policy_is_part_of_observation_model": True,
            "retrospective_evidence_does_not_leak_into_public_prospective_features": True,
            "exit_is_not_instant_zeroing": True,
            "business_exit_does_not_imply_zero_residual_capability_value": True,
            "one_quarter_kpi_stress_is_not_structural_failure_authority": True,
            "real_case_exact_fit_is_not_called_production_accuracy": True,
        },
    }
