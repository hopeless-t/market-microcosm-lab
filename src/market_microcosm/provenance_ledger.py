from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
from typing import Any


GENESIS_HASH = "0" * 64


@dataclass(frozen=True)
class LedgerEvent:
    index: int
    event_type: str
    certificate_id: str
    generation_fingerprint: str
    epoch: int
    payload: dict[str, Any]
    prev_hash: str
    event_hash: str


@dataclass(frozen=True)
class LedgerCheckpoint:
    ledger_id: str
    event_count: int
    head_hash: str
    expected_final_state: str
    expected_generation_fingerprint: str


@dataclass(frozen=True)
class ReplayState:
    certificate_id: str
    generation_fingerprint: str
    status: str
    required_mode: str
    issued_epoch: int
    last_successful_audit_epoch: int
    renewals: int
    last_event_index: int


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def _event_body(
    *,
    index: int,
    event_type: str,
    certificate_id: str,
    generation_fingerprint: str,
    epoch: int,
    payload: dict[str, Any],
    prev_hash: str,
) -> dict[str, Any]:
    return {
        "index": index,
        "event_type": event_type,
        "certificate_id": certificate_id,
        "generation_fingerprint": generation_fingerprint,
        "epoch": epoch,
        "payload": payload,
        "prev_hash": prev_hash,
    }


def event_hash_for_body(body: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()


def append_event(
    ledger: tuple[LedgerEvent, ...],
    *,
    event_type: str,
    certificate_id: str,
    generation_fingerprint: str,
    epoch: int,
    payload: dict[str, Any] | None = None,
) -> tuple[LedgerEvent, ...]:
    payload = dict(payload or {})
    index = len(ledger)
    prev_hash = ledger[-1].event_hash if ledger else GENESIS_HASH
    body = _event_body(
        index=index,
        event_type=event_type,
        certificate_id=certificate_id,
        generation_fingerprint=generation_fingerprint,
        epoch=epoch,
        payload=payload,
        prev_hash=prev_hash,
    )
    event = LedgerEvent(
        **body,
        event_hash=event_hash_for_body(body),
    )
    return ledger + (event,)


def verify_chain(ledger: tuple[LedgerEvent, ...]) -> tuple[bool, str]:
    previous = GENESIS_HASH
    for expected_index, event in enumerate(ledger):
        if event.index != expected_index:
            return False, f"index mismatch at {expected_index}"
        if event.prev_hash != previous:
            return False, f"prev_hash mismatch at {expected_index}"

        body = _event_body(
            index=event.index,
            event_type=event.event_type,
            certificate_id=event.certificate_id,
            generation_fingerprint=event.generation_fingerprint,
            epoch=event.epoch,
            payload=event.payload,
            prev_hash=event.prev_hash,
        )
        if event_hash_for_body(body) != event.event_hash:
            return False, f"event_hash mismatch at {expected_index}"
        previous = event.event_hash

    return True, "ok"


def checkpoint_for(
    ledger: tuple[LedgerEvent, ...],
    *,
    ledger_id: str,
    expected_final_state: str,
    expected_generation_fingerprint: str,
) -> LedgerCheckpoint:
    if not ledger:
        raise ValueError("cannot checkpoint empty ledger")
    return LedgerCheckpoint(
        ledger_id=ledger_id,
        event_count=len(ledger),
        head_hash=ledger[-1].event_hash,
        expected_final_state=expected_final_state,
        expected_generation_fingerprint=expected_generation_fingerprint,
    )


def verify_checkpoint(
    ledger: tuple[LedgerEvent, ...],
    checkpoint: LedgerCheckpoint,
) -> tuple[bool, str]:
    if len(ledger) != checkpoint.event_count:
        return False, "event_count mismatch"
    if not ledger:
        return False, "ledger empty"
    if ledger[-1].event_hash != checkpoint.head_hash:
        return False, "head_hash mismatch"

    state = replay_state(ledger)
    if state.status != checkpoint.expected_final_state:
        return False, "final state mismatch"
    if (
        state.generation_fingerprint
        != checkpoint.expected_generation_fingerprint
    ):
        return False, "generation fingerprint mismatch"

    return True, "ok"


def replay_state(ledger: tuple[LedgerEvent, ...]) -> ReplayState:
    if not ledger:
        raise ValueError("cannot replay empty ledger")

    certificate_id: str | None = None
    generation: str | None = None
    status = "UNISSUED"
    mode = "exhaustive"
    issued_epoch = -1
    last_audit = -1
    renewals = 0

    for event in ledger:
        if certificate_id is None:
            certificate_id = event.certificate_id
        elif event.certificate_id != certificate_id:
            raise ValueError("mixed certificate IDs in one ledger")

        if event.event_type in {"ISSUE", "RECERTIFY"}:
            generation = event.generation_fingerprint
            status = "ACTIVE"
            mode = "adaptive"
            issued_epoch = event.epoch
            last_audit = event.epoch
            if event.event_type == "RECERTIFY":
                renewals += 1

        elif event.event_type == "AUDIT_PASS":
            if generation != event.generation_fingerprint:
                raise ValueError("audit generation mismatch")
            status = "ACTIVE"
            mode = "adaptive"
            last_audit = event.epoch
            renewals += 1

        elif event.event_type == "GENERATION_MISMATCH":
            status = "GENERATION_MISMATCH"
            mode = "exhaustive"

        elif event.event_type in {"AUDIT_FAIL", "REVOKE"}:
            status = "REVOKED"
            mode = "exhaustive"

        elif event.event_type == "EXPIRE":
            status = "EXPIRED"
            mode = "exhaustive"

        elif event.event_type in {
            "ADAPTIVE_USE",
            "EXHAUSTIVE_FALLBACK",
        }:
            pass

        else:
            raise ValueError(f"unknown event type: {event.event_type}")

    assert certificate_id is not None
    assert generation is not None
    return ReplayState(
        certificate_id=certificate_id,
        generation_fingerprint=generation,
        status=status,
        required_mode=mode,
        issued_epoch=issued_epoch,
        last_successful_audit_epoch=last_audit,
        renewals=renewals,
        last_event_index=ledger[-1].index,
    )


def tamper_without_rehash(
    ledger: tuple[LedgerEvent, ...],
    *,
    index: int,
    payload_patch: dict[str, Any],
) -> tuple[LedgerEvent, ...]:
    events = list(ledger)
    target = events[index]
    payload = dict(target.payload)
    payload.update(payload_patch)
    events[index] = replace(target, payload=payload)
    return tuple(events)


def delete_event(
    ledger: tuple[LedgerEvent, ...],
    *,
    index: int,
) -> tuple[LedgerEvent, ...]:
    return tuple(
        event for position, event in enumerate(ledger) if position != index
    )


def reorder_events(
    ledger: tuple[LedgerEvent, ...],
    *,
    first: int,
    second: int,
) -> tuple[LedgerEvent, ...]:
    events = list(ledger)
    events[first], events[second] = events[second], events[first]
    return tuple(events)


def rewrite_and_rehash(
    ledger: tuple[LedgerEvent, ...],
    *,
    index: int,
    event_type: str | None = None,
    payload_patch: dict[str, Any] | None = None,
) -> tuple[LedgerEvent, ...]:
    if not 0 <= index < len(ledger):
        raise IndexError(index)

    result = ledger[:index]
    for position in range(index, len(ledger)):
        source = ledger[position]
        if position == index:
            selected_type = event_type or source.event_type
            payload = dict(source.payload)
            payload.update(payload_patch or {})
        else:
            selected_type = source.event_type
            payload = dict(source.payload)

        result = append_event(
            result,
            event_type=selected_type,
            certificate_id=source.certificate_id,
            generation_fingerprint=source.generation_fingerprint,
            epoch=source.epoch,
            payload=payload,
        )

    return result


def build_reference_ledger(
    *,
    certificate_id: str,
    generation_a: str,
    generation_b: str,
) -> tuple[LedgerEvent, ...]:
    ledger: tuple[LedgerEvent, ...] = ()
    ledger = append_event(
        ledger,
        event_type="ISSUE",
        certificate_id=certificate_id,
        generation_fingerprint=generation_a,
        epoch=0,
        payload={"source": "E014", "optimizer": "E015"},
    )
    ledger = append_event(
        ledger,
        event_type="ADAPTIVE_USE",
        certificate_id=certificate_id,
        generation_fingerprint=generation_a,
        epoch=1,
        payload={"queries": 205},
    )
    ledger = append_event(
        ledger,
        event_type="ADAPTIVE_USE",
        certificate_id=certificate_id,
        generation_fingerprint=generation_a,
        epoch=2,
        payload={"queries": 205},
    )
    ledger = append_event(
        ledger,
        event_type="AUDIT_PASS",
        certificate_id=certificate_id,
        generation_fingerprint=generation_a,
        epoch=3,
        payload={"verifier": "E014-exhaustive", "queries": 882},
    )
    ledger = append_event(
        ledger,
        event_type="ADAPTIVE_USE",
        certificate_id=certificate_id,
        generation_fingerprint=generation_a,
        epoch=4,
        payload={"queries": 205},
    )
    ledger = append_event(
        ledger,
        event_type="GENERATION_MISMATCH",
        certificate_id=certificate_id,
        generation_fingerprint=generation_a,
        epoch=5,
        payload={"next_generation": generation_b},
    )
    ledger = append_event(
        ledger,
        event_type="RECERTIFY",
        certificate_id=certificate_id,
        generation_fingerprint=generation_b,
        epoch=5,
        payload={"verifier": "E014-exhaustive", "queries": 882},
    )
    ledger = append_event(
        ledger,
        event_type="ADAPTIVE_USE",
        certificate_id=certificate_id,
        generation_fingerprint=generation_b,
        epoch=6,
        payload={"queries": 205},
    )
    return ledger


def event_dicts(
    ledger: tuple[LedgerEvent, ...],
) -> list[dict[str, Any]]:
    return [asdict(event) for event in ledger]


def provenance_report_payload(
    *,
    generation_a: str,
    generation_b: str,
) -> dict:
    certificate_id = "adaptive-boundary-sampler-v1"
    ledger = build_reference_ledger(
        certificate_id=certificate_id,
        generation_a=generation_a,
        generation_b=generation_b,
    )
    chain_valid, chain_reason = verify_chain(ledger)
    replay = replay_state(ledger)
    checkpoint = checkpoint_for(
        ledger,
        ledger_id="certificate-ledger-v1",
        expected_final_state="ACTIVE",
        expected_generation_fingerprint=generation_b,
    )
    checkpoint_valid, checkpoint_reason = verify_checkpoint(
        ledger,
        checkpoint,
    )

    payload_tamper = tamper_without_rehash(
        ledger,
        index=1,
        payload_patch={"queries": 1},
    )
    payload_tamper_valid, payload_tamper_reason = verify_chain(
        payload_tamper
    )

    deletion = delete_event(ledger, index=2)
    deletion_valid, deletion_reason = verify_chain(deletion)

    reorder = reorder_events(ledger, first=1, second=2)
    reorder_valid, reorder_reason = verify_chain(reorder)

    prefix_hashes = tuple(event.event_hash for event in ledger)
    extended = append_event(
        ledger,
        event_type="ADAPTIVE_USE",
        certificate_id=certificate_id,
        generation_fingerprint=generation_b,
        epoch=7,
        payload={"queries": 205},
    )
    extension_prefix_preserved = (
        tuple(event.event_hash for event in extended[: len(ledger)])
        == prefix_hashes
    )

    rehashed_attack = rewrite_and_rehash(
        ledger,
        index=len(ledger) - 1,
        event_type="REVOKE",
        payload_patch={"reason": "forged rewrite"},
    )
    rehashed_chain_valid, rehashed_chain_reason = verify_chain(
        rehashed_attack
    )
    attacked_replay = replay_state(rehashed_attack)
    rehashed_checkpoint_valid, rehashed_checkpoint_reason = (
        verify_checkpoint(rehashed_attack, checkpoint)
    )

    gates = {
        "reference_chain_valid": chain_valid,
        "reference_checkpoint_valid": checkpoint_valid,
        "reference_replay_active_on_new_generation": (
            replay.status == "ACTIVE"
            and replay.required_mode == "adaptive"
            and replay.generation_fingerprint == generation_b
        ),
        "payload_tamper_detected_without_rehash": not payload_tamper_valid,
        "event_deletion_detected": not deletion_valid,
        "event_reorder_detected": not reorder_valid,
        "append_only_extension_preserves_prefix_hashes": (
            extension_prefix_preserved
        ),
        "full_rehash_attack_can_fool_internal_chain_check": (
            rehashed_chain_valid
        ),
        "full_rehash_attack_changes_replayed_state": (
            attacked_replay.status == "REVOKED"
            and replay.status != attacked_replay.status
        ),
        "external_checkpoint_detects_full_rehash_attack": (
            not rehashed_checkpoint_valid
        ),
    }

    return {
        "experiment": "E019",
        "ledger_contract": "sha256-hash-chain-plus-external-checkpoint-v1",
        "reference": {
            "events": event_dicts(ledger),
            "chain_valid": chain_valid,
            "chain_reason": chain_reason,
            "replay_state": asdict(replay),
            "checkpoint": asdict(checkpoint),
            "checkpoint_valid": checkpoint_valid,
            "checkpoint_reason": checkpoint_reason,
        },
        "attacks": {
            "payload_tamper_without_rehash": {
                "chain_valid": payload_tamper_valid,
                "reason": payload_tamper_reason,
            },
            "delete_event": {
                "chain_valid": deletion_valid,
                "reason": deletion_reason,
            },
            "reorder_events": {
                "chain_valid": reorder_valid,
                "reason": reorder_reason,
            },
            "full_rehash_rewrite": {
                "chain_valid": rehashed_chain_valid,
                "chain_reason": rehashed_chain_reason,
                "replay_state": asdict(attacked_replay),
                "checkpoint_valid": rehashed_checkpoint_valid,
                "checkpoint_reason": rehashed_checkpoint_reason,
            },
        },
        "append_extension": {
            "prefix_hashes_preserved": extension_prefix_preserved,
            "old_event_count": len(ledger),
            "new_event_count": len(extended),
            "new_head_hash": extended[-1].event_hash,
        },
        "promotion_gate": gates,
        "promoted_ledger_contract": (
            "sha256-hash-chain-plus-external-checkpoint-v1"
            if all(gates.values())
            else None
        ),
        "limitation": (
            "A hash chain alone is not an authorship proof. A trusted "
            "out-of-ledger checkpoint or stronger external transparency/"
            "signature mechanism is required to detect a fully rehashed rewrite."
        ),
    }
