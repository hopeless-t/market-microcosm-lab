from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MeaningProfile:
    name: str
    demand_epochs: tuple[int, ...]
    value_per_demand: int
    deadline: int
    signal_epochs: tuple[int, ...] = ()


MEANINGS = (
    MeaningProfile("canonical-kernel", tuple(range(1, 13)), 10, 0),
    MeaningProfile("finite-ram", (2, 4, 6, 8, 10, 12), 8, 1),
    MeaningProfile("pcg-streaming", (3, 6, 9, 12), 6, 2),
    MeaningProfile("labor-transition", (4, 8, 12), 7, 2),
    MeaningProfile("dormant-social-capital", (2, 11), 12, 1, signal_epochs=(1, 10)),
    MeaningProfile("archive-only", (), 0, 4),
)


TIER = {
    "HOT": {"holding_cost": 4.0, "wake_latency": 0, "wake_cost": 0.0},
    "WARM": {"holding_cost": 2.0, "wake_latency": 1, "wake_cost": 1.0},
    "COLD": {"holding_cost": 0.5, "wake_latency": 2, "wake_cost": 3.0},
    "DORMANT": {"holding_cost": 0.0, "wake_latency": 4, "wake_cost": 6.0},
}


STATIC_TIERS = {
    "canonical-kernel": "HOT",
    "finite-ram": "WARM",
    "pcg-streaming": "COLD",
    "labor-transition": "COLD",
    "dormant-social-capital": "DORMANT",
    "archive-only": "DORMANT",
}


def _recency_tier(epoch: int, last_demand: int | None) -> str:
    if last_demand is None:
        return "DORMANT"
    age = epoch - last_demand
    if age <= 1:
        return "HOT"
    if age <= 3:
        return "WARM"
    if age <= 6:
        return "COLD"
    return "DORMANT"


def _tier_for(
    policy: str,
    profile: MeaningProfile,
    epoch: int,
    last_demand: int | None,
) -> str:
    if policy == "always_hot":
        return "HOT"
    if policy == "all_dormant":
        return "DORMANT"
    if policy == "static_tiering":
        return STATIC_TIERS[profile.name]
    if policy == "recency_only":
        return _recency_tier(epoch, last_demand)
    if policy == "signal_aware_prewarm":
        base = STATIC_TIERS[profile.name]
        if (epoch - 1) in profile.signal_epochs:
            return "WARM"
        return base
    raise ValueError(policy)


def evaluate_policy(policy: str, horizon: int = 12) -> dict:
    last_demand: dict[str, int | None] = {profile.name: None for profile in MEANINGS}
    holding_cost = 0.0
    wake_cost = 0.0
    captured_value = 0
    total_value = sum(
        len(profile.demand_epochs) * profile.value_per_demand for profile in MEANINGS
    )
    missed_events = 0
    event_rows: list[dict] = []
    residency_counts = {tier: 0 for tier in TIER}

    for epoch in range(1, horizon + 1):
        for profile in MEANINGS:
            tier = _tier_for(policy, profile, epoch, last_demand[profile.name])
            residency_counts[tier] += 1
            holding_cost += float(TIER[tier]["holding_cost"])

            if epoch not in profile.demand_epochs:
                continue

            wake_latency = int(TIER[tier]["wake_latency"])
            wake_cost += float(TIER[tier]["wake_cost"])
            served = wake_latency <= profile.deadline
            value = profile.value_per_demand if served else 0
            captured_value += value
            if not served:
                missed_events += 1

            event_rows.append(
                {
                    "epoch": epoch,
                    "meaning": profile.name,
                    "tier": tier,
                    "deadline": profile.deadline,
                    "wake_latency": wake_latency,
                    "served": served,
                    "value": value,
                    "possible_value": profile.value_per_demand,
                    "signal_previous_epoch": (epoch - 1) in profile.signal_epochs,
                }
            )
            last_demand[profile.name] = epoch

    total_cost = holding_cost + wake_cost
    return {
        "policy": policy,
        "holding_cost": holding_cost,
        "wake_cost": wake_cost,
        "total_resource_cost": total_cost,
        "captured_value": captured_value,
        "total_possible_value": total_value,
        "value_coverage": captured_value / total_value,
        "missed_events": missed_events,
        "value_per_resource_cost": captured_value / total_cost if total_cost else 0.0,
        "residency_counts": residency_counts,
        "events": event_rows,
    }


def rpe003_report_payload() -> dict:
    always_hot = evaluate_policy("always_hot")
    all_dormant = evaluate_policy("all_dormant")
    static = evaluate_policy("static_tiering")
    recency = evaluate_policy("recency_only")
    signal = evaluate_policy("signal_aware_prewarm")

    gates = {
        "always_hot_preserves_all_value": always_hot["value_coverage"] == 1.0,
        "always_hot_has_highest_holding_cost": always_hot["holding_cost"] > signal["holding_cost"],
        "all_dormant_misses_urgent_value": all_dormant["value_coverage"] < 1.0,
        "static_tiering_misses_rare_urgent_item": static["value_coverage"] < 1.0,
        "recency_only_has_cold_start_loss": recency["value_coverage"] < 1.0,
        "signal_aware_recovers_all_value": signal["value_coverage"] == 1.0,
        "signal_aware_cost_below_always_hot": signal["total_resource_cost"] < always_hot["total_resource_cost"],
        "signal_aware_beats_static_cost_and_value": (
            signal["total_resource_cost"] < static["total_resource_cost"]
            and signal["captured_value"] > static["captured_value"]
        ),
    }

    rare_static = [
        row
        for row in static["events"]
        if row["meaning"] == "dormant-social-capital"
    ]
    rare_signal = [
        row
        for row in signal["events"]
        if row["meaning"] == "dormant-social-capital"
    ]

    return {
        "experiment": "RPE-003",
        "title": "Curiosity residency and wake-up economics",
        "fixture": {
            "horizon": 12,
            "meaning_count": len(MEANINGS),
            "total_possible_value": always_hot["total_possible_value"],
            "tier_contract": TIER,
        },
        "policies": {
            "always_hot": always_hot,
            "all_dormant": all_dormant,
            "static_tiering": static,
            "recency_only": recency,
            "signal_aware_prewarm": signal,
        },
        "rare_urgent_probe": {
            "static": rare_static,
            "signal_aware": rare_signal,
        },
        "comparison": {
            "signal_cost_reduction_vs_always_hot_pct": round(
                100.0
                * (always_hot["total_resource_cost"] - signal["total_resource_cost"])
                / always_hot["total_resource_cost"],
                3,
            ),
            "static_value_loss_pct": round(100.0 * (1.0 - static["value_coverage"]), 3),
            "recency_value_loss_pct": round(100.0 * (1.0 - recency["value_coverage"]), 3),
        },
        "promotion_gate": gates,
        "candidate_rule": "PRESERVE_DORMANT_OPTION_VALUE_AND_PREWARM_ONLY_ON_DECISION_HAZARD_SIGNALS",
        "claim_ceiling": "DETERMINISTIC_SYNTHETIC_WAKE_SIGNAL_FIXTURE_ONLY_NO_REAL_ATTENTION_SCHEDULER_CLAIM",
    }
