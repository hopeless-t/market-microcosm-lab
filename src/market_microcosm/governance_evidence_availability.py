from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date


@dataclass(frozen=True)
class PeriodEvidence:
    evidence_id: str
    effective_period: str
    effective_period_start: date
    effective_period_end: date
    publicly_available_on: date
    description: str


def allied_exit_criteria_evidence() -> PeriodEvidence:
    return PeriodEvidence(
        evidence_id="allied-overseas-exit-criteria",
        effective_period="2024-Q1",
        effective_period_start=date(2024, 1, 1),
        effective_period_end=date(2024, 3, 31),
        publicly_available_on=date(2024, 8, 14),
        description=(
            "FY2024 H1 material states stricter withdrawal criteria had been "
            "set for the overseas subsidiary in Q1 and budget-vs-actual "
            "management was enforced against those criteria."
        ),
    )


def public_evidence_authority(as_of: date) -> dict:
    evidence = allied_exit_criteria_evidence()
    available = as_of >= evidence.publicly_available_on
    return {
        "as_of": as_of.isoformat(),
        "evidence_id": evidence.evidence_id,
        "effective_period": evidence.effective_period,
        "publicly_available_on": evidence.publicly_available_on.isoformat(),
        "available_to_public_evaluator": available,
        "decision": "ADMIT" if available else "REJECT_FUTURE_INFORMATION",
    }


def governance_evidence_availability_report_payload() -> dict:
    evidence = allied_exit_criteria_evidence()
    may_cutoff = public_evidence_authority(date(2024, 5, 15))
    disclosure_day = public_evidence_authority(date(2024, 8, 14))

    gates = {
        "effective_period_precedes_public_disclosure": (
            evidence.effective_period_end < evidence.publicly_available_on
        ),
        "may_public_evaluator_cannot_use_q1_internal_checkpoint": (
            may_cutoff["decision"] == "REJECT_FUTURE_INFORMATION"
        ),
        "evidence_becomes_publicly_admissible_on_august_fourteenth": (
            disclosure_day["decision"] == "ADMIT"
        ),
        "effective_period_is_not_collapsed_into_public_availability": True,
        "unknown_exact_internal_effective_date_is_not_invented": True,
    }

    return {
        "experiment": "E088",
        "question": (
            "When a later public filing says a governance checkpoint was "
            "already effective in an earlier quarter, which timestamp controls "
            "a public prospective evaluator?"
        ),
        "evidence": {
            **asdict(evidence),
            "effective_period_start": evidence.effective_period_start.isoformat(),
            "effective_period_end": evidence.effective_period_end.isoformat(),
            "publicly_available_on": evidence.publicly_available_on.isoformat(),
        },
        "public_authority_checks": {
            "2024-05-15": may_cutoff,
            "2024-08-14": disclosure_day,
        },
        "promotion_gate": gates,
        "promoted_availability_rule": (
            "public-prospective-evidence-uses-availability-time-not-retrospective-effective-period-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Governance evidence now carries both effective-period semantics "
            "and public-availability time. Public prospective evaluation uses "
            "availability time; retrospective filings cannot leak earlier "
            "internal checkpoints backward into the public feature set."
        ),
        "limitations": (
            "The filing identifies the checkpoint as occurring in Q1 but does "
            "not disclose an exact internal effective date. E088 therefore "
            "stores a period, not an invented point timestamp."
        ),
    }
