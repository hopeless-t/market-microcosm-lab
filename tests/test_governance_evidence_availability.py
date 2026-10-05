from datetime import date

from market_microcosm.governance_evidence_availability import (
    allied_exit_criteria_evidence,
    governance_evidence_availability_report_payload,
    public_evidence_authority,
)


def test_effective_period_and_public_availability_are_distinct() -> None:
    evidence = allied_exit_criteria_evidence()
    assert evidence.effective_period == "2024-Q1"
    assert evidence.effective_period_end == date(2024, 3, 31)
    assert evidence.publicly_available_on == date(2024, 8, 14)


def test_public_evaluator_rejects_retrospective_leakage() -> None:
    assert public_evidence_authority(date(2024, 5, 15))["decision"] == (
        "REJECT_FUTURE_INFORMATION"
    )
    assert public_evidence_authority(date(2024, 8, 14))["decision"] == "ADMIT"


def test_e088_promotion_contract() -> None:
    payload = governance_evidence_availability_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_availability_rule"] == (
        "public-prospective-evidence-uses-availability-time-not-retrospective-effective-period-v1"
    )
