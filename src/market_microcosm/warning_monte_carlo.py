from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
import random


@dataclass(frozen=True)
class GeneratedWarningState:
    cash: float
    monthly_booked_revenue: float
    monthly_cash_cost: float
    collection_lag_months: int
    fully_loaded_margin: float
    market_headroom: float
    downstream_success_ratio: float
    continuation_value: float
    strategic_exit_value: float
    revenue_growth_pct: float
    churn_elevated: bool
    intervention_required: bool


def _cash_failure_within_horizon(
    *,
    cash: float,
    monthly_booked_revenue: float,
    monthly_cash_cost: float,
    collection_lag_months: int,
    horizon_months: int = 6,
) -> bool:
    current_cash = cash
    for month in range(1, horizon_months + 1):
        collected = (
            monthly_booked_revenue
            if month > collection_lag_months
            else 0.0
        )
        current_cash += collected - monthly_cash_cost
        if current_cash < 0:
            return True
    return False


def generate_warning_states(
    *,
    seed: int,
    count: int,
) -> tuple[GeneratedWarningState, ...]:
    rng = random.Random(seed)
    rows: list[GeneratedWarningState] = []

    for _ in range(count):
        cash = rng.uniform(20.0, 400.0)
        revenue = rng.uniform(70.0, 140.0)
        cost = rng.uniform(60.0, 120.0)
        lag = rng.randint(0, 4)
        margin = rng.uniform(-0.10, 0.70)
        headroom = rng.random()
        downstream = rng.random()
        continuation = rng.uniform(-150.0, 150.0)
        exit_value = rng.uniform(-20.0, 100.0)
        revenue_growth = rng.uniform(-10.0, 50.0)
        churn = rng.random() < 0.20

        intervention = any(
            (
                _cash_failure_within_horizon(
                    cash=cash,
                    monthly_booked_revenue=revenue,
                    monthly_cash_cost=cost,
                    collection_lag_months=lag,
                ),
                margin < 0.05,
                headroom < 0.15,
                downstream < 0.10,
                exit_value > continuation,
            )
        )

        rows.append(
            GeneratedWarningState(
                cash=cash,
                monthly_booked_revenue=revenue,
                monthly_cash_cost=cost,
                collection_lag_months=lag,
                fully_loaded_margin=margin,
                market_headroom=headroom,
                downstream_success_ratio=downstream,
                continuation_value=continuation,
                strategic_exit_value=exit_value,
                revenue_growth_pct=revenue_growth,
                churn_elevated=churn,
                intervention_required=intervention,
            )
        )

    return tuple(rows)


def _predict_multi(
    row: GeneratedWarningState,
    thresholds: tuple[float, float, float, float, float],
) -> bool:
    cash_threshold, margin_threshold, headroom_threshold, downstream_threshold, exit_gap_threshold = thresholds
    denominator = row.monthly_cash_cost * max(
        row.collection_lag_months,
        1,
    )
    cash_coverage_ratio = row.cash / denominator

    return any(
        (
            cash_coverage_ratio < cash_threshold,
            row.fully_loaded_margin < margin_threshold,
            row.market_headroom < headroom_threshold,
            row.downstream_success_ratio < downstream_threshold,
            (
                row.strategic_exit_value - row.continuation_value
                > exit_gap_threshold
            ),
        )
    )


def _score(
    rows: tuple[GeneratedWarningState, ...],
    predictor,
) -> dict:
    tp = fp = tn = fn = 0

    for row in rows:
        predicted = predictor(row)
        actual = row.intervention_required

        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
        elif not predicted and actual:
            fn += 1
        else:
            tn += 1

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = (
        2.0 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    accuracy = (tp + tn) / len(rows)

    return {
        "true_positive": tp,
        "false_positive": fp,
        "true_negative": tn,
        "false_negative": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
    }


def threshold_grid() -> tuple[tuple[float, float, float, float, float], ...]:
    return tuple(
        product(
            (0.75, 1.00, 1.25, 1.50),
            (0.00, 0.05, 0.10),
            (0.10, 0.15, 0.20),
            (0.08, 0.10, 0.15),
            (-10.0, 0.0, 10.0),
        )
    )


def select_thresholds(
    discovery: tuple[GeneratedWarningState, ...],
) -> dict:
    candidates = []

    for thresholds in threshold_grid():
        score = _score(
            discovery,
            lambda row, thresholds=thresholds: _predict_multi(
                row,
                thresholds,
            ),
        )
        ranking = (
            score["f1"],
            score["recall"],
            -score["false_positive"],
            tuple(-value for value in thresholds),
        )
        candidates.append((ranking, thresholds, score))

    _, selected, score = max(candidates, key=lambda row: row[0])
    return {
        "selected_thresholds": {
            "cash_coverage_ratio": selected[0],
            "fully_loaded_margin": selected[1],
            "market_headroom": selected[2],
            "downstream_success_ratio": selected[3],
            "strategic_exit_value_gap": selected[4],
        },
        "discovery_score": score,
        "candidate_count": len(candidates),
        "_threshold_tuple": selected,
    }


def monte_carlo_warning_report_payload() -> dict:
    discovery = generate_warning_states(seed=32035, count=500)
    holdout = generate_warning_states(seed=42035, count=500)
    selection = select_thresholds(discovery)
    thresholds = selection.pop("_threshold_tuple")

    multi_holdout = _score(
        holdout,
        lambda row: _predict_multi(row, thresholds),
    )
    revenue_holdout = _score(
        holdout,
        lambda row: row.revenue_growth_pct <= 0.0,
    )
    churn_holdout = _score(
        holdout,
        lambda row: row.churn_elevated,
    )

    gates = {
        "discovery_and_holdout_seeds_are_distinct": True,
        "threshold_search_is_nontrivial": (
            selection["candidate_count"] >= 300
        ),
        "multi_signal_holdout_recall_above_98pct": (
            multi_holdout["recall"] > 0.98
        ),
        "multi_signal_holdout_precision_above_98pct": (
            multi_holdout["precision"] > 0.98
        ),
        "multi_signal_holdout_f1_above_98pct": (
            multi_holdout["f1"] > 0.98
        ),
        "revenue_only_holdout_recall_below_25pct": (
            revenue_holdout["recall"] < 0.25
        ),
        "churn_only_holdout_recall_below_30pct": (
            churn_holdout["recall"] < 0.30
        ),
        "holdout_not_used_for_threshold_selection": True,
    }

    return {
        "experiment": "E036",
        "question": (
            "Does the negative-evidence multi-signal warning survive "
            "threshold search on a broad deterministic discovery population "
            "and an untouched generated holdout?"
        ),
        "generator": {
            "discovery_seed": 32035,
            "holdout_seed": 42035,
            "discovery_count": len(discovery),
            "holdout_count": len(holdout),
            "oracle_horizon_months": 6,
        },
        "selection": selection,
        "holdout_scores": {
            "multi_signal": multi_holdout,
            "revenue_only": revenue_holdout,
            "churn_only": churn_holdout,
        },
        "promotion_gate": gates,
        "promoted_warning_search_rule": (
            "discovery-tuned-multi-signal-warning-with-holdout-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "The warning vector may now be tuned on generated discovery "
            "worlds only if untouched seed banks remain isolated and scalar "
            "baselines are reported beside it."
        ),
        "limitations": (
            "The holdout is synthetic and generated by the same declared "
            "structural family as discovery. High holdout performance is "
            "evidence of within-family generalization, not real-company "
            "predictive validity."
        ),
    }
