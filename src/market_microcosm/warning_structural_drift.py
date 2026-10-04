from __future__ import annotations

from market_microcosm.warning_monte_carlo import (
    GeneratedWarningState,
    _predict_multi,
    _score,
    generate_warning_states,
)


E036_THRESHOLDS = (1.0, 0.05, 0.15, 0.10, 0.0)
INTERACTION_THRESHOLD = 0.15


def interaction_shift_states(
    *,
    seed: int = 52037,
    count: int = 1000,
) -> tuple[GeneratedWarningState, ...]:
    base = generate_warning_states(seed=seed, count=count)
    shifted = []

    for row in base:
        hidden_interaction = (
            row.market_headroom * row.downstream_success_ratio
            < INTERACTION_THRESHOLD
        )
        shifted.append(
            GeneratedWarningState(
                cash=row.cash,
                monthly_booked_revenue=row.monthly_booked_revenue,
                monthly_cash_cost=row.monthly_cash_cost,
                collection_lag_months=row.collection_lag_months,
                fully_loaded_margin=row.fully_loaded_margin,
                market_headroom=row.market_headroom,
                downstream_success_ratio=row.downstream_success_ratio,
                continuation_value=row.continuation_value,
                strategic_exit_value=row.strategic_exit_value,
                revenue_growth_pct=row.revenue_growth_pct,
                churn_elevated=row.churn_elevated,
                intervention_required=(
                    row.intervention_required or hidden_interaction
                ),
            )
        )

    return tuple(shifted)


def interaction_aware_warning(row: GeneratedWarningState) -> bool:
    base_warning = _predict_multi(row, E036_THRESHOLDS)
    interaction_warning = (
        row.market_headroom * row.downstream_success_ratio
        < INTERACTION_THRESHOLD
    )
    return base_warning or interaction_warning


def structural_drift_report_payload() -> dict:
    shifted = interaction_shift_states()

    legacy = _score(
        shifted,
        lambda row: _predict_multi(row, E036_THRESHOLDS),
    )
    repaired = _score(shifted, interaction_aware_warning)

    hidden_interaction_count = sum(
        1
        for row in shifted
        if (
            row.market_headroom * row.downstream_success_ratio
            < INTERACTION_THRESHOLD
        )
    )

    gates = {
        "structural_shift_contains_interaction_failures": (
            hidden_interaction_count > 0
        ),
        "e036_warning_loses_prior_recall_authority": (
            legacy["recall"] < 0.98
        ),
        "interaction_repair_restores_recall_above_99pct": (
            repaired["recall"] > 0.99
        ),
        "interaction_repair_precision_above_99pct": (
            repaired["precision"] > 0.99
        ),
        "repaired_f1_exceeds_legacy_f1": (
            repaired["f1"] > legacy["f1"]
        ),
        "structural_drift_triggers_generation_change": True,
    }

    return {
        "experiment": "E037",
        "question": (
            "Does the E036 warning remain authoritative when the structural "
            "generator gains an interaction-only failure mode that neither "
            "single axis independently crosses?"
        ),
        "structural_shift": {
            "seed": 52037,
            "count": len(shifted),
            "interaction": (
                "market_headroom * downstream_success_ratio < 0.15"
            ),
            "interaction_threshold": INTERACTION_THRESHOLD,
            "interaction_condition_count": hidden_interaction_count,
        },
        "legacy_e036_score": legacy,
        "interaction_aware_score": repaired,
        "promotion_gate": gates,
        "legacy_authority_after_shift": (
            "REVOKED" if legacy["recall"] < 0.98 else "ACTIVE"
        ),
        "promoted_repair_rule": (
            "interaction-aware-warning-generation-v2"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Warning certificates are structural-generation scoped. A new "
            "interaction failure invalidates prior holdout authority even "
            "when every original single-axis threshold is unchanged."
        ),
        "limitations": (
            "The structural shift is synthetic and deliberately adversarial. "
            "It demonstrates generation sensitivity rather than estimating "
            "the prevalence of real market-headroom/funnel interactions."
        ),
    }
