from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
import hashlib
import hmac
from typing import Iterable

from .checkpoint_rotation import build_rotation, extend_reference_ledger


DOMAIN = b"market-microcosm/checkpoint-witness/v1:"


@dataclass(frozen=True)
class Witness:
    witness_id: str
    secret: str


@dataclass(frozen=True)
class Attestation:
    sequence: int
    checkpoint_hash: str
    witness_id: str
    signature: str


@dataclass(frozen=True)
class QuorumVerification:
    valid: bool
    threshold: int
    valid_witnesses: tuple[str, ...]
    invalid_witnesses: tuple[str, ...]
    reason: str


def witness_registry(count: int = 5) -> tuple[Witness, ...]:
    return tuple(
        Witness(
            witness_id=f"witness-{index}",
            secret=f"e021-synthetic-secret-{index}",
        )
        for index in range(count)
    )


def attestation_message(*, sequence: int, checkpoint_hash: str) -> bytes:
    return (
        DOMAIN
        + str(sequence).encode("ascii")
        + b":"
        + checkpoint_hash.encode("ascii")
    )


def sign(
    witness: Witness,
    *,
    sequence: int,
    checkpoint_hash: str,
) -> Attestation:
    signature = hmac.new(
        witness.secret.encode("utf-8"),
        attestation_message(
            sequence=sequence,
            checkpoint_hash=checkpoint_hash,
        ),
        hashlib.sha256,
    ).hexdigest()
    return Attestation(
        sequence=sequence,
        checkpoint_hash=checkpoint_hash,
        witness_id=witness.witness_id,
        signature=signature,
    )


def verify_attestation(
    attestation: Attestation,
    *,
    witnesses: dict[str, Witness],
) -> bool:
    witness = witnesses.get(attestation.witness_id)
    if witness is None:
        return False
    expected = sign(
        witness,
        sequence=attestation.sequence,
        checkpoint_hash=attestation.checkpoint_hash,
    ).signature
    return hmac.compare_digest(expected, attestation.signature)


def verify_quorum(
    attestations: Iterable[Attestation],
    *,
    sequence: int,
    checkpoint_hash: str,
    witnesses: tuple[Witness, ...],
    threshold: int,
) -> QuorumVerification:
    registry = {w.witness_id: w for w in witnesses}
    valid: set[str] = set()
    invalid: set[str] = set()

    for attestation in attestations:
        if (
            attestation.sequence != sequence
            or attestation.checkpoint_hash != checkpoint_hash
        ):
            invalid.add(attestation.witness_id)
            continue

        if verify_attestation(attestation, witnesses=registry):
            valid.add(attestation.witness_id)
        else:
            invalid.add(attestation.witness_id)

    ok = len(valid) >= threshold
    return QuorumVerification(
        valid=ok,
        threshold=threshold,
        valid_witnesses=tuple(sorted(valid)),
        invalid_witnesses=tuple(sorted(invalid)),
        reason=(
            "quorum satisfied"
            if ok
            else f"valid witnesses {len(valid)} below threshold {threshold}"
        ),
    )


def detect_equivocation(
    attestations: Iterable[Attestation],
) -> dict[str, tuple[str, ...]]:
    by_witness_sequence: dict[tuple[str, int], set[str]] = {}
    for attestation in attestations:
        key = (attestation.witness_id, attestation.sequence)
        by_witness_sequence.setdefault(key, set()).add(
            attestation.checkpoint_hash
        )

    evidence: dict[str, tuple[str, ...]] = {}
    for (witness_id, sequence), hashes in by_witness_sequence.items():
        if len(hashes) > 1:
            evidence[f"{witness_id}@{sequence}"] = tuple(sorted(hashes))
    return evidence


def quorum_sets(
    witness_count: int,
    threshold: int,
) -> tuple[tuple[int, ...], ...]:
    return tuple(combinations(range(witness_count), threshold))


def quorum_intersection_report(
    witness_count: int,
    threshold: int,
) -> dict:
    quorums = quorum_sets(witness_count, threshold)
    pair_count = 0
    disjoint_pairs = 0
    minimum_intersection: int | None = None

    for left_index, left in enumerate(quorums):
        left_set = set(left)
        for right in quorums[left_index + 1 :]:
            pair_count += 1
            intersection = len(left_set.intersection(right))
            if minimum_intersection is None:
                minimum_intersection = intersection
            else:
                minimum_intersection = min(
                    minimum_intersection,
                    intersection,
                )
            if intersection == 0:
                disjoint_pairs += 1

    return {
        "witness_count": witness_count,
        "threshold": threshold,
        "quorum_count": len(quorums),
        "quorum_pair_count": pair_count,
        "minimum_intersection": (
            0 if minimum_intersection is None else minimum_intersection
        ),
        "disjoint_quorum_pairs": disjoint_pairs,
        "strict_majority": 2 * threshold > witness_count,
    }


def _signers(
    witnesses: tuple[Witness, ...],
    indexes: tuple[int, ...],
    *,
    sequence: int,
    checkpoint_hash: str,
) -> tuple[Attestation, ...]:
    return tuple(
        sign(
            witnesses[index],
            sequence=sequence,
            checkpoint_hash=checkpoint_hash,
        )
        for index in indexes
    )


def witness_quorum_report_payload(
    *,
    generation_a: str,
    generation_b: str,
) -> dict:
    witnesses = witness_registry(5)
    threshold = 3

    ledger = extend_reference_ledger(
        generation_a=generation_a,
        generation_b=generation_b,
    )
    rotation = build_rotation(
        ledger,
        ledger_id="certificate-ledger-v1",
        event_counts=(2, 4, 6, 8),
    )
    checkpoint = rotation[-1]
    sequence = checkpoint.sequence
    honest_hash = checkpoint.checkpoint_hash
    forged_hash = hashlib.sha256(
        ("forged:" + honest_hash).encode("ascii")
    ).hexdigest()

    honest_attestations = _signers(
        witnesses,
        (0, 1, 2),
        sequence=sequence,
        checkpoint_hash=honest_hash,
    )
    honest = verify_quorum(
        honest_attestations,
        sequence=sequence,
        checkpoint_hash=honest_hash,
        witnesses=witnesses,
        threshold=threshold,
    )

    compromise_results = {}
    for compromised_count in (1, 2, 3):
        indexes = tuple(range(compromised_count))
        attestations = _signers(
            witnesses,
            indexes,
            sequence=sequence,
            checkpoint_hash=forged_hash,
        )
        verification = verify_quorum(
            attestations,
            sequence=sequence,
            checkpoint_hash=forged_hash,
            witnesses=witnesses,
            threshold=threshold,
        )
        compromise_results[str(compromised_count)] = asdict(verification)

    view_a_attestations = _signers(
        witnesses,
        (0, 1, 2),
        sequence=sequence,
        checkpoint_hash=honest_hash,
    )
    view_b_attestations = _signers(
        witnesses,
        (2, 3, 4),
        sequence=sequence,
        checkpoint_hash=forged_hash,
    )
    view_a = verify_quorum(
        view_a_attestations,
        sequence=sequence,
        checkpoint_hash=honest_hash,
        witnesses=witnesses,
        threshold=threshold,
    )
    view_b = verify_quorum(
        view_b_attestations,
        sequence=sequence,
        checkpoint_hash=forged_hash,
        witnesses=witnesses,
        threshold=threshold,
    )
    equivocation = detect_equivocation(
        view_a_attestations + view_b_attestations
    )

    majority_geometry = quorum_intersection_report(5, 3)
    weak_geometry = quorum_intersection_report(5, 2)

    bad_signature = replace_signature(
        honest_attestations[0],
        signature="0" * 64,
    )
    bad_signature_check = verify_attestation(
        bad_signature,
        witnesses={w.witness_id: w for w in witnesses},
    )

    gates = {
        "honest_three_of_five_quorum_valid": honest.valid,
        "one_compromised_witness_cannot_forge": (
            not compromise_results["1"]["valid"]
        ),
        "two_compromised_witnesses_cannot_forge": (
            not compromise_results["2"]["valid"]
        ),
        "three_compromised_witnesses_define_forge_boundary": (
            compromise_results["3"]["valid"]
        ),
        "three_of_five_quorums_always_intersect": (
            majority_geometry["minimum_intersection"] >= 1
            and majority_geometry["disjoint_quorum_pairs"] == 0
        ),
        "two_of_five_can_form_disjoint_quorums": (
            weak_geometry["disjoint_quorum_pairs"] > 0
        ),
        "conflicting_three_of_five_views_both_verify": (
            view_a.valid and view_b.valid
        ),
        "conflicting_quorums_leave_equivocation_evidence": (
            bool(equivocation)
        ),
        "invalid_signature_rejected": not bad_signature_check,
    }

    return {
        "experiment": "E021",
        "contract": "three-of-five-witness-quorum-with-equivocation-detection-v1",
        "checkpoint": {
            "sequence": sequence,
            "checkpoint_hash": honest_hash,
            "forged_checkpoint_hash": forged_hash,
        },
        "witnesses": [w.witness_id for w in witnesses],
        "threshold": threshold,
        "honest_quorum": asdict(honest),
        "compromise_boundary": compromise_results,
        "quorum_geometry": {
            "three_of_five": majority_geometry,
            "two_of_five": weak_geometry,
        },
        "split_view": {
            "view_a": asdict(view_a),
            "view_b": asdict(view_b),
            "equivocation_evidence": equivocation,
        },
        "invalid_signature_rejected": not bad_signature_check,
        "promotion_gate": gates,
        "promoted_witness_contract": (
            "three-of-five-witness-quorum-with-equivocation-detection-v1"
            if all(gates.values())
            else None
        ),
        "limitation": (
            "Witness independence is simulated with in-process HMAC keys. "
            "A real deployment needs independent failure domains, protected "
            "private keys, authenticated publication, and evidence retention."
        ),
    }


def replace_signature(
    attestation: Attestation,
    *,
    signature: str,
) -> Attestation:
    return Attestation(
        sequence=attestation.sequence,
        checkpoint_hash=attestation.checkpoint_hash,
        witness_id=attestation.witness_id,
        signature=signature,
    )
