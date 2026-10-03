from market_microcosm.core import Actor, EcosystemState, Transfer
from market_microcosm.reference import reference_step


def make_state() -> EcosystemState:
    return EcosystemState(
        t=0,
        actors=(
            Actor("platform", "platform", 60.0, burn=5.0),
            Actor("developer", "developer", 40.0, burn=4.0),
        ),
        user_utility=1.0,
        service_quality=1.0,
    )


def test_internal_transfer_conserves_cash() -> None:
    state = make_state()
    nxt = reference_step(
        state,
        (Transfer("platform", "developer", 10.0),),
    )
    assert nxt.total_cash == state.total_cash
    assert nxt.t == 1


def test_overdraw_is_rejected() -> None:
    state = make_state()
    try:
        reference_step(
            state,
            (Transfer("developer", "platform", 1000.0),),
        )
    except ValueError:
        pass
    else:
        raise AssertionError("overdraw must fail closed")
