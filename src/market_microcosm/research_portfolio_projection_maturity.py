from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectionSample:
    repository: str
    source_commit: str
    source_path: str
    insertion_kind: str
    persists_on_main: bool
    maturity: str
    evidence_note: str
    later_evidence_ref: str | None = None


SAMPLE = (
    ProjectionSample(
        repository="catfood-semantic-forge",
        source_commit="6b453bc5980361112d4650a32e01cf057fe743fe",
        source_path="docs/research/STRATA_V0_1_39_CANONICAL_IR_2026-10-05.md",
        insertion_kind="DOCS_ONLY_NEW_FILE",
        persists_on_main=True,
        maturity="PERSISTENT_DOC_ONLY_UNKNOWN",
        evidence_note="The Strata projection commit adds one research note. No source-specific downstream executable adoption is established by the sampled evidence.",
    ),
    ProjectionSample(
        repository="market-microcosm-lab",
        source_commit="cf6130543366d9f56389b648120f622567e551be",
        source_path="docs/research/STRATA_V0_1_39_RESOURCE_MARKET_2026-10-05.md",
        insertion_kind="DOCS_ONLY_NEW_FILE",
        persists_on_main=True,
        maturity="PERSISTENT_DOC_ONLY_UNKNOWN",
        evidence_note="The projection remains a research note on main. Later RPE work overlaps resource/residency themes but has multiple explicit inputs, so Strata-specific causal credit is not assigned.",
    ),
    ProjectionSample(
        repository="next-generation-github",
        source_commit="ffa4df0f3d65ec960e7013d7f730204b0131e411",
        source_path="docs/research/STRATA_V0_1_39_CROSS_POLLINATION_2026-10-05.md",
        insertion_kind="DOCS_ONLY_NEW_FILE",
        persists_on_main=True,
        maturity="CONVERGENT_OTHER_SOURCE",
        evidence_note="A later demand-paged HOT/WARM/COLD/OFF research PR overlaps the residency abstraction but explicitly cites DeepSeek Harness as its trigger and was closed unmerged.",
        later_evidence_ref="hopeless-t/next-generation-github#42",
    ),
    ProjectionSample(
        repository="recursive-flourishing-lab",
        source_commit="8a68ffaa7c7067f12b6a08da6eea75b071db52e6",
        source_path="docs/research/STRATA_V0_1_39_PORTFOLIO_SCHEDULING_2026-10-05.md",
        insertion_kind="DOCS_ONLY_NEW_FILE",
        persists_on_main=True,
        maturity="REINFORCEMENT_OF_PREEXISTING_MECHANISM",
        evidence_note="The executable finite semantic working-set mechanism predates the Strata projection, so the projection cannot be treated as the origin of that mechanism.",
        later_evidence_ref="b05504c7bcece75ced5d0fa563e74f212e87371d",
    ),
    ProjectionSample(
        repository="field-report-app",
        source_commit="a8bdce83ca738a1442540025896b5a51683f7236",
        source_path="docs/research/STRATA_V0_1_39_MOBILE_RESOURCE_TIERING_2026-10-05.md",
        insertion_kind="DOCS_ONLY_NEW_FILE",
        persists_on_main=True,
        maturity="PERSISTENT_DOC_ONLY_UNKNOWN",
        evidence_note="The sampled source commit adds one design/research note. No source-specific downstream implementation is established by this sample.",
    ),
)


def rpe012_report_payload() -> dict:
    maturity_counts: dict[str, int] = {}
    for row in SAMPLE:
        maturity_counts[row.maturity] = maturity_counts.get(row.maturity, 0) + 1

    operational_credit_confirmed = sum(
        row.maturity == "UNIQUE_SOURCE_OPERATIONAL_TRANSFER_CONFIRMED" for row in SAMPLE
    )
    unknown_count = sum("UNKNOWN" in row.maturity for row in SAMPLE)

    gates = {
        "sample_contains_five_repositories": len(SAMPLE) == 5,
        "all_insertion_commits_are_docs_only_new_files": all(
            row.insertion_kind == "DOCS_ONLY_NEW_FILE" for row in SAMPLE
        ),
        "all_sampled_projection_notes_persist_on_main": all(row.persists_on_main for row in SAMPLE),
        "preexisting_mechanism_case_preserved": maturity_counts.get("REINFORCEMENT_OF_PREEXISTING_MECHANISM", 0) >= 1,
        "other_source_convergence_case_preserved": maturity_counts.get("CONVERGENT_OTHER_SOURCE", 0) >= 1,
        "unknown_cases_not_force_classified": unknown_count >= 1,
        "no_unique_operational_credit_invented": operational_credit_confirmed == 0,
    }

    return {
        "experiment": "RPE-012",
        "title": "Observed projection maturity sample",
        "sample": [row.__dict__ for row in SAMPLE],
        "summary": {
            "sample_size": len(SAMPLE),
            "docs_only_at_insertion_count": sum(row.insertion_kind == "DOCS_ONLY_NEW_FILE" for row in SAMPLE),
            "persist_on_main_count": sum(row.persists_on_main for row in SAMPLE),
            "maturity_counts": maturity_counts,
            "unique_source_operational_transfer_confirmed_count": operational_credit_confirmed,
            "persistent_docs_only_unknown_count": unknown_count,
        },
        "promotion_gate": gates,
        "theory_update": (
            "Physical projection count is not a value metric. In the five-repository Strata sample, all source commits are documentation-only and persistent, "
            "while one sampled concept clearly predates Strata and another later converges from a different explicit source. Source contribution therefore needs provenance-aware maturity classification rather than binary used/unused labeling."
        ),
        "candidate_rule": "TRACK_PROJECTION_MATURITY_AND_SOURCE_CONTRIBUTION_SEPARATELY_FROM_ARTIFACT_EXISTENCE",
        "claim_ceiling": "FIVE_REPOSITORY_OBSERVED_METADATA_AND_FILE_SAMPLE_ONLY_NO_POPULATION_USAGE_RATE_OR_CAUSAL_CREDIT_CLAIM",
    }
