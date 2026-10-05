from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date


@dataclass(frozen=True)
class ExitState:
    state: str
    starts_on: date
    ends_on: date | None
    accepts_new_customers: bool
    serves_existing_customers: bool
    transition_obligations_active: bool


def jooto_exit_states() -> tuple[ExitState, ...]:
    return (
        ExitState(
            state="RUNOFF_AND_MIGRATION",
            starts_on=date(2026, 8, 6),
            ends_on=date(2027, 7, 31),
            accepts_new_customers=False,
            serves_existing_customers=True,
            transition_obligations_active=True,
        ),
        ExitState(
            state="FINAL_SHUTDOWN",
            starts_on=date(2027, 8, 1),
            ends_on=None,
            accepts_new_customers=False,
            serves_existing_customers=False,
            transition_obligations_active=False,
        ),
    )


def naive_instant_exit_model() -> dict:
    return {
        "effective_on": "2026-08-06",
        "revenue_after_decision": 0,
        "operating_cost_after_decision": 0,
        "existing_customer_obligation": False,
        "transition_cost_possible": False,
        "status": "CONTRADICTED_BY_PUBLIC_EXIT_PLAN",
    }


def exit_runoff_report_payload() -> dict:
    states = jooto_exit_states()
    runoff = states[0]
    runoff_days = (runoff.ends_on - runoff.starts_on).days + 1
    naive = naive_instant_exit_model()

    gates = {
        "runoff_begins_on_board_decision_date": (
            runoff.starts_on == date(2026, 8, 6)
        ),
        "existing_customers_continue_during_runoff": (
            runoff.serves_existing_customers is True
        ),
        "new_customer_intake_stops_during_runoff": (
            runoff.accepts_new_customers is False
        ),
        "transition_obligations_remain_active": (
            runoff.transition_obligations_active is True
        ),
        "runoff_inclusive_duration_is_360_days": runoff_days == 360,
        "naive_instant_zero_model_is_rejected": (
            naive["status"] == "CONTRADICTED_BY_PUBLIC_EXIT_PLAN"
        ),
        "final_shutdown_is_separate_state": (
            states[1].state == "FINAL_SHUTDOWN"
            and states[1].starts_on == date(2027, 8, 1)
        ),
    }

    return {
        "experiment": "E094",
        "question": (
            "Should a SaaS business-exit decision instantly zero revenue, cost, "
            "and customer obligations, or does public exit evidence require a "
            "runoff/migration state?"
        ),
        "source": {
            "provider": "PR TIMES, Inc.",
            "service": "Jooto",
            "decision_date": "2026-08-06",
            "general_service_end_date": "2027-07-31",
            "annotation": (
                "New registrations/contracts/upgrades stop on the decision date, "
                "while existing customers can continue through 2027-07-31. The "
                "company commits to service/security maintenance, data migration, "
                "fee settlement and other transition work, with possible one-time costs."
            ),
        },
        "states": [
            {
                **asdict(state),
                "starts_on": state.starts_on.isoformat(),
                "ends_on": state.ends_on.isoformat() if state.ends_on else None,
            }
            for state in states
        ],
        "runoff_inclusive_days": runoff_days,
        "naive_instant_exit_model": naive,
        "promotion_gate": gates,
        "promoted_exit_state_rule": (
            "strategic-exit-is-runoff-state-machine-not-instant-zeroing-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Exit becomes a lifecycle state machine. A board decision can stop "
            "new intake immediately while revenue/cost/customer obligations continue "
            "through an explicit runoff and migration period before final shutdown."
        ),
        "limitations": (
            "E094 models public contractual/operational timing, not the exact future "
            "monthly revenue or transition cost trajectory during runoff."
        ),
    }
