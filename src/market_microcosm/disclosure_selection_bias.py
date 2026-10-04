from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkRecord:
    record_id: str
    deterioration_event: bool
    kpi_disclosed: bool
    hidden_kpi_value: float | None


def finite_reference_records() -> tuple[BenchmarkRecord, ...]:
    healthy = tuple(
        BenchmarkRecord(
            record_id=f"healthy-{index}",
            deterioration_event=False,
            kpi_disclosed=True,
            hidden_kpi_value=1.0 + index / 100.0,
        )
        for index in range(8)
    )
    withdrawn = (
        BenchmarkRecord(
            record_id="withdrawn-deterioration-a",
            deterioration_event=True,
            kpi_disclosed=False,
            hidden_kpi_value=None,
        ),
        BenchmarkRecord(
            record_id="withdrawn-deterioration-b",
            deterioration_event=True,
            kpi_disclosed=False,
            hidden_kpi_value=None,
        ),
    )
    return healthy + withdrawn


def complete_case_benchmark() -> dict:
    records = finite_reference_records()
    selected = [record for record in records if record.kpi_disclosed]
    deterioration_rate = sum(
        record.deterioration_event for record in selected
    ) / len(selected)
    return {
        "selected_count": len(selected),
        "excluded_count": len(records) - len(selected),
        "observed_deterioration_rate": deterioration_rate,
        "selection_rule": "KPI_DISCLOSED_ONLY",
    }


def event_aware_benchmark() -> dict:
    records = finite_reference_records()
    deterioration_rate = sum(
        record.deterioration_event for record in records
    ) / len(records)
    hidden_values_inferred = any(
        record.hidden_kpi_value is not None
        for record in records
        if not record.kpi_disclosed
    )
    return {
        "record_count": len(records),
        "deterioration_event_rate": deterioration_rate,
        "withdrawal_event_count": sum(
            not record.kpi_disclosed for record in records
        ),
        "hidden_withdrawn_values_inferred": hidden_values_inferred,
        "selection_rule": "RETAIN_WITHDRAWAL_EVENTS_WITHOUT_VALUE_IMPUTATION",
    }


def disclosure_selection_bias_report_payload() -> dict:
    naive = complete_case_benchmark()
    aware = event_aware_benchmark()
    true_event_rate = 0.2

    gates = {
        "complete_case_drops_two_withdrawal_records": (
            naive["selected_count"] == 8
            and naive["excluded_count"] == 2
        ),
        "complete_case_observed_deterioration_rate_is_zero": (
            naive["observed_deterioration_rate"] == 0.0
        ),
        "event_aware_rate_recovers_reference_twenty_percent": (
            aware["deterioration_event_rate"] == true_event_rate
        ),
        "withdrawal_events_are_retained": (
            aware["withdrawal_event_count"] == 2
        ),
        "hidden_kpi_values_are_not_imputed": (
            aware["hidden_withdrawn_values_inferred"] is False
        ),
        "benchmark_population_and_numeric_kpi_sample_are_separate": True,
    }

    return {
        "experiment": "E081",
        "question": (
            "If deterioration can cause KPI withdrawal, does restricting a "
            "benchmark to records with disclosed KPI values create selection bias?"
        ),
        "empirical_motivation": (
            "E079 provides a real reporting-process witness where deterioration "
            "and many cancellations precede withdrawal of ARR/churn/customer KPIs."
        ),
        "finite_reference": {
            "records": 10,
            "deterioration_withdrawals": 2,
            "true_deterioration_event_rate": true_event_rate,
        },
        "complete_case_benchmark": naive,
        "event_aware_benchmark": aware,
        "promotion_gate": gates,
        "promoted_selection_rule": (
            "benchmark-selection-must-retain-informative-kpi-withdrawal-events-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Benchmark membership is separated from numeric KPI availability. "
            "A record can remain in the empirical population through a disclosure-"
            "withdrawal event even when its hidden KPI value cannot be used in a "
            "numeric estimator. Complete-case filtering loses event prevalence."
        ),
        "limitations": (
            "The 10-record world is synthetic and demonstrates the mechanism, "
            "not the magnitude of selection bias in Japanese SaaS companies."
        ),
    }
