from market_microcosm.toy_world import ToyState, ToyWorld
from market_microcosm.viability import exact_robust_viability_kernel, oracle_action


def test_exact_kernel_is_nonempty_and_excludes_dead_states() -> None:
    world = ToyWorld()
    result = exact_robust_viability_kernel(world)
    assert result.kernel
    assert ToyState(0, 4, 4) not in result.kernel
    assert all(world.viable(s) for s in result.kernel)


def test_oracle_action_keeps_every_disturbance_in_kernel() -> None:
    world = ToyWorld()
    result = exact_robust_viability_kernel(world)
    for state in result.kernel:
        action = oracle_action(world, result, state)
        assert all(world.step(state, action, w) in result.kernel for w in world.disturbances)
