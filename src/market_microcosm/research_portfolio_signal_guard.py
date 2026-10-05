from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.research_portfolio_residency import MEANINGS, STATIC_TIERS, TIER


@dataclass(frozen=True)
class SignalScenario:
    name: str
    signals: tuple[tuple[int, float], ...]
    degraded_epochs: tuple[int, ...] = ()


SCENARIOS = (
    SignalScenario("healthy", ((1, 0.95), (10, 0.95))),
    SignalScenario("missing-first", ((10, 0.95),), degraded_epochs=(1, 2)),
    SignalScenario("delayed-first", ((2, 0.95), (10, 0.95)), degraded_epochs=(1, 2)),
    SignalScenario("false-positive", ((1, 0.95), (5, 0.30), (7, 0.40), (10, 0.95))),
    SignalScenario("combined", ((5, 0.30), (7, 0.40), (10, 0.95)), degraded_epochs=(1, 2)),
)


RARE_NAME = "dormant-social-capital"
CONFIDENCE_THRESHOLD = 0.80


def _rare_tier(policy: str, epoch: int, scenario: SignalScenario) -> str:
    confidence_by_epoch = dict(scenario.signals)
    previous_confidence = confidence_by_epoch.get(epoch - 1, 0.0)

    if policy == "naive_any_signal":
        return "WARM" if (epoch - 1) in confidence_by_epoch else "DORMANT"
    if policy == "confidence_filtered":
        return "WARM" if previous_confidence >= CONFIDENCE_THRESHOLD else "DORMANT"
    if policy == "always_warm_rare":
        return "WARM"
    if policy == "certified_hybrid":
        if epoch in scenario.degraded_epochs:
            return "WARM"
        return "WARM" if previous_confidence >= CONFIDENCE_THRESHOLD else "DORMANT"
    raise ValueError(policy)


def evaluate_signal_policy(policy: str, scenario: SignalScenario, horizon: int = 12) -> dict:
    holding_cost = 0.0
    wake_cost = 0.0
    captured_value = 0
    total_value = sum(
        len(profile.demand_epochs) * profile.value_per_demand for profile in MEANINGS
    )
    missed_events = 0
    rare_rows: list[dict] = []

    for epoch in range(1, horizon + 1):
        for profile in MEANINGS:
            if profile.name == RARE_NAME:
                tier = _rare_tier(policy, epoch, scenario)
            else:
                tier = STATIC_TIERS[profile.name]

            holding_cost += float(TIER[tier]["holding_cost"])

            if epoch not in profile.demand_epochs:
                continue

            wake_latency = int(TIER[tier]["wake_latency"])
            wake_cost += float(TIER[tier]["wake_cost"])
            served = wake_latency <= profile.deadline
            if served:
                captured_value += profile.value_per_demand
            else:
                missed_events += 1

            if profile.name == RARE_NAME:
                rare_rows.append(
                    {
                        "epoch": epoch,
                        "tier": tier,
                        "served": served,
                        "signal_previous_epoch": (epoch - 1) in dict(scenario.signals),
                        "previous_signal_confidence": dict(scenario.signals).get(epoch - 1),
                        "channel_degraded": epoch in scenario.degraded_epochs,
                    }
                )

    total_cost = holding_cost + wake_cost
    return {
        "policy": policy,
        "scenario": scenario.name,
        "holding_cost": holding_cost,
        "wake_cost": wake_cost,
        "total_resource_cost": total_cost,
        "captured_value": captured_value,
        "total_possible_value": total_value,
        "value_coverage": captured_value / total_value,
        "missed_events": missed_events,
        "rare_probe": rare_rows,
    }


def _aggregate(policy: str) -> dict:
    rows = [evaluate_signal_policy(policy, scenario) for scenario in SCENARIOS]
    captured = sum(int(row["captured_value"]) for row in rows)
    possible = sum(int(row["total_possible_value"]) for row in rows)
    cost = sum(float(row["total_resource_cost"]) for row in rows)
    return {
        "policy": policy,
        "scenario_count": len(rows),
        "aggregate_resource_cost": cost,
        "aggregate_captured_value": captured,
        "aggregate_possible_value": possible,
        "aggregate_value_coverage": captured / possible,
        "scenario_results": rows,
    }


def rpe004_report_payload() -> dict:
    naive = _aggregate("naive_any_signal")
    filtered = _aggregate("confidence_filtered")
    always_warm = _aggregate("always_warm_rare")
    hybrid = _aggregate("certified_hybrid")

    by_name = {
        policy["policy"]: {row["scenario"]: row for row in policy["scenario_results"]}
        for policy in (naive, filtered, always_warm, hybrid)
    }

    gates = {
        "missing_signal_breaks_naive_value": by_name["naive_any_signal"]["missing-first"]["value_coverage"] < 1.0,
        "delayed_signal_breaks_naive_value": by_name["naive_any_signal"]["delayed-first"]["value_coverage"] < 1.0,
        "confidence_filter_removes_false_positive_cost": (
            by_name["confidence_filtered"]["false-positive"]["total_resource_cost"]
            < by_name["naive_any_signal"]["false-positive"]["total_resource_cost"]
        ),
        "confidence_filter_alone_cannot_recover_missing_signal": by_name["confidence_filtered"]["missing-first"]["value_coverage"] < 1.0,
        "always_warm_is_safe_but_expensive": (
            always_warm["aggregate_value_coverage"] == 1.0
            and always_warm["aggregate_resource_cost"] > hybrid["aggregate_resource_cost"]
        ),
        "certified_hybrid_preserves_all_value": hybrid["aggregate_value_coverage"] == 1.0,
        "certified_hybrid_beats_naive_cost_and_value": (
            hybrid["aggregate_resource_cost"] < naive["aggregate_resource_cost"]
            and hybrid["aggregate_captured_value"] > naive["aggregate_captured_value"]
        ),
        "degraded_channel_triggers_conservative_residency": all(
            any(row["channel_degraded"] and row["tier"] == "WARM" for row in result["rare_probe"])
            for scenario_name, result in by_name["certified_hybrid"].items()
            if scenario_name in {"missing-first", "delayed-first", "combined"}
        ),
    }

    return {
        "experiment": "RPE-004",
        "title": "Wake-signal reliability adversary",
        "fixture": {
            "scenario_count": len(SCENARIOS),
            "confidence_threshold": CONFIDENCE_THRESHOLD,
            "scenarios": [
                {
                    "name": scenario.name,
                    "signals": list(scenario.signals),
                    "degraded_epochs": list(scenario.degraded_epochs),
                }
                for scenario in SCENARIOS
            ],
        },
        "policies": {
            "naive_any_signal": naive,
            "confidence_filtered": filtered,
            "always_warm_rare": always_warm,
            "certified_hybrid": hybrid,
        },
        "comparison": {
            "naive_value_loss_pct": round(100.0 * (1.0 - naive["aggregate_value_coverage"]), 3),
            "hybrid_cost_reduction_vs_always_warm_pct": round(
                100.0
                * (always_warm["aggregate_resource_cost"] - hybrid["aggregate_resource_cost"])
                / always_warm["aggregate_resource_cost"],
                3,
            ),
            "hybrid_cost_reduction_vs_naive_pct": round(
                100.0
                * (naive["aggregate_resource_cost"] - hybrid["aggregate_resource_cost"])
                / naive["aggregate_resource_cost"],
                3,
            ),
        },
        "promotion_gate": gates,
        "candidate_rule": "SIGNAL_DRIVEN_PREWARM_REQUIRES_CHANNEL_HEALTH_CERTIFICATION_AND_FAIL_CLOSED_RESIDENCY_FALLBACK",
        "claim_ceiling": "DETERMINISTIC_SYNTHETIC_SIGNAL_HEALTH_FIXTURE_ONLY_NO_REAL_ALERT_RELIABILITY_CLAIM",
    }
