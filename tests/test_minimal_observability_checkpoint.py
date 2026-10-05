from market_microcosm.minimal_observability_checkpoint import (
    boundary_checkpoint_reference,
    minimal_observability_checkpoint_report_payload,
)


def test_two_arr_values_do_not_resolve_newest_mrr() -> None:
    row = boundary_checkpoint_reference()

    assert row["previous_arr"] == 60.0
    assert row["current_arr"] == 44.0
    assert row["unresolved_pairs_without_boundary"] == [
        [8, 0],
        [9, 1],
        [10, 2],
    ]


def test_one_outgoing_boundary_value_restores_newest_mrr() -> None:
    row = boundary_checkpoint_reference()

    assert row["true_outgoing_oldest_mrr"] == 10
    assert row["true_newest_mrr"] == 2
    assert row["reconstructed_newest_mrr_with_boundary"] == 2


def test_e041_promotion_contract() -> None:
    payload = minimal_observability_checkpoint_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_checkpoint_rule"] == (
        "rolling-window-boundary-checkpoint-restores-observability-v1"
    )
