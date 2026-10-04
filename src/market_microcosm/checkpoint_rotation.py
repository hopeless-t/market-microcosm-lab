from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
from typing import Any

from .provenance_ledger import (
    GENESIS_HASH,
    LedgerEvent,
    append_event,
    build_reference_ledger,
    replay_state,
    rewrite_and_rehash,
    verify_chain,
)


CHECKPOINT_GENESIS = "0" * 64


@dataclass(frozen=True)
class RotatingCheckpoint:
    sequence: int
    ledger_id: str
    event_count: int
    ledger_head_hash: str
    previous_checkpoint_hash: str
    checkpoint_hash: str


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def _checkpoint_body(
    *,
    sequence: int,
    ledger_id: str,
    event_count: int,
    ledger_head_hash: str,
    previous_checkpoint_hash: str,
) -> dict[str, Any]:
    return {
        "sequence": sequence,
        "ledger_id": ledger_id,
        "event_count": event_count,
        "ledger_head_hash": ledger_head_hash,
        "previous_checkpoint_hash": previous_checkpoint_hash,
    }


def checkpoint_hash_for_body(body: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()


def append_checkpoint(
    checkpoints: tuple[RotatingCheckpoint, ...],
    *,
    ledger: tuple[LedgerEvent, ...],
    ledger_id: str,
    event_count: int,
) -> tuple[RotatingCheckpoint, ...]:
    if not 1 <= event_count <= len(ledger):
        raise ValueError("event_count outside ledger")
    if checkpoints and event_count <= checkpoints[-1].event_count:
        raise ValueError("checkpoint event_count must increase")

    sequence = len(checkpoints)
    previous_checkpoint_hash = (
        checkpoints[-1].checkpoint_hash
        if checkpoints
        else CHECKPOINT_GENESIS
    )
    body = _checkpoint_body(
        sequence=sequence,
        ledger_id=ledger_id,
        event_count=event_count,
        ledger_head_hash=ledger[event_count - 1].event_hash,
        previous_checkpoint_hash=previous_checkpoint_hash,
    )
    checkpoint = RotatingCheckpoint(
        **body,
        checkpoint_hash=checkpoint_hash_for_body(body),
    )
    return checkpoints + (checkpoint,)


def build_rotation(
    ledger: tuple[LedgerEvent, ...],
    *,
    ledger_id: str,
    event_counts: tuple[int, ...],
) -> tuple[RotatingCheckpoint, ...]:
    checkpoints: tuple[RotatingCheckpoint, ...] = ()
    for event_count in event_counts:
        checkpoints = append_checkpoint(
            checkpoints,
            ledger=ledger,
            ledger_id=ledger_id,
            event_count=event_count,
        )
    return checkpoints


def verify_latest_only(
    ledger: tuple[LedgerEvent, ...],
    checkpoint: RotatingCheckpoint,
) -> tuple[bool, str]:
    chain_ok, reason = verify_chain(ledger)
    if not chain_ok:
        return False, f"ledger chain invalid: {reason}"
    if checkpoint.event_count > len(ledger):
        return False, "checkpoint beyond ledger"
    if (
        ledger[checkpoint.event_count - 1].event_hash
        != checkpoint.ledger_head_hash
    ):
        return False, "ledger head mismatch"

    body = _checkpoint_body(
        sequence=checkpoint.sequence,
        ledger_id=checkpoint.ledger_id,
        event_count=checkpoint.event_count,
        ledger_head_hash=checkpoint.ledger_head_hash,
        previous_checkpoint_hash=checkpoint.previous_checkpoint_hash,
    )
    if checkpoint_hash_for_body(body) != checkpoint.checkpoint_hash:
        return False, "checkpoint hash mismatch"
    return True, "ok"


def verify_rotation(
    ledger: tuple[LedgerEvent, ...],
    checkpoints: tuple[RotatingCheckpoint, ...],
    *,
    pinned_checkpoint_hash: str | None = None,
    pinned_sequence: int | None = None,
) -> tuple[bool, str]:
    chain_ok, reason = verify_chain(ledger)
    if not chain_ok:
        return False, f"ledger chain invalid: {reason}"
    if not checkpoints:
        return False, "no checkpoints"

    previous_hash = CHECKPOINT_GENESIS
    previous_count = 0
    seen_ids: set[str] = set()
    pinned_seen = pinned_checkpoint_hash is None

    for expected_sequence, checkpoint in enumerate(checkpoints):
        if checkpoint.sequence != expected_sequence:
            return False, f"sequence mismatch at {expected_sequence}"
        if checkpoint.ledger_id in seen_ids:
            pass
        seen_ids.add(checkpoint.ledger_id)
        if checkpoint.previous_checkpoint_hash != previous_hash:
            return False, f"checkpoint link mismatch at {expected_sequence}"
        if checkpoint.event_count <= previous_count:
            return False, f"non-increasing event_count at {expected_sequence}"
        if checkpoint.event_count > len(ledger):
            return False, f"checkpoint beyond ledger at {expected_sequence}"
        if (
            ledger[checkpoint.event_count - 1].event_hash
            != checkpoint.ledger_head_hash
        ):
            return False, f"ledger prefix mismatch at {expected_sequence}"

        body = _checkpoint_body(
            sequence=checkpoint.sequence,
            ledger_id=checkpoint.ledger_id,
            event_count=checkpoint.event_count,
            ledger_head_hash=checkpoint.ledger_head_hash,
            previous_checkpoint_hash=checkpoint.previous_checkpoint_hash,
        )
        if checkpoint_hash_for_body(body) != checkpoint.checkpoint_hash:
            return False, f"checkpoint hash mismatch at {expected_sequence}"

        if (
            pinned_checkpoint_hash is not None
            and checkpoint.checkpoint_hash == pinned_checkpoint_hash
        ):
            if (
                pinned_sequence is not None
                and checkpoint.sequence != pinned_sequence
            ):
                return False, "pinned checkpoint sequence mismatch"
            pinned_seen = True

        previous_hash = checkpoint.checkpoint_hash
        previous_count = checkpoint.event_count

    if not pinned_seen:
        return False, "pinned checkpoint missing"
    return True, "ok"


def forge_latest_checkpoint(
    ledger: tuple[LedgerEvent, ...],
    *,
    ledger_id: str,
) -> RotatingCheckpoint:
    body = _checkpoint_body(
        sequence=0,
        ledger_id=ledger_id,
        event_count=len(ledger),
        ledger_head_hash=ledger[-1].event_hash,
        previous_checkpoint_hash=CHECKPOINT_GENESIS,
    )
    return RotatingCheckpoint(
        **body,
        checkpoint_hash=checkpoint_hash_for_body(body),
    )


def delete_checkpoint(
    checkpoints: tuple[RotatingCheckpoint, ...],
    *,
    index: int,
) -> tuple[RotatingCheckpoint, ...]:
    return tuple(
        checkpoint
        for position, checkpoint in enumerate(checkpoints)
        if position != index
    )


def reorder_checkpoints(
    checkpoints: tuple[RotatingCheckpoint, ...],
    *,
    first: int,
    second: int,
) -> tuple[RotatingCheckpoint, ...]:
    rows = list(checkpoints)
    rows[first], rows[second] = rows[second], rows[first]
    return tuple(rows)


def fork_children(
    checkpoint: RotatingCheckpoint,
    *,
    ledger: tuple[LedgerEvent, ...],
) -> tuple[RotatingCheckpoint, RotatingCheckpoint]:
    next_count = min(len(ledger), checkpoint.event_count + 1)

    def make(label: str) -> RotatingCheckpoint:
        body = _checkpoint_body(
            sequence=checkpoint.sequence + 1,
            ledger_id=f"{checkpoint.ledger_id}:{label}",
            event_count=next_count,
            ledger_head_hash=ledger[next_count - 1].event_hash,
            previous_checkpoint_hash=checkpoint.checkpoint_hash,
        )
        return RotatingCheckpoint(
            **body,
            checkpoint_hash=checkpoint_hash_for_body(body),
        )

    return make("fork-a"), make("fork-b")


def detect_checkpoint_forks(
    checkpoints: tuple[RotatingCheckpoint, ...],
) -> tuple[bool, tuple[str, ...]]:
    children_by_parent: dict[str, set[str]] = {}
    for checkpoint in checkpoints:
        children_by_parent.setdefault(
            checkpoint.previous_checkpoint_hash,
            set(),
        ).add(checkpoint.checkpoint_hash)

    forked_parents = tuple(
        sorted(
            parent
            for parent, children in children_by_parent.items()
            if parent != CHECKPOINT_GENESIS and len(children) > 1
        )
    )
    return bool(forked_parents), forked_parents


def extend_reference_ledger(
    *,
    generation_a: str,
    generation_b: str,
) -> tuple[LedgerEvent, ...]:
    ledger = build_reference_ledger(
        certificate_id="adaptive-boundary-sampler-v1",
        generation_a=generation_a,
        generation_b=generation_b,
    )
    ledger = append_event(
        ledger,
        event_type="ADAPTIVE_USE",
        certificate_id="adaptive-boundary-sampler-v1",
        generation_fingerprint=generation_b,
        epoch=7,
        payload={"queries": 205},
    )
    ledger = append_event(
        ledger,
        event_type="AUDIT_PASS",
        certificate_id="adaptive-boundary-sampler-v1",
        generation_fingerprint=generation_b,
        epoch=8,
        payload={"verifier": "E014-exhaustive", "queries": 882},
    )
    return ledger


def checkpoint_rotation_report_payload(
    *,
    generation_a: str,
    generation_b: str,
) -> dict:
    ledger = extend_reference_ledger(
        generation_a=generation_a,
        generation_b=generation_b,
    )
    checkpoints = build_rotation(
        ledger,
        ledger_id="certificate-ledger-v1",
        event_counts=(2, 4, 6, 8),
    )
    rotation_ok, rotation_reason = verify_rotation(ledger, checkpoints)

    pinned = checkpoints[1]
    pinned_ok, pinned_reason = verify_rotation(
        ledger,
        checkpoints,
        pinned_checkpoint_hash=pinned.checkpoint_hash,
        pinned_sequence=pinned.sequence,
    )

    deleted = delete_checkpoint(checkpoints, index=1)
    deleted_ok, deleted_reason = verify_rotation(
        ledger,
        deleted,
        pinned_checkpoint_hash=pinned.checkpoint_hash,
        pinned_sequence=pinned.sequence,
    )

    reordered = reorder_checkpoints(checkpoints, first=1, second=2)
    reordered_ok, reordered_reason = verify_rotation(
        ledger,
        reordered,
        pinned_checkpoint_hash=pinned.checkpoint_hash,
        pinned_sequence=pinned.sequence,
    )

    rewritten = rewrite_and_rehash(
        ledger,
        index=1,
        payload_patch={"queries": 1, "attack": "rewrite-old-prefix"},
    )
    forged_latest = forge_latest_checkpoint(
        rewritten,
        ledger_id="certificate-ledger-v1",
    )
    latest_only_ok, latest_only_reason = verify_latest_only(
        rewritten,
        forged_latest,
    )
    pinned_rotation_attack_ok, pinned_rotation_attack_reason = (
        verify_rotation(
            rewritten,
            checkpoints,
            pinned_checkpoint_hash=pinned.checkpoint_hash,
            pinned_sequence=pinned.sequence,
        )
    )

    fork_a, fork_b = fork_children(
        checkpoints[1],
        ledger=ledger,
    )
    fork_detected, forked_parents = detect_checkpoint_forks(
        checkpoints[:2] + (fork_a, fork_b)
    )

    unanchored_tail_events = len(ledger) - checkpoints[-1].event_count
    replay = replay_state(ledger)

    gates = {
        "honest_rotation_valid": rotation_ok,
        "pinned_checkpoint_continuity_valid": pinned_ok,
        "checkpoint_deletion_detected": not deleted_ok,
        "checkpoint_reorder_detected": not reordered_ok,
        "latest_only_forgery_can_self_consistently_pass": latest_only_ok,
        "pinned_rotation_rejects_rewritten_prefix": (
            not pinned_rotation_attack_ok
        ),
        "checkpoint_fork_detected": fork_detected,
        "reference_replay_remains_active": (
            replay.status == "ACTIVE"
            and replay.required_mode == "adaptive"
        ),
    }

    return {
        "experiment": "E020",
        "contract": "rotating-checkpoint-chain-with-pinned-anchor-v1",
        "reference": {
            "ledger_event_count": len(ledger),
            "checkpoints": [asdict(x) for x in checkpoints],
            "rotation_valid": rotation_ok,
            "rotation_reason": rotation_reason,
            "pinned_checkpoint": asdict(pinned),
            "pinned_rotation_valid": pinned_ok,
            "pinned_rotation_reason": pinned_reason,
            "replay_state": asdict(replay),
            "anchored_event_count": checkpoints[-1].event_count,
            "unanchored_tail_events": unanchored_tail_events,
        },
        "attacks": {
            "delete_checkpoint": {
                "rotation_valid": deleted_ok,
                "reason": deleted_reason,
            },
            "reorder_checkpoints": {
                "rotation_valid": reordered_ok,
                "reason": reordered_reason,
            },
            "latest_only_forgery": {
                "latest_only_valid": latest_only_ok,
                "latest_only_reason": latest_only_reason,
                "pinned_rotation_valid": pinned_rotation_attack_ok,
                "pinned_rotation_reason": pinned_rotation_attack_reason,
            },
            "checkpoint_fork": {
                "detected": fork_detected,
                "forked_parents": forked_parents,
            },
        },
        "promotion_gate": gates,
        "promoted_rotation_contract": (
            "rotating-checkpoint-chain-with-pinned-anchor-v1"
            if all(gates.values())
            else None
        ),
        "limitation": (
            "Checkpoint continuity assumes at least one independently trusted "
            "pinned checkpoint. If the external anchor authority itself is "
            "compromised and can mint replacement anchors, signatures or an "
            "independent transparency mechanism are still required."
        ),
    }
