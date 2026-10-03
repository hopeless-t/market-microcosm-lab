from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import re
from typing import Iterable


LEDGER_FORMAT_VERSION = 1
GENESIS_HASH = "0" * 64
HASH_RE = re.compile(r"^[0-9a-f]{64}$")

ALLOWED_EVENT_TYPES = {
    "ADAPTIVE_PROMOTION",
    "CERTIFICATE_ISSUE",
    "AUDIT_RENEWAL",
    "GENERATION_DRIFT",
    "RECERTIFY",
    "AUDIT_FAILURE",
    "REVOKE",
    "EXPIRE",
    "PORTFOLIO_SCHEDULER_PROMOTION",
    "MANDATORY_AUDIT_FAIL_CLOSED",
}


@dataclass(frozen=True)
class LedgerEntry:
    ledger_version: int
    sequence: int
    evidence_epoch: int
    event_type: str
    generation_fingerprint: str
    decision: str
    evidence_digest: str
    details: dict
    previous_hash: str
    event_hash: str


@dataclass(frozen=True)
class LedgerVerification:
    valid: bool
    reason: str
    failed_index: int | None
    tip_hash: str
    entry_count: int


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def digest_object(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _entry_body(
    *,
    ledger_version: int,
    sequence: int,
    evidence_epoch: int,
    event_type: str,
    generation_fingerprint: str,
    decision: str,
    evidence_digest: str,
    details: dict,
    previous_hash: str,
) -> dict:
    return {
        "ledger_version": ledger_version,
        "sequence": sequence,
        "evidence_epoch": evidence_epoch,
        "event_type": event_type,
        "generation_fingerprint": generation_fingerprint,
        "decision": decision,
        "evidence_digest": evidence_digest,
        "details": details,
        "previous_hash": previous_hash,
    }


def event_hash_from_body(body: dict) -> str:
    return digest_object(body)


def append_entry(
    ledger: tuple[LedgerEntry, ...],
    *,
    evidence_epoch: int,
    event_type: str,
    generation_fingerprint: str,
    decision: str,
    evidence_digest: str,
    details: dict | None = None,
) -> tuple[LedgerEntry, ...]:
    if event_type not in ALLOWED_EVENT_TYPES:
        raise ValueError(f"unsupported ledger event: {event_type}")
    if not HASH_RE.fullmatch(generation_fingerprint):
        raise ValueError("generation fingerprint must be sha256 hex")
    if not HASH_RE.fullmatch(evidence_digest):
        raise ValueError("evidence digest must be sha256 hex")

    previous_hash = ledger[-1].event_hash if ledger else GENESIS_HASH
    sequence = len(ledger)
    body = _entry_body(
        ledger_version=LEDGER_FORMAT_VERSION,
        sequence=sequence,
        evidence_epoch=evidence_epoch,
        event_type=event_type,
        generation_fingerprint=generation_fingerprint,
        decision=decision,
        evidence_digest=evidence_digest,
        details=details or {},
        previous_hash=previous_hash,
    )
    entry = LedgerEntry(
        **body,
        event_hash=event_hash_from_body(body),
    )
    return ledger + (entry,)


def verify_ledger(
    entries: Iterable[LedgerEntry | dict],
) -> LedgerVerification:
    normalized = tuple(
        entry if isinstance(entry, LedgerEntry) else LedgerEntry(**entry)
        for entry in entries
    )
    expected_previous = GENESIS_HASH
    previous_epoch = -1

    for index, entry in enumerate(normalized):
        if entry.ledger_version != LEDGER_FORMAT_VERSION:
            return LedgerVerification(
                False,
                "unsupported ledger version",
                index,
                expected_previous,
                len(normalized),
            )
        if entry.sequence != index:
            return LedgerVerification(
                False,
                "sequence discontinuity",
                index,
                expected_previous,
                len(normalized),
            )
        if entry.evidence_epoch < previous_epoch:
            return LedgerVerification(
                False,
                "evidence epoch moved backwards",
                index,
                expected_previous,
                len(normalized),
            )
        if entry.event_type not in ALLOWED_EVENT_TYPES:
            return LedgerVerification(
                False,
                "unsupported event type",
                index,
                expected_previous,
                len(normalized),
            )
        if entry.previous_hash != expected_previous:
            return LedgerVerification(
                False,
                "previous hash mismatch",
                index,
                expected_previous,
                len(normalized),
            )
        if not HASH_RE.fullmatch(entry.generation_fingerprint):
            return LedgerVerification(
                False,
                "invalid generation fingerprint",
                index,
                expected_previous,
                len(normalized),
            )
        if not HASH_RE.fullmatch(entry.evidence_digest):
            return LedgerVerification(
                False,
                "invalid evidence digest",
                index,
                expected_previous,
                len(normalized),
            )

        body = _entry_body(
            ledger_version=entry.ledger_version,
            sequence=entry.sequence,
            evidence_epoch=entry.evidence_epoch,
            event_type=entry.event_type,
            generation_fingerprint=entry.generation_fingerprint,
            decision=entry.decision,
            evidence_digest=entry.evidence_digest,
            details=entry.details,
            previous_hash=entry.previous_hash,
        )
        calculated = event_hash_from_body(body)
        if entry.event_hash != calculated:
            return LedgerVerification(
                False,
                "event hash mismatch",
                index,
                expected_previous,
                len(normalized),
            )

        expected_previous = entry.event_hash
        previous_epoch = entry.evidence_epoch

    return LedgerVerification(
        True,
        "ok",
        None,
        expected_previous,
        len(normalized),
    )


def ledger_jsonl(entries: tuple[LedgerEntry, ...]) -> str:
    return "".join(
        canonical_json(asdict(entry)) + "\n"
        for entry in entries
    )


def build_reference_ledger(
    *,
    e015_report: dict,
    e016_report: dict,
    e017_report: dict,
    e018_report: dict,
) -> tuple[LedgerEntry, ...]:
    e015_digest = digest_object(e015_report)
    e016_digest = digest_object(e016_report)
    e017_digest = digest_object(e017_report)
    e018_digest = digest_object(e018_report)

    original_generation = str(
        e016_report["same_generation"]["fingerprint"]
    )
    changed_generation = str(
        e016_report["changed_generation"]["fingerprint"]
    )

    ledger: tuple[LedgerEntry, ...] = ()

    ledger = append_entry(
        ledger,
        evidence_epoch=0,
        event_type="ADAPTIVE_PROMOTION",
        generation_fingerprint=original_generation,
        decision="bounded adaptive sampler promoted",
        evidence_digest=e015_digest,
        details={
            "candidate": e015_report["candidate"],
            "query_savings_fraction": (
                e015_report["aggregate"]["query_savings_fraction"]
            ),
        },
    )
    ledger = append_entry(
        ledger,
        evidence_epoch=0,
        event_type="CERTIFICATE_ISSUE",
        generation_fingerprint=original_generation,
        decision="adaptive authority issued",
        evidence_digest=e016_digest,
        details={
            "guard_contract_passed": e016_report["guard_contract_passed"],
        },
    )
    ledger = append_entry(
        ledger,
        evidence_epoch=3,
        event_type="AUDIT_RENEWAL",
        generation_fingerprint=original_generation,
        decision="certificate renewed after exhaustive audit",
        evidence_digest=e017_digest,
        details={
            "audit_interval_epochs": (
                e017_report["policy"]["audit_interval_epochs"]
            ),
        },
    )
    ledger = append_entry(
        ledger,
        evidence_epoch=5,
        event_type="GENERATION_DRIFT",
        generation_fingerprint=changed_generation,
        decision="old certificate invalidated",
        evidence_digest=e016_digest,
        details={
            "old_generation": original_generation,
            "new_generation": changed_generation,
        },
    )
    ledger = append_entry(
        ledger,
        evidence_epoch=5,
        event_type="RECERTIFY",
        generation_fingerprint=changed_generation,
        decision="exhaustive recertification completed",
        evidence_digest=e017_digest,
        details={
            "drift_epoch": e017_report["drift_epoch"],
            "required_mode": "exhaustive",
        },
    )
    ledger = append_entry(
        ledger,
        evidence_epoch=6,
        event_type="PORTFOLIO_SCHEDULER_PROMOTION",
        generation_fingerprint=changed_generation,
        decision="bounded-dp audit scheduler promoted",
        evidence_digest=e018_digest,
        details={
            "scheduler": e018_report["promoted_scheduler"],
            "dp_exact_match_rate": (
                e018_report["aggregate"]["dp_exact_match_rate"]
            ),
            "dp_work_reduction_fraction": (
                e018_report["aggregate"]["dp_work_reduction_fraction"]
            ),
        },
    )
    ledger = append_entry(
        ledger,
        evidence_epoch=6,
        event_type="MANDATORY_AUDIT_FAIL_CLOSED",
        generation_fingerprint=changed_generation,
        decision="infeasible mandatory audit portfolio rejected",
        evidence_digest=e018_digest,
        details={
            "fail_closed": (
                e018_report["infeasible_mandatory_case"]["dp"]["fail_closed"]
            ),
        },
    )

    return ledger


def tamper_payload(
    entries: tuple[LedgerEntry, ...],
    *,
    index: int,
) -> tuple[LedgerEntry, ...]:
    target = entries[index]
    modified_details = dict(target.details)
    modified_details["tampered"] = True
    return (
        entries[:index]
        + (replace(target, details=modified_details),)
        + entries[index + 1 :]
    )


def delete_entry(
    entries: tuple[LedgerEntry, ...],
    *,
    index: int,
) -> tuple[LedgerEntry, ...]:
    return entries[:index] + entries[index + 1 :]


def reorder_entries(
    entries: tuple[LedgerEntry, ...],
    *,
    left: int,
    right: int,
) -> tuple[LedgerEntry, ...]:
    mutable = list(entries)
    mutable[left], mutable[right] = mutable[right], mutable[left]
    return tuple(mutable)


def ledger_report_payload(
    *,
    e015_report: dict,
    e016_report: dict,
    e017_report: dict,
    e018_report: dict,
) -> tuple[dict, tuple[LedgerEntry, ...]]:
    ledger = build_reference_ledger(
        e015_report=e015_report,
        e016_report=e016_report,
        e017_report=e017_report,
        e018_report=e018_report,
    )
    clean = verify_ledger(ledger)

    duplicate_ledger = build_reference_ledger(
        e015_report=e015_report,
        e016_report=e016_report,
        e017_report=e017_report,
        e018_report=e018_report,
    )
    deterministic = (
        ledger_jsonl(ledger) == ledger_jsonl(duplicate_ledger)
        and clean.tip_hash == verify_ledger(duplicate_ledger).tip_hash
    )

    payload_tamper = verify_ledger(
        tamper_payload(ledger, index=2)
    )
    deletion = verify_ledger(
        delete_entry(ledger, index=2)
    )
    reorder = verify_ledger(
        reorder_entries(ledger, left=2, right=3)
    )

    gates = {
        "clean_chain_verifies": clean.valid,
        "deterministic_rebuild_matches_tip": deterministic,
        "payload_tamper_detected": not payload_tamper.valid,
        "entry_deletion_detected": not deletion.valid,
        "entry_reorder_detected": not reorder.valid,
        "source_evidence_digests_present": all(
            HASH_RE.fullmatch(entry.evidence_digest)
            for entry in ledger
        ),
    }

    report = {
        "experiment": "E019",
        "ledger_format_version": LEDGER_FORMAT_VERSION,
        "entry_count": len(ledger),
        "tip_hash": clean.tip_hash,
        "clean_verification": asdict(clean),
        "tamper_probes": {
            "payload_mutation": asdict(payload_tamper),
            "entry_deletion": asdict(deletion),
            "entry_reorder": asdict(reorder),
        },
        "promotion_gate": gates,
        "ledger_contract_passed": all(gates.values()),
        "source_experiments": ["E015", "E016", "E017", "E018"],
        "limitation": (
            "A local hash chain detects in-chain mutation, deletion, and reorder "
            "against a known tip. An attacker able to rewrite the entire ledger "
            "and replace the trusted tip can recompute the chain; external "
            "signatures or transparency anchoring are future work."
        ),
    }
    return report, ledger
