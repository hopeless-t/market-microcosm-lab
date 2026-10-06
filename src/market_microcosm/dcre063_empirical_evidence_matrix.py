from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceClass(str, Enum):
    PRIMARY_SOURCE_REPORTED = "PRIMARY_SOURCE_REPORTED"
    THIRD_PARTY_ASSURED_PRIMARY = "THIRD_PARTY_ASSURED_PRIMARY"
    INDEPENDENT_OFFICIAL_CROSSCHECK = "INDEPENDENT_OFFICIAL_CROSSCHECK"
    SECONDARY_DERIVED_CANDIDATE = "SECONDARY_DERIVED_CANDIDATE"


@dataclass(frozen=True)
class EmpiricalEvidenceRow:
    claim: str
    evidence_class: EvidenceClass
    promoted: bool
    causal: bool
    blocker: str | None = None


def dcre_empirical_evidence_rows() -> tuple[EmpiricalEvidenceRow, ...]:
    return (
        EmpiricalEvidenceRow(
            claim="Google data-center electricity more than doubled 2020-2024",
            evidence_class=EvidenceClass.PRIMARY_SOURCE_REPORTED,
            promoted=True,
            causal=False,
            blocker="does not identify rebound cause or eta",
        ),
        EmpiricalEvidenceRow(
            claim="FY2024 Google data-center electricity and water totals are assured",
            evidence_class=EvidenceClass.THIRD_PARTY_ASSURED_PRIMARY,
            promoted=True,
            causal=False,
            blocker="metric population identity is not certified",
        ),
        EmpiricalEvidenceRow(
            claim="NWCPUD 2024 residential price is 7.72 cents/kWh and below Oregon average",
            evidence_class=EvidenceClass.INDEPENDENT_OFFICIAL_CROSSCHECK,
            promoted=True,
            causal=False,
            blocker="no counterfactual identifies governance effect",
        ),
        EmpiricalEvidenceRow(
            claim="NWCPUD 2024 total sales are 1,530,602 MWh and industrial share exceeds 82%",
            evidence_class=EvidenceClass.INDEPENDENT_OFFICIAL_CROSSCHECK,
            promoted=True,
            causal=False,
            blocker="industrial sector is not identical to data-center load",
        ),
        EmpiricalEvidenceRow(
            claim="NWCPUD load grew from 90 MW in 2016 to 277 MW in 2026 with data centers reported as a substantial driver",
            evidence_class=EvidenceClass.PRIMARY_SOURCE_REPORTED,
            promoted=True,
            causal=False,
            blocker="exact data-center contribution is not observed",
        ),
        EmpiricalEvidenceRow(
            claim="NWCPUD large-load governance mechanisms exist",
            evidence_class=EvidenceClass.PRIMARY_SOURCE_REPORTED,
            promoted=True,
            causal=False,
            blocker="mechanism effectiveness is not identified",
        ),
        EmpiricalEvidenceRow(
            claim="NWCPUD 2024 SAIDI/SAIFI candidate values are 34.8 minutes / 0.22 interruptions",
            evidence_class=EvidenceClass.SECONDARY_DERIVED_CANDIDATE,
            promoted=False,
            causal=False,
            blocker="direct NWCPUD row from official EIA-861 Reliability schedule not inspected in current evidence path",
        ),
    )


def dcre063_empirical_evidence_matrix_report() -> dict:
    rows = dcre_empirical_evidence_rows()
    promoted = tuple(row for row in rows if row.promoted)
    candidates = tuple(row for row in rows if not row.promoted)
    return {
        "experiment": "DCRE-063",
        "rows": rows,
        "promoted_rows": promoted,
        "candidate_rows": candidates,
        "causally_identified_rows": tuple(row for row in rows if row.causal),
        "promoted_count": len(promoted),
        "candidate_count": len(candidates),
        "causal_count": sum(int(row.causal) for row in rows),
        "reliability_candidate_promoted": False,
        "next_high_value_gap": "DIRECT_OFFICIAL_UTILITY_RELIABILITY_ROW_OR_CREDIBLE_COUNTERFACTUAL",
        "authority_effect": "NONE",
    }
