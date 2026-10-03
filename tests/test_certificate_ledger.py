from market_microcosm.certificate_ledger import (
    append_entry,
    delete_entry,
    digest_object,
    ledger_jsonl,
    reorder_entries,
    tamper_payload,
    verify_ledger,
)


def _ledger():
    generation = digest_object({"generation": 1})
    evidence = digest_object({"evidence": 1})
    ledger = ()
    ledger = append_entry(
        ledger,
        evidence_epoch=0,
        event_type="CERTIFICATE_ISSUE",
        generation_fingerprint=generation,
        decision="issued",
        evidence_digest=evidence,
    )
    ledger = append_entry(
        ledger,
        evidence_epoch=3,
        event_type="AUDIT_RENEWAL",
        generation_fingerprint=generation,
        decision="renewed",
        evidence_digest=evidence,
    )
    ledger = append_entry(
        ledger,
        evidence_epoch=6,
        event_type="PORTFOLIO_SCHEDULER_PROMOTION",
        generation_fingerprint=generation,
        decision="scheduler promoted",
        evidence_digest=evidence,
    )
    return ledger


def test_clean_ledger_verifies_and_is_deterministic() -> None:
    first = _ledger()
    second = _ledger()
    assert verify_ledger(first).valid is True
    assert ledger_jsonl(first) == ledger_jsonl(second)
    assert verify_ledger(first).tip_hash == verify_ledger(second).tip_hash


def test_payload_tamper_is_detected() -> None:
    ledger = _ledger()
    assert verify_ledger(tamper_payload(ledger, index=1)).valid is False


def test_deletion_is_detected() -> None:
    ledger = _ledger()
    assert verify_ledger(delete_entry(ledger, index=1)).valid is False


def test_reordering_is_detected() -> None:
    ledger = _ledger()
    assert verify_ledger(
        reorder_entries(ledger, left=1, right=2)
    ).valid is False
