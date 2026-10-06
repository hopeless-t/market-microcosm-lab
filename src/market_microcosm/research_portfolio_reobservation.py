from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations


@dataclass(frozen=True)
class RecoveryAction:
    name: str
    release: int
    deadline: int
    value: int
    mandatory: bool = False


REMAINING_ACTIONS = (
    RecoveryAction("mandatory-verification", 2, 3, 0, mandatory=True),
    RecoveryAction("reobserve-stale-A", 2, 4, 9),
    RecoveryAction("fresh-B", 2, 4, 7),
    RecoveryAction("fresh-C", 2, 5, 6),
)

INITIAL_PLAN = (
    (1, "wake-A"),
    (2, "mandatory-verification"),
    (3, "fresh-B"),
    (4, "fresh-C"),
)


def _schedule(actions: tuple[RecoveryAction, ...]) -> dict[str, int] | None:
    if not actions:
        return {}
    slots = (2, 3, 4)
    for chosen_slots in combinations(slots, len(actions)):
        for action_order in permutations(actions):
            schedule = dict(zip((action.name for action in action_order), chosen_slots))
            if all(action.release <= schedule[action.name] < action.deadline for action in action_order):
                return schedule
    return None


def _mandatory_preserved(selected: tuple[RecoveryAction, ...]) -> bool:
    mandatory_names = {action.name for action in REMAINING_ACTIONS if action.mandatory}
    return mandatory_names <= {action.name for action in selected}


def exact_safe_replan() -> dict:
    best: tuple[int, int, tuple[str, ...], tuple[RecoveryAction, ...], dict[str, int]] | None = None
    work_units = 0
    for size in range(len(REMAINING_ACTIONS) + 1):
        for subset in combinations(REMAINING_ACTIONS, size):
            work_units += 1
            if not _mandatory_preserved(subset):
                continue
            schedule = _schedule(subset)
            if schedule is None:
                continue
            names = tuple(sorted(action.name for action in subset))
            rank = (sum(action.value for action in subset), -len(subset), names)
            if best is None or rank > best[:3]:
                best = (rank[0], rank[1], rank[2], subset, schedule)
    assert best is not None
    return {
        "policy": "exact-safe-replan",
        "selected": list(best[2]),
        "schedule": best[4],
        "captured_value": best[0],
        "mandatory_preserved": True,
        "work_units": work_units,
    }


def static_commitment() -> dict:
    # Epoch 1 wake of A succeeds mechanically but freshness validation fails.
    # The original plan continues without allocating re-observation capacity.
    return {
        "policy": "static-commitment",
        "schedule": {"mandatory-verification": 2, "fresh-B": 3, "fresh-C": 4},
        "captured_value": 13,
        "stale_A_value": 0,
        "mandatory_preserved": True,
        "reobservation_performed": False,
    }


def immediate_reobserve_greedy() -> dict:
    # Greedy recovery immediately spends epoch 2 on A, then B and C. This
    # maximizes local recovered value but violates the mandatory verification deadline.
    return {
        "policy": "immediate-reobserve-greedy",
        "schedule": {"reobserve-stale-A": 2, "fresh-B": 3, "fresh-C": 4},
        "captured_value": 22,
        "mandatory_preserved": False,
        "reobservation_performed": True,
    }


def rpe007_report_payload() -> dict:
    static = static_commitment()
    greedy = immediate_reobserve_greedy()
    adaptive = exact_safe_replan()

    stale_event = {
        "epoch": 1,
        "meaning": "A",
        "wake_succeeded": True,
        "freshness_check": "STALE",
        "old_projection_authority_after_check": "REVOKED",
        "reobservation_required": True,
    }

    gates = {
        "wake_success_does_not_imply_semantic_freshness": (
            stale_event["wake_succeeded"] and stale_event["freshness_check"] == "STALE"
        ),
        "stale_detection_revokes_old_projection_authority": stale_event["old_projection_authority_after_check"] == "REVOKED",
        "static_plan_loses_stale_value": static["captured_value"] < adaptive["captured_value"],
        "greedy_recovery_can_violate_mandatory_work": not greedy["mandatory_preserved"],
        "adaptive_replan_preserves_mandatory_work": adaptive["mandatory_preserved"],
        "adaptive_replan_recovers_stale_value": "reobserve-stale-A" in adaptive["selected"],
        "adaptive_replan_beats_static_value": adaptive["captured_value"] > static["captured_value"],
        "unsafe_greedy_not_promoted_despite_higher_value": (
            greedy["captured_value"] > adaptive["captured_value"]
            and not greedy["mandatory_preserved"]
        ),
    }

    return {
        "experiment": "RPE-007",
        "title": "Stale meaning, re-observation, and bounded replanning",
        "initial_plan": list(INITIAL_PLAN),
        "stale_event": stale_event,
        "policies": {
            "static_commitment": static,
            "immediate_reobserve_greedy": greedy,
            "exact_safe_replan": adaptive,
        },
        "promotion_gate": gates,
        "candidate_rule": "WAKE_DOES_NOT_RESTORE_AUTHORITY_VALIDATE_FRESHNESS_REOBSERVE_AND_REPLAN_UNDER_MANDATORY_CONSTRAINTS",
        "claim_ceiling": "EXACT_SMALL_SYNTHETIC_REOBSERVATION_WORLD_ONLY_NO_REAL_RESEARCH_FRESHNESS_POLICY_CLAIM",
    }
