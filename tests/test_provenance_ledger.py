from market_microcosm.provenance_ledger import (
    append_event,
    build_reference_ledger,
    checkpoint_for,
    delete_event,
    replay_state,
    reorder_events,
    rewrite_and_rehash,
    tamper_without_rehash,
    verify_chain,
    verify_checkpoint,
)


def _ledger():
    return build_reference_ledger(
        certificate_id="cert",
        generation_a="g1",
        generation_b="g2",
    )


def test_reference_chain_replays_active_generation() -> None:
    ledger = _ledger()
    ok, _ = verify_chain(ledger)
    state = replay_state(ledger)
    assert ok
    assert state.status == "ACTIVE"
    assert state.required_mode == "adaptive"
    assert state.generation_fingerprint == "g2"


def test_direct_tamper_delete_and_reorder_are_detected() -> None:
    ledger = _ledger()
    tampered = tamper_without_rehash(
        ledger,
        index=1,
        payload_patch={"queries": 1},
    )
    deleted = delete_event(ledger, index=2)
    reordered = reorder_events(ledger, first=1, second=2)

    assert verify_chain(tampered)[0] is False
    assert verify_chain(deleted)[0] is False
    assert verify_chain(reordered)[0] is False


def test_append_only_extension_preserves_prefix_hashes() -> None:
    ledger = _ledger()
    hashes = tuple(event.event_hash for event in ledger)
    extended = append_event(
        ledger,
        event_type="ADAPTIVE_USE",
        certificate_id="cert",
        generation_fingerprint="g2",
        epoch=7,
        payload={"queries": 205},
    )
    assert tuple(event.event_hash for event in extended[:len(ledger)]) == hashes


def test_external_checkpoint_detects_full_rehash_rewrite() -> None:
    ledger = _ledger()
    checkpoint = checkpoint_for(
        ledger,
        ledger_id="ledger",
        expected_final_state="ACTIVE",
        expected_generation_fingerprint="g2",
    )
    attack = rewrite_and_rehash(
        ledger,
        index=len(ledger) - 1,
        event_type="REVOKE",
        payload_patch={"reason": "forged rewrite"},
    )

    assert verify_chain(attack)[0] is True
    assert replay_state(attack).status == "REVOKED"
    assert verify_checkpoint(attack, checkpoint)[0] is False
