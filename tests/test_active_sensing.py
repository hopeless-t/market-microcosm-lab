from market_microcosm.active_sensing import (
    active_sensing_report_payload,
    cheapest_resolving_observation,
)


def test_cheap_partial_refinements_do_not_resolve_boundary_case() -> None:
    row = cheapest_resolving_observation()

    cheap = [
        candidate
        for candidate in row["candidates"]
        if candidate["cost"] == 1
    ]
    assert cheap
    assert all(
        candidate["resolves_predicate"] is False
        for candidate in cheap
    )


def test_predicate_native_query_beats_full_state_query() -> None:
    row = cheapest_resolving_observation()

    assert row["selected"]["name"] == "predicate_native_ledger_check"
    assert row["selected"]["cost"] == 2


def test_e045_promotion_contract() -> None:
    payload = active_sensing_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_active_sensing_rule"] == (
        "request-cheapest-predicate-sufficient-observation-v1"
    )
