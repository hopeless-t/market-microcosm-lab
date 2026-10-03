from market_microcosm.certificate_lifecycle import (
    ACTIVE,
    ADAPTIVE,
    AUDIT_DUE,
    EXHAUSTIVE,
    EXPIRED,
    GENERATION_MISMATCH,
    REVOKED,
    LifecyclePolicy,
    decide,
    issue_certificate,
    record_audit,
    stable_schedule,
)


def test_periodic_audit_and_hard_expiry() -> None:
    policy = LifecyclePolicy(audit_interval_epochs=3, expiry_epochs=6)
    cert = issue_certificate(generation_fingerprint="g1", epoch=0)

    assert decide(
        cert,
        epoch=2,
        current_generation_fingerprint="g1",
        policy=policy,
    ).state == ACTIVE
    assert decide(
        cert,
        epoch=3,
        current_generation_fingerprint="g1",
        policy=policy,
    ).state == AUDIT_DUE
    assert decide(
        cert,
        epoch=6,
        current_generation_fingerprint="g1",
        policy=policy,
    ).state == EXPIRED


def test_generation_mismatch_is_exhaustive() -> None:
    cert = issue_certificate(generation_fingerprint="g1", epoch=0)
    d = decide(
        cert,
        epoch=1,
        current_generation_fingerprint="g2",
        policy=LifecyclePolicy(),
    )
    assert d.state == GENERATION_MISMATCH
    assert d.required_mode == EXHAUSTIVE


def test_failed_audit_revokes_certificate() -> None:
    cert = issue_certificate(generation_fingerprint="g1", epoch=0)
    cert = record_audit(
        cert,
        epoch=3,
        audit_passed=False,
        current_generation_fingerprint="g1",
    )
    d = decide(
        cert,
        epoch=4,
        current_generation_fingerprint="g1",
        policy=LifecyclePolicy(),
    )
    assert d.state == REVOKED
    assert d.required_mode == EXHAUSTIVE


def test_successful_audit_renews_adaptive_window() -> None:
    cert = issue_certificate(generation_fingerprint="g1", epoch=0)
    cert = record_audit(
        cert,
        epoch=3,
        audit_passed=True,
        current_generation_fingerprint="g1",
    )
    d = decide(
        cert,
        epoch=4,
        current_generation_fingerprint="g1",
        policy=LifecyclePolicy(),
    )
    assert d.state == ACTIVE
    assert d.required_mode == ADAPTIVE


def test_stable_schedule_uses_exhaustive_only_for_issue_and_audits() -> None:
    steps = stable_schedule(
        epochs=7,
        generation_fingerprint="g1",
        adaptive_query_cost=205,
        exhaustive_query_cost=882,
        policy=LifecyclePolicy(),
    )
    assert [step.mode for step in steps] == [
        EXHAUSTIVE,
        ADAPTIVE,
        ADAPTIVE,
        EXHAUSTIVE,
        ADAPTIVE,
        ADAPTIVE,
        EXHAUSTIVE,
    ]
