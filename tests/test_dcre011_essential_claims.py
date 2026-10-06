from market_microcosm.dcre011_essential_claims import (
    evidence_gate_allocate,
    frozen_claims,
    trust_claim_allocate,
    truth_oracle_allocate,
)


def test_unverified_protection_claim_is_goodharted() -> None:
    selected = trust_claim_allocate(frozen_claims())
    assert selected.actor_id == "PREMIUM"
    assert selected.claimed_essential is True
    assert selected.true_essential is False
    assert selected.system_wait_value == 0.08


def test_evidence_gate_recovers_frozen_essential_actor() -> None:
    selected = evidence_gate_allocate(frozen_claims())
    assert selected.actor_id == "ESSENTIAL"
    assert selected.true_essential is True
    assert selected.system_wait_value == 0.50


def test_evidence_gate_matches_truth_oracle_in_frozen_world() -> None:
    evidence = evidence_gate_allocate(frozen_claims())
    oracle = truth_oracle_allocate(frozen_claims())
    assert evidence.actor_id == oracle.actor_id == "ESSENTIAL"


def test_threshold_too_high_can_remove_all_protected_access() -> None:
    try:
        evidence_gate_allocate(frozen_claims(), threshold=0.95)
    except ValueError as exc:
        assert "no evidence-qualified" in str(exc)
    else:
        raise AssertionError("expected fail-closed empty qualification")
