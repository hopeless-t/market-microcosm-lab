from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class PrewarmJob:
    name: str
    release: int
    deadline: int
    duration: int
    value: int


DEADLINE_TRAP = (
    PrewarmJob("A-long-salient", 1, 3, 2, 9),
    PrewarmJob("B-urgent", 1, 2, 1, 6),
    PrewarmJob("C-urgent", 2, 3, 1, 6),
    PrewarmJob("D-later", 3, 4, 1, 5),
)

DENSITY_TRAP = (
    PrewarmJob("A-dense-small", 1, 6, 1, 6),
    PrewarmJob("B-medium", 1, 6, 2, 10),
    PrewarmJob("C-large", 1, 6, 3, 12),
)


def _allowed_slots(job: PrewarmJob) -> tuple[int, ...]:
    return tuple(range(job.release, job.deadline))


def _find_schedule(jobs: tuple[PrewarmJob, ...]) -> dict[str, tuple[int, ...]] | None:
    ordered = sorted(jobs, key=lambda job: (job.deadline, job.release, job.name))

    def place(index: int, used: set[int], schedule: dict[str, tuple[int, ...]]):
        if index == len(ordered):
            return dict(schedule)
        job = ordered[index]
        for slots in combinations(_allowed_slots(job), job.duration):
            if any(slot in used for slot in slots):
                continue
            used.update(slots)
            schedule[job.name] = slots
            result = place(index + 1, used, schedule)
            if result is not None:
                return result
            for slot in slots:
                used.remove(slot)
            del schedule[job.name]
        return None

    return place(0, set(), {})


def _result(name: str, jobs: tuple[PrewarmJob, ...], selected: tuple[PrewarmJob, ...], work_units: int) -> dict:
    schedule = _find_schedule(selected)
    assert schedule is not None
    return {
        "algorithm": name,
        "selected": [job.name for job in selected],
        "total_value": sum(job.value for job in selected),
        "total_duration": sum(job.duration for job in selected),
        "schedule": {key: list(value) for key, value in sorted(schedule.items())},
        "work_units": work_units,
    }


def exact_oracle(jobs: tuple[PrewarmJob, ...]) -> dict:
    best: tuple[int, int, tuple[str, ...], tuple[PrewarmJob, ...]] | None = None
    work_units = 0
    for size in range(len(jobs) + 1):
        for subset in combinations(jobs, size):
            work_units += 1
            if _find_schedule(subset) is None:
                continue
            rank = (
                sum(job.value for job in subset),
                -sum(job.duration for job in subset),
                tuple(sorted(job.name for job in subset)),
                subset,
            )
            if best is None or rank[:3] > best[:3]:
                best = rank
    assert best is not None
    return _result("exact-oracle", jobs, best[3], work_units)


def _greedy(jobs: tuple[PrewarmJob, ...], *, mode: str) -> dict:
    if mode == "value":
        ordered = sorted(jobs, key=lambda job: (-job.value, job.deadline, job.name))
    elif mode == "density":
        ordered = sorted(
            jobs,
            key=lambda job: (-(job.value / job.duration), job.deadline, job.name),
        )
    elif mode == "arrival":
        ordered = sorted(jobs, key=lambda job: (job.release, job.name))
    else:
        raise ValueError(mode)

    selected: list[PrewarmJob] = []
    work_units = 0
    for job in ordered:
        work_units += 1
        candidate = tuple(selected + [job])
        if _find_schedule(candidate) is not None:
            selected.append(job)
    return _result(f"greedy-{mode}", jobs, tuple(selected), work_units)


def evaluate_portfolio(name: str, jobs: tuple[PrewarmJob, ...]) -> dict:
    oracle = exact_oracle(jobs)
    value = _greedy(jobs, mode="value")
    density = _greedy(jobs, mode="density")
    arrival = _greedy(jobs, mode="arrival")
    return {
        "portfolio": name,
        "jobs": [job.__dict__ for job in jobs],
        "oracle": oracle,
        "greedy_value": value,
        "greedy_density": density,
        "greedy_arrival": arrival,
        "value_matches_oracle": value["total_value"] == oracle["total_value"],
        "density_matches_oracle": density["total_value"] == oracle["total_value"],
        "arrival_matches_oracle": arrival["total_value"] == oracle["total_value"],
    }


def rpe005_report_payload() -> dict:
    deadline = evaluate_portfolio("deadline-trap", DEADLINE_TRAP)
    density = evaluate_portfolio("density-trap", DENSITY_TRAP)

    gates = {
        "deadline_trap_defeats_value_greedy": (
            deadline["greedy_value"]["total_value"] < deadline["oracle"]["total_value"]
        ),
        "deadline_trap_defeats_arrival_greedy": (
            deadline["greedy_arrival"]["total_value"] < deadline["oracle"]["total_value"]
        ),
        "density_greedy_can_succeed_on_deadline_trap": deadline["density_matches_oracle"],
        "density_trap_defeats_density_greedy": (
            density["greedy_density"]["total_value"] < density["oracle"]["total_value"]
        ),
        "value_greedy_can_succeed_on_density_trap": density["value_matches_oracle"],
        "no_single_tested_greedy_matches_both_portfolios": not (
            deadline["value_matches_oracle"] and density["value_matches_oracle"]
        ) and not (
            deadline["density_matches_oracle"] and density["density_matches_oracle"]
        ) and not (
            deadline["arrival_matches_oracle"] and density["arrival_matches_oracle"]
        ),
    }

    return {
        "experiment": "RPE-005",
        "title": "Finite prewarm capacity scheduling",
        "portfolios": {
            "deadline_trap": deadline,
            "density_trap": density,
        },
        "promotion_gate": gates,
        "candidate_rule": "SCARCE_PREWARM_CAPACITY_REQUIRES_DEADLINE_FEASIBLE_PORTFOLIO_SCHEDULING_AND_GREEDY_COUNTEREXAMPLE_TESTS",
        "claim_ceiling": "EXACT_SMALL_SYNTHETIC_SCHEDULING_WORLDS_ONLY_NO_REAL_WARMUP_THROUGHPUT_CLAIM",
    }
