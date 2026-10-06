from market_microcosm.rpe014_projection_maturity import (
    ProjectionEvidence,
    ProjectionMaturity,
    classify_projection,
    summarize_maturity,
)


def sample() -> dict[str, ProjectionEvidence]:
    return {
        "catfood-semantic-forge": ProjectionEvidence(projection_persists=True),
        "market-microcosm-lab": ProjectionEvidence(projection_persists=True),
        "field-report-app": ProjectionEvidence(projection_persists=True),
        "recursive-flourishing-lab": ProjectionEvidence(
            projection_persists=True,
            prior_operational_mechanism=True,
        ),
        "next-generation-github": ProjectionEvidence(
            projection_persists=True,
            later_other_source_explicit=True,
        ),
    }


def test_representative_strata_sample_preserves_unknowns() -> None:
    counts = summarize_maturity(sample())
    assert counts[ProjectionMaturity.PERSISTENT_DOC_ONLY_UNKNOWN.value] == 3
    assert counts[ProjectionMaturity.REINFORCEMENT.value] == 1
    assert counts[ProjectionMaturity.CONVERGENT_OTHER_SOURCE.value] == 1
    assert counts[ProjectionMaturity.OPERATIONAL_TRANSFER.value] == 0


def test_persistence_alone_does_not_imply_adoption() -> None:
    state = classify_projection(ProjectionEvidence(projection_persists=True))
    assert state is ProjectionMaturity.PERSISTENT_DOC_ONLY_UNKNOWN


def test_operational_transfer_requires_matching_provenance() -> None:
    state = classify_projection(
        ProjectionEvidence(
            projection_persists=True,
            downstream_operational_artifact=True,
            downstream_source_matches_projection=True,
        )
    )
    assert state is ProjectionMaturity.OPERATIONAL_TRANSFER
