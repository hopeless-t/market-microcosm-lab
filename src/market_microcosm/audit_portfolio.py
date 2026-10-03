from __future__ import annotations

from dataclasses import asdict, dataclass
import random


@dataclass(frozen=True)
class AuditItem:
    name: str
    audit_cost_units: int
    restoration_value: int
    mandatory: bool = False


@dataclass(frozen=True)
class ScheduleResult:
    algorithm: str
    feasible: bool
    selected_names: tuple[str, ...]
    total_cost_units: int
    total_restoration_value: int
    work_units: int
    fail_closed: bool = False


@dataclass(frozen=True)
class PortfolioBenchmark:
    portfolio_name: str
    budget_units: int
    item_count: int
    mandatory_count: int
    oracle: ScheduleResult
    dp: ScheduleResult
    greedy: ScheduleResult
    dp_matches_oracle: bool
    greedy_matches_oracle: bool


def _better(
    value: int,
    cost: int,
    names: tuple[str, ...],
    incumbent: tuple[int, int, tuple[str, ...]] | None,
) -> bool:
    if incumbent is None:
        return True
    incumbent_value, incumbent_cost, incumbent_names = incumbent
    if value != incumbent_value:
        return value > incumbent_value
    if cost != incumbent_cost:
        return cost < incumbent_cost
    return names < incumbent_names


def exhaustive_schedule(
    items: tuple[AuditItem, ...],
    *,
    budget_units: int,
) -> ScheduleResult:
    mandatory_names = {
        item.name for item in items if item.mandatory
    }
    mandatory_cost = sum(
        item.audit_cost_units for item in items if item.mandatory
    )
    if mandatory_cost > budget_units:
        return ScheduleResult(
            algorithm="exhaustive-oracle",
            feasible=False,
            selected_names=(),
            total_cost_units=0,
            total_restoration_value=0,
            work_units=1,
            fail_closed=True,
        )

    best: tuple[int, int, tuple[str, ...]] | None = None
    work = 0
    count = len(items)

    for mask in range(1 << count):
        work += 1
        selected = tuple(
            item
            for index, item in enumerate(items)
            if mask & (1 << index)
        )
        selected_names = tuple(sorted(item.name for item in selected))
        if not mandatory_names.issubset(selected_names):
            continue

        cost = sum(item.audit_cost_units for item in selected)
        if cost > budget_units:
            continue

        value = sum(item.restoration_value for item in selected)
        if _better(value, cost, selected_names, best):
            best = (value, cost, selected_names)

    if best is None:
        return ScheduleResult(
            algorithm="exhaustive-oracle",
            feasible=False,
            selected_names=(),
            total_cost_units=0,
            total_restoration_value=0,
            work_units=work,
            fail_closed=True,
        )

    value, cost, names = best
    return ScheduleResult(
        algorithm="exhaustive-oracle",
        feasible=True,
        selected_names=names,
        total_cost_units=cost,
        total_restoration_value=value,
        work_units=work,
    )


def dp_schedule(
    items: tuple[AuditItem, ...],
    *,
    budget_units: int,
) -> ScheduleResult:
    mandatory = tuple(item for item in items if item.mandatory)
    optional = tuple(item for item in items if not item.mandatory)

    mandatory_cost = sum(item.audit_cost_units for item in mandatory)
    mandatory_value = sum(item.restoration_value for item in mandatory)
    mandatory_names = tuple(sorted(item.name for item in mandatory))

    if mandatory_cost > budget_units:
        return ScheduleResult(
            algorithm="bounded-dp",
            feasible=False,
            selected_names=(),
            total_cost_units=0,
            total_restoration_value=0,
            work_units=1,
            fail_closed=True,
        )

    remaining_budget = budget_units - mandatory_cost
    states: dict[int, tuple[int, tuple[str, ...]]] = {0: (0, ())}
    work = 0

    for item in optional:
        previous = tuple(states.items())
        next_states = dict(states)

        for used_cost, (value, names) in previous:
            work += 1
            new_cost = used_cost + item.audit_cost_units
            if new_cost > remaining_budget:
                continue

            new_value = value + item.restoration_value
            new_names = tuple(sorted(names + (item.name,)))
            incumbent = next_states.get(new_cost)

            if (
                incumbent is None
                or new_value > incumbent[0]
                or (
                    new_value == incumbent[0]
                    and new_names < incumbent[1]
                )
            ):
                next_states[new_cost] = (new_value, new_names)

        states = next_states

    best: tuple[int, int, tuple[str, ...]] | None = None
    for optional_cost, (optional_value, optional_names) in states.items():
        total_cost = mandatory_cost + optional_cost
        total_value = mandatory_value + optional_value
        names = tuple(sorted(mandatory_names + optional_names))
        if _better(total_value, total_cost, names, best):
            best = (total_value, total_cost, names)

    assert best is not None
    value, cost, names = best

    return ScheduleResult(
        algorithm="bounded-dp",
        feasible=True,
        selected_names=names,
        total_cost_units=cost,
        total_restoration_value=value,
        work_units=work,
    )


def greedy_schedule(
    items: tuple[AuditItem, ...],
    *,
    budget_units: int,
) -> ScheduleResult:
    mandatory = [item for item in items if item.mandatory]
    optional = [item for item in items if not item.mandatory]

    mandatory_cost = sum(item.audit_cost_units for item in mandatory)
    if mandatory_cost > budget_units:
        return ScheduleResult(
            algorithm="greedy-value-per-cost",
            feasible=False,
            selected_names=(),
            total_cost_units=0,
            total_restoration_value=0,
            work_units=1,
            fail_closed=True,
        )

    selected = list(mandatory)
    remaining = budget_units - mandatory_cost
    work = 0

    optional.sort(
        key=lambda item: (
            -(item.restoration_value / item.audit_cost_units),
            -item.restoration_value,
            item.audit_cost_units,
            item.name,
        )
    )

    for item in optional:
        work += 1
        if item.audit_cost_units <= remaining:
            selected.append(item)
            remaining -= item.audit_cost_units

    names = tuple(sorted(item.name for item in selected))
    return ScheduleResult(
        algorithm="greedy-value-per-cost",
        feasible=True,
        selected_names=names,
        total_cost_units=sum(item.audit_cost_units for item in selected),
        total_restoration_value=sum(
            item.restoration_value for item in selected
        ),
        work_units=work,
    )


def benchmark_portfolio(
    name: str,
    items: tuple[AuditItem, ...],
    *,
    budget_units: int,
) -> PortfolioBenchmark:
    oracle = exhaustive_schedule(items, budget_units=budget_units)
    dp = dp_schedule(items, budget_units=budget_units)
    greedy = greedy_schedule(items, budget_units=budget_units)

    return PortfolioBenchmark(
        portfolio_name=name,
        budget_units=budget_units,
        item_count=len(items),
        mandatory_count=sum(item.mandatory for item in items),
        oracle=oracle,
        dp=dp,
        greedy=greedy,
        dp_matches_oracle=(
            dp.feasible == oracle.feasible
            and dp.selected_names == oracle.selected_names
            and dp.total_restoration_value == oracle.total_restoration_value
            and dp.total_cost_units == oracle.total_cost_units
        ),
        greedy_matches_oracle=(
            greedy.feasible == oracle.feasible
            and greedy.selected_names == oracle.selected_names
            and greedy.total_restoration_value
            == oracle.total_restoration_value
            and greedy.total_cost_units == oracle.total_cost_units
        ),
    )


def generated_portfolios(
    *,
    seed: int = 18017,
    portfolio_count: int = 48,
) -> tuple[tuple[str, tuple[AuditItem, ...], int], ...]:
    rng = random.Random(seed)
    portfolios = []

    for portfolio_index in range(portfolio_count):
        item_count = 8
        mandatory_indexes = set(
            rng.sample(
                range(item_count),
                rng.randint(0, 2),
            )
        )

        items = tuple(
            AuditItem(
                name=f"p{portfolio_index:02d}-cert{item_index}",
                audit_cost_units=rng.randint(1, 6),
                restoration_value=rng.randint(10, 150),
                mandatory=item_index in mandatory_indexes,
            )
            for item_index in range(item_count)
        )

        mandatory_cost = sum(
            item.audit_cost_units for item in items if item.mandatory
        )
        total_cost = sum(item.audit_cost_units for item in items)

        lower = min(total_cost, mandatory_cost + 4)
        upper = min(total_cost, mandatory_cost + 12)
        budget = rng.randint(lower, upper)

        portfolios.append(
            (
                f"generated-{portfolio_index:02d}",
                items,
                budget,
            )
        )

    return tuple(portfolios)


def greedy_trap_portfolio() -> tuple[AuditItem, ...]:
    return (
        AuditItem("A", audit_cost_units=10, restoration_value=60),
        AuditItem("B", audit_cost_units=20, restoration_value=100),
        AuditItem("C", audit_cost_units=30, restoration_value=120),
    )


def infeasible_mandatory_portfolio() -> tuple[AuditItem, ...]:
    return (
        AuditItem(
            "generation-drift",
            audit_cost_units=7,
            restoration_value=100,
            mandatory=True,
        ),
        AuditItem(
            "revoked-verifier",
            audit_cost_units=6,
            restoration_value=90,
            mandatory=True,
        ),
        AuditItem(
            "optional-old-evidence",
            audit_cost_units=2,
            restoration_value=20,
        ),
    )


def audit_portfolio_report_payload() -> dict:
    generated = tuple(
        benchmark_portfolio(name, items, budget_units=budget)
        for name, items, budget in generated_portfolios()
    )

    trap_items = greedy_trap_portfolio()
    greedy_trap = benchmark_portfolio(
        "greedy-trap",
        trap_items,
        budget_units=50,
    )

    infeasible_items = infeasible_mandatory_portfolio()
    infeasible = benchmark_portfolio(
        "mandatory-over-budget",
        infeasible_items,
        budget_units=10,
    )

    oracle_work = sum(row.oracle.work_units for row in generated)
    dp_work = sum(row.dp.work_units for row in generated)
    work_reduction = (
        1.0 - dp_work / oracle_work if oracle_work else 0.0
    )

    gates = {
        "dp_matches_exact_oracle_on_all_generated_portfolios": all(
            row.dp_matches_oracle for row in generated
        ),
        "dp_reduces_search_work_by_at_least_50_percent": (
            work_reduction >= 0.50
        ),
        "greedy_counterexample_exists": (
            not greedy_trap.greedy_matches_oracle
            and greedy_trap.oracle.total_restoration_value
            > greedy_trap.greedy.total_restoration_value
        ),
        "mandatory_over_budget_fails_closed": (
            not infeasible.oracle.feasible
            and not infeasible.dp.feasible
            and not infeasible.greedy.feasible
            and infeasible.oracle.fail_closed
            and infeasible.dp.fail_closed
            and infeasible.greedy.fail_closed
        ),
    }

    return {
        "experiment": "E018",
        "question": (
            "Can a bounded audit-portfolio scheduler match an exhaustive "
            "small-world oracle while avoiding greedy budget-allocation traps?"
        ),
        "generated_portfolio_count": len(generated),
        "generated_results": [asdict(row) for row in generated],
        "aggregate": {
            "oracle_work_units": oracle_work,
            "dp_work_units": dp_work,
            "dp_work_reduction_fraction": work_reduction,
            "dp_exact_match_rate": (
                sum(row.dp_matches_oracle for row in generated)
                / len(generated)
            ),
            "greedy_exact_match_rate": (
                sum(row.greedy_matches_oracle for row in generated)
                / len(generated)
            ),
        },
        "greedy_trap": asdict(greedy_trap),
        "infeasible_mandatory_case": asdict(infeasible),
        "promotion_gate": gates,
        "promoted_scheduler": (
            "bounded-dp" if all(gates.values()) else None
        ),
    }
