import random

from market_microcosm.ecology import MarketWorld, default_mechanisms


def test_market_step_conserves_declared_cash_flows() -> None:
    world = MarketWorld()
    state = world.initial_state()
    result = world.step(state, default_mechanisms()[0], random.Random(7))
    assert abs(result.audit.conservation_error) < 1e-6


def test_market_dynamics_are_seed_deterministic() -> None:
    world = MarketWorld()
    mechanism = default_mechanisms()[2]

    def run(seed: int):
        state = world.initial_state()
        rng = random.Random(seed)
        for _ in range(12):
            state = world.step(state, mechanism, rng).state
        return state

    assert run(11) == run(11)
    assert run(11) != run(12)


def test_mechanism_creator_pool_is_fully_allocated_when_creators_exist() -> None:
    world = MarketWorld()
    state = world.initial_state()
    result = world.step(state, default_mechanisms()[3], random.Random(3))
    assert abs(result.audit.creator_pool - result.audit.creator_paid) < 1e-6
