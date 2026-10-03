from __future__ import annotations

from dataclasses import asdict, dataclass, replace


ACTIVE = "ACTIVE"
AUDIT_DUE = "AUDIT_DUE"
EXPIRED = "EXPIRED"
REVOKED = "REVOKED"
GENERATION_MISMATCH = "GENERATION_MISMATCH"

ADAPTIVE = "adaptive"
EXHAUSTIVE = "exhaustive"


@dataclass(frozen=True)
class LifecyclePolicy:
    audit_interval_epochs: int = 3
    expiry_epochs: int = 6

    def validate(self) -> None:
        if self.audit_interval_epochs <= 0:
            raise ValueError("audit_interval_epochs must be positive")
        if self.expiry_epochs <= self.audit_interval_epochs:
            raise ValueError("expiry_epochs must exceed audit_interval_epochs")


@dataclass(frozen=True)
class CertificateState:
    generation_fingerprint: str
    issued_epoch: int
    last_successful_audit_epoch: int
    renewals: int = 0
    revoked: bool = False
    revocation_reason: str | None = None


@dataclass(frozen=True)
class CertificateDecision:
    epoch: int
    state: str
    required_mode: str
    evidence_age: int
    audit_age: int
    reason: str


@dataclass(frozen=True)
class LifecycleStep:
    epoch: int
    event: str
    generation_fingerprint: str
    state: str
    mode: str
    query_cost: int
    certificate_renewals: int
    reason: str


def issue_certificate(
    *,
    generation_fingerprint: str,
    epoch: int,
) -> CertificateState:
    return CertificateState(
        generation_fingerprint=generation_fingerprint,
        issued_epoch=epoch,
        last_successful_audit_epoch=epoch,
    )


def decide(
    certificate: CertificateState,
    *,
    epoch: int,
    current_generation_fingerprint: str,
    policy: LifecyclePolicy,
) -> CertificateDecision:
    policy.validate()
    if epoch < certificate.issued_epoch:
        raise ValueError("epoch precedes certificate issuance")

    evidence_age = epoch - certificate.issued_epoch
    audit_age = epoch - certificate.last_successful_audit_epoch

    if certificate.revoked:
        return CertificateDecision(
            epoch=epoch,
            state=REVOKED,
            required_mode=EXHAUSTIVE,
            evidence_age=evidence_age,
            audit_age=audit_age,
            reason=certificate.revocation_reason or "certificate revoked",
        )

    if certificate.generation_fingerprint != current_generation_fingerprint:
        return CertificateDecision(
            epoch=epoch,
            state=GENERATION_MISMATCH,
            required_mode=EXHAUSTIVE,
            evidence_age=evidence_age,
            audit_age=audit_age,
            reason="generation fingerprint changed",
        )

    if audit_age >= policy.expiry_epochs:
        return CertificateDecision(
            epoch=epoch,
            state=EXPIRED,
            required_mode=EXHAUSTIVE,
            evidence_age=evidence_age,
            audit_age=audit_age,
            reason="audit evidence exceeded hard expiry",
        )

    if audit_age >= policy.audit_interval_epochs:
        return CertificateDecision(
            epoch=epoch,
            state=AUDIT_DUE,
            required_mode=EXHAUSTIVE,
            evidence_age=evidence_age,
            audit_age=audit_age,
            reason="periodic exhaustive audit due",
        )

    return CertificateDecision(
        epoch=epoch,
        state=ACTIVE,
        required_mode=ADAPTIVE,
        evidence_age=evidence_age,
        audit_age=audit_age,
        reason="certificate current",
    )


def record_audit(
    certificate: CertificateState,
    *,
    epoch: int,
    audit_passed: bool,
    current_generation_fingerprint: str,
) -> CertificateState:
    if current_generation_fingerprint != certificate.generation_fingerprint:
        return replace(
            certificate,
            revoked=True,
            revocation_reason="generation mismatch during audit",
        )

    if not audit_passed:
        return replace(
            certificate,
            revoked=True,
            revocation_reason="exhaustive audit failed",
        )

    return replace(
        certificate,
        last_successful_audit_epoch=epoch,
        renewals=certificate.renewals + 1,
        revoked=False,
        revocation_reason=None,
    )


def recertify(
    *,
    generation_fingerprint: str,
    epoch: int,
) -> CertificateState:
    return issue_certificate(
        generation_fingerprint=generation_fingerprint,
        epoch=epoch,
    )


def stable_schedule(
    *,
    epochs: int,
    generation_fingerprint: str,
    adaptive_query_cost: int,
    exhaustive_query_cost: int,
    policy: LifecyclePolicy,
) -> tuple[LifecycleStep, ...]:
    if epochs <= 0:
        return ()

    certificate = issue_certificate(
        generation_fingerprint=generation_fingerprint,
        epoch=0,
    )
    steps = [
        LifecycleStep(
            epoch=0,
            event="issue",
            generation_fingerprint=generation_fingerprint,
            state=ACTIVE,
            mode=EXHAUSTIVE,
            query_cost=exhaustive_query_cost,
            certificate_renewals=certificate.renewals,
            reason="initial exhaustive certification",
        )
    ]

    for epoch in range(1, epochs):
        decision = decide(
            certificate,
            epoch=epoch,
            current_generation_fingerprint=generation_fingerprint,
            policy=policy,
        )
        if decision.state == AUDIT_DUE:
            certificate = record_audit(
                certificate,
                epoch=epoch,
                audit_passed=True,
                current_generation_fingerprint=generation_fingerprint,
            )
            steps.append(
                LifecycleStep(
                    epoch=epoch,
                    event="periodic-audit-pass",
                    generation_fingerprint=generation_fingerprint,
                    state=ACTIVE,
                    mode=EXHAUSTIVE,
                    query_cost=exhaustive_query_cost,
                    certificate_renewals=certificate.renewals,
                    reason="audit due; exhaustive verifier renewed certificate",
                )
            )
        else:
            steps.append(
                LifecycleStep(
                    epoch=epoch,
                    event="adaptive-use",
                    generation_fingerprint=generation_fingerprint,
                    state=decision.state,
                    mode=decision.required_mode,
                    query_cost=(
                        adaptive_query_cost
                        if decision.required_mode == ADAPTIVE
                        else exhaustive_query_cost
                    ),
                    certificate_renewals=certificate.renewals,
                    reason=decision.reason,
                )
            )
    return tuple(steps)


def drift_schedule(
    *,
    epochs: int,
    drift_epoch: int,
    original_generation: str,
    new_generation: str,
    adaptive_query_cost: int,
    exhaustive_query_cost: int,
    policy: LifecyclePolicy,
) -> tuple[LifecycleStep, ...]:
    if not 0 < drift_epoch < epochs:
        raise ValueError("drift_epoch must be inside the schedule")

    certificate = issue_certificate(
        generation_fingerprint=original_generation,
        epoch=0,
    )
    current_generation = original_generation
    steps = [
        LifecycleStep(
            epoch=0,
            event="issue",
            generation_fingerprint=current_generation,
            state=ACTIVE,
            mode=EXHAUSTIVE,
            query_cost=exhaustive_query_cost,
            certificate_renewals=certificate.renewals,
            reason="initial exhaustive certification",
        )
    ]

    for epoch in range(1, epochs):
        if epoch == drift_epoch:
            current_generation = new_generation

        decision = decide(
            certificate,
            epoch=epoch,
            current_generation_fingerprint=current_generation,
            policy=policy,
        )

        if decision.state == GENERATION_MISMATCH:
            certificate = recertify(
                generation_fingerprint=current_generation,
                epoch=epoch,
            )
            steps.append(
                LifecycleStep(
                    epoch=epoch,
                    event="generation-drift-recertify",
                    generation_fingerprint=current_generation,
                    state=ACTIVE,
                    mode=EXHAUSTIVE,
                    query_cost=exhaustive_query_cost,
                    certificate_renewals=certificate.renewals,
                    reason="generation mismatch forced exhaustive recertification",
                )
            )
        elif decision.state == AUDIT_DUE:
            certificate = record_audit(
                certificate,
                epoch=epoch,
                audit_passed=True,
                current_generation_fingerprint=current_generation,
            )
            steps.append(
                LifecycleStep(
                    epoch=epoch,
                    event="periodic-audit-pass",
                    generation_fingerprint=current_generation,
                    state=ACTIVE,
                    mode=EXHAUSTIVE,
                    query_cost=exhaustive_query_cost,
                    certificate_renewals=certificate.renewals,
                    reason="audit due; exhaustive verifier renewed certificate",
                )
            )
        else:
            steps.append(
                LifecycleStep(
                    epoch=epoch,
                    event="adaptive-use",
                    generation_fingerprint=current_generation,
                    state=decision.state,
                    mode=decision.required_mode,
                    query_cost=(
                        adaptive_query_cost
                        if decision.required_mode == ADAPTIVE
                        else exhaustive_query_cost
                    ),
                    certificate_renewals=certificate.renewals,
                    reason=decision.reason,
                )
            )
    return tuple(steps)


def query_summary(
    steps: tuple[LifecycleStep, ...],
    *,
    exhaustive_query_cost: int,
) -> dict:
    actual = sum(step.query_cost for step in steps)
    baseline = len(steps) * exhaustive_query_cost
    return {
        "epochs": len(steps),
        "actual_queries": actual,
        "always_exhaustive_queries": baseline,
        "query_savings_fraction": (
            1.0 - actual / baseline if baseline else 0.0
        ),
        "adaptive_epochs": sum(step.mode == ADAPTIVE for step in steps),
        "exhaustive_epochs": sum(step.mode == EXHAUSTIVE for step in steps),
    }


def lifecycle_report_payload(
    *,
    e015_report: dict,
    e016_report: dict,
    epochs: int = 12,
    drift_epoch: int = 5,
    policy: LifecyclePolicy = LifecyclePolicy(),
) -> dict:
    adaptive_cost = int(e015_report["aggregate"]["adaptive_queries"])
    exhaustive_cost = int(e015_report["aggregate"]["exhaustive_queries"])

    certified_generation = str(
        e016_report["same_generation"]["fingerprint"]
    )
    drift_generation = str(
        e016_report["changed_generation"]["fingerprint"]
    )

    stable = stable_schedule(
        epochs=epochs,
        generation_fingerprint=certified_generation,
        adaptive_query_cost=adaptive_cost,
        exhaustive_query_cost=exhaustive_cost,
        policy=policy,
    )
    drift = drift_schedule(
        epochs=epochs,
        drift_epoch=drift_epoch,
        original_generation=certified_generation,
        new_generation=drift_generation,
        adaptive_query_cost=adaptive_cost,
        exhaustive_query_cost=exhaustive_cost,
        policy=policy,
    )

    failed_audit_certificate = issue_certificate(
        generation_fingerprint=certified_generation,
        epoch=0,
    )
    failed_audit_certificate = record_audit(
        failed_audit_certificate,
        epoch=policy.audit_interval_epochs,
        audit_passed=False,
        current_generation_fingerprint=certified_generation,
    )
    failed_audit_decision = decide(
        failed_audit_certificate,
        epoch=policy.audit_interval_epochs + 1,
        current_generation_fingerprint=certified_generation,
        policy=policy,
    )

    skipped_audit_certificate = issue_certificate(
        generation_fingerprint=certified_generation,
        epoch=0,
    )
    expiry_decision = decide(
        skipped_audit_certificate,
        epoch=policy.expiry_epochs,
        current_generation_fingerprint=certified_generation,
        policy=policy,
    )

    stable_summary = query_summary(
        stable,
        exhaustive_query_cost=exhaustive_cost,
    )
    drift_summary = query_summary(
        drift,
        exhaustive_query_cost=exhaustive_cost,
    )

    gates = {
        "stable_schedule_saves_at_least_50_percent": (
            stable_summary["query_savings_fraction"] >= 0.50
        ),
        "stable_schedule_uses_exhaustive_on_audit_epochs": all(
            step.mode == EXHAUSTIVE
            for step in stable
            if step.event in {"issue", "periodic-audit-pass"}
        ),
        "generation_drift_forces_exhaustive": any(
            step.epoch == drift_epoch
            and step.event == "generation-drift-recertify"
            and step.mode == EXHAUSTIVE
            for step in drift
        ),
        "failed_audit_revokes": (
            failed_audit_decision.state == REVOKED
            and failed_audit_decision.required_mode == EXHAUSTIVE
        ),
        "skipped_audit_hard_expires": (
            expiry_decision.state == EXPIRED
            and expiry_decision.required_mode == EXHAUSTIVE
        ),
        "e016_guard_contract_was_valid": bool(
            e016_report["guard_contract_passed"]
        ),
    }

    return {
        "experiment": "E017",
        "source_experiments": ["E015", "E016"],
        "policy": asdict(policy),
        "stable_schedule": [asdict(step) for step in stable],
        "stable_summary": stable_summary,
        "drift_epoch": drift_epoch,
        "drift_schedule": [asdict(step) for step in drift],
        "drift_summary": drift_summary,
        "failed_audit_decision": asdict(failed_audit_decision),
        "expiry_decision": asdict(expiry_decision),
        "promotion_gate": gates,
        "lifecycle_contract_passed": all(gates.values()),
    }
