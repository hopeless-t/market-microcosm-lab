from market_microcosm.dcre010_wait_slot_allocation import (
    allocation_value,
    fifo_allocate,
    frozen_actors,
    posted_price_allocate,
    system_value_allocate,
)


def test_fifo_spends_slot_on_first_arrival() -> None:
    selected = fifo_allocate(frozen_actors())
    assert tuple(actor.actor_id for actor in selected) == ("PREMIUM",)
    assert allocation_value(selected) == 0.08


def test_posted_price_excludes_low_budget_essential_actor() -> None:
    actors = frozen_actors()
    essential = next(actor for actor in actors if actor.essential)
    assert essential.budget < 0.05
    selected = posted_price_allocate(actors, price=0.05)
    assert tuple(actor.actor_id for actor in selected) == ("PREMIUM",)
    assert all(not actor.essential for actor in selected)


def test_system_value_allocation_selects_essential_actor() -> None:
    selected = system_value_allocate(frozen_actors())
    assert tuple(actor.actor_id for actor in selected) == ("ESSENTIAL",)
    assert allocation_value(selected) == 0.50


def test_price_and_fifo_have_lower_system_value_in_frozen_world() -> None:
    actors = frozen_actors()
    fifo = allocation_value(fifo_allocate(actors))
    priced = allocation_value(posted_price_allocate(actors))
    exact = allocation_value(system_value_allocate(actors))
    assert fifo == priced == 0.08
    assert exact == 0.50
    assert exact > priced
