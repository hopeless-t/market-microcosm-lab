from market_microcosm.checkpoint_rotation import (
    build_rotation,
    checkpoint_rotation_report_payload,
    delete_checkpoint,
    detect_checkpoint_forks,
    extend_reference_ledger,
    fork_children,
    forge_latest_checkpoint,
    reorder_checkpoints,
    verify_latest_only,
    verify_rotation,
)
from market_microcosm.provenance_ledger import rewrite_and_rehash


def _reference():
    ledger = extend_reference_ledger(
        generation_a="g1",
        generation_b="g2",
    )
    checkpoints = build_rotation(
        ledger,
        ledger_id="ledger",
        event_counts=(2, 4, 6, 8),
    )
    return ledger, checkpoints


def test_reference_rotation_and_pinned_checkpoint() -> None:
    ledger, checkpoints = _reference()
    pinned = checkpoints[1]
    assert verify_rotation(ledger, checkpoints)[0] is True
    assert verify_rotation(
        ledger,
        checkpoints,
        pinned_checkpoint_hash=pinned.checkpoint_hash,
        pinned_sequence=pinned.sequence,
    )[0] is True


def test_delete_and_reorder_are_detected() -> None:
    ledger, checkpoints = _reference()
    pinned = checkpoints[1]
    deleted = delete_checkpoint(checkpoints, index=1)
    reordered = reorder_checkpoints(checkpoints, first=1, second=2)

    assert verify_rotation(
        ledger,
        deleted,
        pinned_checkpoint_hash=pinned.checkpoint_hash,
        pinned_sequence=pinned.sequence,
    )[0] is False
    assert verify_rotation(
        ledger,
        reordered,
        pinned_checkpoint_hash=pinned.checkpoint_hash,
        pinned_sequence=pinned.sequence,
    )[0] is False


def test_latest_only_forgery_passes_but_pinned_history_rejects() -> None:
    ledger, checkpoints = _reference()
    rewritten = rewrite_and_rehash(
        ledger,
        index=1,
        payload_patch={"queries": 1},
    )
    forged = forge_latest_checkpoint(
        rewritten,
        ledger_id="ledger",
    )
    pinned = checkpoints[1]

    assert verify_latest_only(rewritten, forged)[0] is True
    assert verify_rotation(
        rewritten,
        checkpoints,
        pinned_checkpoint_hash=pinned.checkpoint_hash,
        pinned_sequence=pinned.sequence,
    )[0] is False


def test_checkpoint_fork_is_detected() -> None:
    ledger, checkpoints = _reference()
    fork_a, fork_b = fork_children(checkpoints[1], ledger=ledger)
    detected, parents = detect_checkpoint_forks(
        checkpoints[:2] + (fork_a, fork_b)
    )
    assert detected is True
    assert parents


def test_e020_promotion_contract() -> None:
    payload = checkpoint_rotation_report_payload(
        generation_a="g1",
        generation_b="g2",
    )
    assert (
        payload["promoted_rotation_contract"]
        == "rotating-checkpoint-chain-with-pinned-anchor-v1"
    )
    assert all(payload["promotion_gate"].values())
