from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProjectionMaturity(str, Enum):
    OPERATIONAL_TRANSFER = "OPERATIONAL_TRANSFER"
    REINFORCEMENT = "REINFORCEMENT"
    CONVERGENT_OTHER_SOURCE = "CONVERGENT_OTHER_SOURCE"
    PERSISTENT_DOC_ONLY_UNKNOWN = "PERSISTENT_DOC_ONLY_UNKNOWN"
    DORMANT_OR_LOST_UNKNOWN = "DORMANT_OR_LOST_UNKNOWN"


@dataclass(frozen=True)
class ProjectionEvidence:
    projection_persists: bool
    downstream_operational_artifact: bool = False
    downstream_source_matches_projection: bool = False
    prior_operational_mechanism: bool = False
    later_other_source_explicit: bool = False


def classify_projection(evidence: ProjectionEvidence) -> ProjectionMaturity:
    if evidence.prior_operational_mechanism:
        return ProjectionMaturity.REINFORCEMENT
    if evidence.downstream_operational_artifact and evidence.downstream_source_matches_projection:
        return ProjectionMaturity.OPERATIONAL_TRANSFER
    if evidence.later_other_source_explicit:
        return ProjectionMaturity.CONVERGENT_OTHER_SOURCE
    if evidence.projection_persists:
        return ProjectionMaturity.PERSISTENT_DOC_ONLY_UNKNOWN
    return ProjectionMaturity.DORMANT_OR_LOST_UNKNOWN


def summarize_maturity(items: dict[str, ProjectionEvidence]) -> dict[str, int]:
    counts = {state.value: 0 for state in ProjectionMaturity}
    for evidence in items.values():
        counts[classify_projection(evidence).value] += 1
    return counts
