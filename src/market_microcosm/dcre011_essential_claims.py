from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UrgencyClaim:
    actor_id: str
    arrival_order: int
    true_essential: bool
    claimed_essential: bool
    evidence_score: float
    system_wait_value: float

    def __post_init__(self) -> None:
        if self.arrival_order < 0:
            raise ValueError("arrival_order must be non-negative")
        if not 0.0 <= self.evidence_score <= 1.0:
            raise ValueError("evidence_score must be within [0, 1]")
        if self.system_wait_value < 0.0:
            raise ValueError("system_wait_value must be non-negative")


def frozen_claims() -> tuple[UrgencyClaim, ...]:
    return (
        UrgencyClaim("PREMIUM", 0, False, True, 0.20, 0.08),
        UrgencyClaim("ESSENTIAL", 1, True, True, 0.90, 0.50),
        UrgencyClaim("ROUTINE", 2, False, False, 0.80, 0.06),
    )


def trust_claim_allocate(claims: tuple[UrgencyClaim, ...]) -> UrgencyClaim:
    claimed = [claim for claim in claims if claim.claimed_essential]
    if not claimed:
        raise ValueError("no claimed-essential actor")
    return min(claimed, key=lambda claim: (claim.arrival_order, claim.actor_id))


def evidence_gate_allocate(
    claims: tuple[UrgencyClaim, ...], *, threshold: float = 0.80
) -> UrgencyClaim:
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be within [0, 1]")
    qualified = [
        claim
        for claim in claims
        if claim.claimed_essential and claim.evidence_score >= threshold
    ]
    if not qualified:
        raise ValueError("no evidence-qualified essential claim")
    return max(
        qualified,
        key=lambda claim: (claim.system_wait_value, -claim.arrival_order, claim.actor_id),
    )


def truth_oracle_allocate(claims: tuple[UrgencyClaim, ...]) -> UrgencyClaim:
    true = [claim for claim in claims if claim.true_essential]
    if not true:
        raise ValueError("no true essential actor")
    return max(true, key=lambda claim: (claim.system_wait_value, claim.actor_id))
