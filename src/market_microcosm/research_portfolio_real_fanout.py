from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ObservedCommit:
    repository: str
    sha: str
    message: str
    created_at: str


# Snapshot from GitHub commit search for `Strata` under hopeless-t, restricted here
# to the dense 2026-10-05 23:10:37..23:16:57 JST event cluster.
STRATA_FANOUT = (
    ObservedCommit("finite-ram-lab", "2b8f87061051b991e0926d9b9c2a80538e18b26f", "research: intake Strata v0.1.39 runtime allocation ideas", "2026-10-05T23:10:37+09:00"),
    ObservedCommit("mvca", "a60bd6f39cb4447e38e1e4675546bfb1c7dba3fe", "research: map Strata runtime allocation ideas into MVCA", "2026-10-05T23:11:00+09:00"),
    ObservedCommit("mvca-runtime", "2378c8eb23b5ffd94968223c2f9bbbfeada82d2a", "research: add Strata-inspired runtime scheduling candidates", "2026-10-05T23:11:17+09:00"),
    ObservedCommit("mvca-hq", "4139e8b2bf4008fcd1c36fa98ebfc8973630e08a", "research: add Strata topology and admission ideas to MVCA-HQ", "2026-10-05T23:11:31+09:00"),
    ObservedCommit("next-generation-github", "ffa4df0f3d65ec960e7013d7f730204b0131e411", "research: import Strata hot-set ideas into next-generation GitHub", "2026-10-05T23:11:50+09:00"),
    ObservedCommit("finite-tool-surface-lab", "f7a111bbf31663959e893bff02306382b56a9601", "research: map Strata hot-set scheduling to finite tool surfaces", "2026-10-05T23:12:03+09:00"),
    ObservedCommit("memory-attention-lab", "d0e09390a8defdac8f15aaeda48d66113a417f1f", "research: add Strata working-set ideas to memory-attention lab", "2026-10-05T23:12:15+09:00"),
    ObservedCommit("harness-component-economics", "09d1c86003dc66b9be97aa80801297dffc7bfcb6", "research: add Strata component-economics case study", "2026-10-05T23:12:31+09:00"),
    ObservedCommit("market-microcosm-lab", "cf6130543366d9f56389b648120f622567e551be", "research: model Strata as a resource-allocation microcosm", "2026-10-05T23:12:47+09:00"),
    ObservedCommit("catfood-pcg-lab", "ccef78a6d7764723539683c21f59622d47804277", "research: apply Strata tiering ideas to PCG asset streaming", "2026-10-05T23:13:04+09:00"),
    ObservedCommit("catfood-jev-cua-lab", "6ccd66792319eb728c5dfaf8784eecc0cfa7e644", "research: apply Strata working-set scheduling to Jev/CUA", "2026-10-05T23:13:20+09:00"),
    ObservedCommit("catfood-expressive-engine", "1882fcdb0672a004140fc8a6b88cdf91988c41d4", "research: add Strata-inspired expressive resource scheduling", "2026-10-05T23:13:33+09:00"),
    ObservedCommit("catfood-semantic-forge", "6b453bc5980361112d4650a32e01cf057fe743fe", "research: derive canonical IR lessons from Strata v0.1.39", "2026-10-05T23:13:50+09:00"),
    ObservedCommit("chatgpt-recovery-dynamics", "b4f5846aa47d020f5d544ad2a1e77efb9f3fb6ae", "research: map Strata tiering into recovery dynamics", "2026-10-05T23:14:08+09:00"),
    ObservedCommit("chatgpt-refresh-poc", "ddd132b4f1308fb7a82e627cac0413c8b18a56e1", "research: add tiered refresh-state ideas from Strata", "2026-10-05T23:14:21+09:00"),
    ObservedCommit("catnood-agent-control", "88b537a2b9a51da2d6a97bdf713eb4fd233192a4", "research: add Strata-inspired agent admission and placement", "2026-10-05T23:14:33+09:00"),
    ObservedCommit("NazeYatta", "4d88b2958339b889035b60f3a0cc29911cd80c49", "research: add bounded resource-preflight ideas from Strata", "2026-10-05T23:14:47+09:00"),
    ObservedCommit("evidence-manifest-generator", "83db8f674a851713b6b2eddf8ef076ff051e4155", "research: capture Strata reproducibility metadata ideas", "2026-10-05T23:15:01+09:00"),
    ObservedCommit("field-report-app", "a8bdce83ca738a1442540025896b5a51683f7236", "research: apply Strata working-set discipline to field report app", "2026-10-05T23:15:17+09:00"),
    ObservedCommit("catnood-web", "43d14b3e9dbc75bc11f8fb0a9638f2ab5d46ef93", "research: add Strata-inspired web working-set notes", "2026-10-05T23:15:30+09:00"),
    ObservedCommit("dissociated-control-systems", "ce4163e31b180e6c8fe33d0f1ec7e337316c72e0", "research: add bounded Strata control-systems analogy to DCS", "2026-10-05T23:15:45+09:00"),
    ObservedCommit("recursive-flourishing-lab", "8a68ffaa7c7067f12b6a08da6eea75b071db52e6", "research: add bounded working-set portfolio ideas from Strata", "2026-10-05T23:16:03+09:00"),
    ObservedCommit("topological-spin-lab", "6fe3b8e1c74e78e329a1b0fa229834122f22af91", "research: capture Strata regime and measurement methodology", "2026-10-05T23:16:17+09:00"),
    ObservedCommit("DDS_Vault", "0905a34a82b0dbed114a51bcf51a5d28e04eb3f0", "research: index Strata v0.1.39 cross-repo routing", "2026-10-05T23:16:57+09:00"),
)


def rpe011_report_payload() -> dict:
    ordered = sorted(STRATA_FANOUT, key=lambda row: row.created_at)
    timestamps = [datetime.fromisoformat(row.created_at) for row in ordered]
    gaps = [
        (right - left).total_seconds()
        for left, right in zip(timestamps, timestamps[1:])
    ]
    span_seconds = (timestamps[-1] - timestamps[0]).total_seconds()
    repositories = {row.repository for row in ordered}

    observed = {
        "commit_count": len(ordered),
        "distinct_repository_count": len(repositories),
        "first_commit_at": ordered[0].created_at,
        "last_commit_at": ordered[-1].created_at,
        "window_seconds": span_seconds,
        "window_minutes": span_seconds / 60.0,
        "commits_per_window_minute": len(ordered) / (span_seconds / 60.0),
        "mean_intercommit_gap_seconds": sum(gaps) / len(gaps),
        "max_intercommit_gap_seconds": max(gaps),
        "all_messages_explicitly_reference_strata": all(
            "strata" in row.message.lower() for row in ordered
        ),
        "one_commit_per_repository_in_snapshot": len(repositories) == len(ordered),
    }

    counterfactual = {
        "observed_materializations": len(ordered),
        "candidate_canonical_source_events": 1,
        "minimum_projection_count_if_no_downstream_need_is_known": 0,
        "maximum_projection_count_if_every_observed_projection_was_needed": len(ordered),
        "decision_relevant_projection_count": None,
        "counterfactual_materialization_savings": None,
        "reason_unknown": (
            "Commit metadata establishes a dense cross-repository Strata fan-out cluster, "
            "but does not establish which downstream projections changed a later decision."
        ),
    }

    gates = {
        "dense_fanout_cluster_observed": observed["commit_count"] >= 20,
        "cross_repository_fanout_observed": observed["distinct_repository_count"] >= 20,
        "cluster_is_time_concentrated": observed["window_seconds"] <= 600,
        "messages_share_explicit_source_term": observed["all_messages_explicitly_reference_strata"],
        "snapshot_has_one_projection_commit_per_repo": observed["one_commit_per_repository_in_snapshot"],
        "counterfactual_savings_left_unknown": counterfactual["counterfactual_materialization_savings"] is None,
        "decision_relevance_left_unknown": counterfactual["decision_relevant_projection_count"] is None,
    }

    return {
        "experiment": "RPE-011",
        "title": "Observed Strata cross-repository fan-out replay",
        "source": {
            "retrieval": "GitHub commit search",
            "query": "Strata",
            "owner": "hopeless-t",
            "snapshot_rows": [row.__dict__ for row in ordered],
        },
        "observed": observed,
        "counterfactual_envelope": counterfactual,
        "promotion_gate": gates,
        "theory_update": (
            "RPE-001 fan-out is no longer only a synthetic possibility: one observed Strata event cluster "
            "contains 24 explicit source-referencing commits across 24 repositories in 380 seconds. "
            "However, commit metadata alone cannot identify which projections were decision-relevant, "
            "so retrospective savings remain unclaimed."
        ),
        "claim_ceiling": "OBSERVED_GITHUB_COMMIT_METADATA_CLUSTER_ONLY_NO_CAUSAL_OR_COUNTERFACTUAL_SAVINGS_CLAIM",
    }
