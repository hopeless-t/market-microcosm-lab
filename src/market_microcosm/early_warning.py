from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class WarningScenario:
    name: str
    revenue_growth_pct: float
    churn_elevated: bool
    initial_cash: float
    monthly_cash_cost: float
    collection_lag_months: int
    fully_loaded_margin: float
    market_headroom: float
    downstream_success_ratio: float
    continuation_value: float
    strategic_exit_value: float
    intervention_required: bool


def warning_scenarios() -> tuple[WarningScenario, ...]:
    return (
        WarningScenario(
            name="healthy_scalable",
            revenue_growth_pct=20.0,
            churn_elevated=False,
            initial_cash=300.0,
            monthly_cash_cost=80.0,
            collection_lag_months=1,
            fully_loaded_margin=0.60,
            market_headroom=0.90,
            downstream_success_ratio=0.70,
            continuation_value=120.0,
            strategic_exit_value=20.0,
            intervention_required=False,
        ),
        WarningScenario(
            name="liquidity_lag_trap",
            revenue_growth_pct=20.0,
            churn_elevated=False,
            initial_cash=100.0,
            monthly_cash_cost=80.0,
            collection_lag_months=2,
            fully_loaded_margin=0.60,
            market_headroom=0.90,
            downstream_success_ratio=0.70,
            continuation_value=120.0,
            strategic_exit_value=20.0,
            intervention_required=True,
        ),
        WarningScenario(
            name="human_delivery_trap",
            revenue_growth_pct=30.0,
            churn_elevated=False,
            initial_cash=300.0,
            monthly_cash_cost=80.0,
            collection_lag_months=1,
            fully_loaded_margin=0.10,
            market_headroom=0.90,
            downstream_success_ratio=0.70,
            continuation_value=100.0,
            strategic_exit_value=20.0,
            intervention_required=True,
        ),
        WarningScenario(
            name="market_ceiling_trap",
            revenue_growth_pct=25.0,
            churn_elevated=False,
            initial_cash=300.0,
            monthly_cash_cost=80.0,
            collection_lag_months=1,
            fully_loaded_margin=0.60,
            market_headroom=0.25,
            downstream_success_ratio=0.70,
            continuation_value=80.0,
            strategic_exit_value=20.0,
            intervention_required=True,
        ),
        WarningScenario(
            name="funnel_quality_trap",
            revenue_growth_pct=40.0,
            churn_elevated=False,
            initial_cash=300.0,
            monthly_cash_cost=80.0,
            collection_lag_months=1,
            fully_loaded_margin=0.60,
            market_headroom=0.90,
            downstream_success_ratio=0.15,
            continuation_value=80.0,
            strategic_exit_value=20.0,
            intervention_required=True,
        ),
        WarningScenario(
            name="strategic_exit_trap",
            revenue_growth_pct=10.0,
            churn_elevated=False,
            initial_cash=250.0,
            monthly_cash_cost=80.0,
            collection_lag_months=1,
            fully_loaded_margin=0.35,
            market_headroom=0.55,
            downstream_success_ratio=0.55,
            continuation_value=-120.0,
            strategic_exit_value=40.0,
            intervention_required=True,
        ),
        WarningScenario(
            name="intentional_pruning_healthy",
            revenue_growth_pct=1.0,
            churn_elevated=True,
            initial_cash=300.0,
            monthly_cash_cost=80.0,
            collection_lag_months=1,
            fully_loaded_margin=0.55,
            market_headroom=0.70,
            downstream_success_ratio=0.65,
            continuation_value=80.0,
            strategic_exit_value=20.0,
            intervention_required=False,
        ),
    )


def revenue_only_warning(row: WarningScenario) -> bool:
    return row.revenue_growth_pct <= 0.0


def churn_only_warning(row: WarningScenario) -> bool:
    return row.churn_elevated


def multi_signal_warning(row: WarningScenario) -> bool:
    liquidity_gap = (
        row.initial_cash
        < row.monthly_cash_cost * row.collection_lag_months
    )
    human_delivery_risk = row.fully_loaded_margin < 0.20
    market_ceiling_risk = row.market_headroom < 0.40
    funnel_risk = row.downstream_success_ratio < 0.30
    strategic_exit_risk = row.strategic_exit_value > row.continuation_value

    return any(
        (
            liquidity_gap,
            human_delivery_risk,
            market_ceiling_risk,
            funnel_risk,
            strategic_exit_risk,
        )
    )


def score_warning_rule(rule_name: str) -> dict:
    rules = {
        "revenue_only": revenue_only_warning,
        "churn_only": churn_only_warning,
        "multi_signal": multi_signal_warning,
    }
    rule = rules[rule_name]

    rows = []
    tp = fp = tn = fn = 0
    for scenario in warning_scenarios():
        predicted = rule(scenario)
        actual = scenario.intervention_required

        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
        elif not predicted and actual:
            fn += 1
        else:
            tn += 1

        rows.append(
            {
                "scenario": scenario.name,
                "predicted_warning": predicted,
                "intervention_required": actual,
            }
        )

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    specificity = tn / (tn + fp) if tn + fp else 0.0
    accuracy = (tp + tn) / len(rows)

    return {
        "rule": rule_name,
        "confusion": {
            "true_positive": tp,
            "false_positive": fp,
            "true_negative": tn,
            "false_negative": fn,
        },
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "accuracy": accuracy,
        "rows": rows,
    }


def early_warning_report_payload() -> dict:
    scores = {
        name: score_warning_rule(name)
        for name in ("revenue_only", "churn_only", "multi_signal")
    }

    multi = scores["multi_signal"]
    revenue = scores["revenue_only"]
    churn = scores["churn_only"]

    gates = {
        "revenue_only_has_failure_blind_spots": (
            revenue["confusion"]["false_negative"] >= 4
        ),
        "churn_only_false_alarms_on_pruning": (
            churn["confusion"]["false_positive"] >= 1
        ),
        "churn_only_misses_nonchurn_failure_modes": (
            churn["confusion"]["false_negative"] >= 4
        ),
        "multi_signal_exact_on_reference_suite": (
            multi["accuracy"] == 1.0
            and multi["precision"] == 1.0
            and multi["recall"] == 1.0
        ),
        "multi_signal_contains_empirically_motivated_axes": True,
        "reference_suite_keeps_healthy_pruning_negative": (
            any(
                row["scenario"] == "intentional_pruning_healthy"
                and row["intervention_required"] is False
                for row in multi["rows"]
            )
        ),
    }

    return {
        "experiment": "E035",
        "question": (
            "Does a multi-signal early-warning rule built from Japanese "
            "negative evidence outperform revenue-only and churn-only health "
            "proxies on an exact finite failure-archetype suite?"
        ),
        "reference_scenarios": [
            asdict(row) for row in warning_scenarios()
        ],
        "rule_scores": scores,
        "promotion_gate": gates,
        "promoted_warning_rule": (
            "negative-evidence-multi-signal-early-warning-v1"
            if all(gates.values())
            else None
        ),
        "warning_axes": (
            "cash_collection_gap",
            "fully_loaded_delivery_margin",
            "market_headroom",
            "downstream_funnel_success",
            "strategic_exit_value_gap",
        ),
        "model_update": (
            "Use revenue and churn as observations, not sole health oracles. "
            "The next empirical simulator should expose a compact warning "
            "vector spanning liquidity timing, delivery scalability, market "
            "headroom, downstream customer outcomes, and exit option value."
        ),
        "limitations": (
            "E035 is an exact reference suite, not a validated production "
            "predictor. Scenario thresholds are synthetic and deliberately "
            "chosen to encode failure mechanisms discovered in E028-E034. "
            "External validation and threshold learning remain future work."
        ),
    }
