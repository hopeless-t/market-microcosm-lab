from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CIAmplificationObservation:
    branch_commits: int
    pr_workflow_runs: int
    files_changed: int

    @property
    def runs_per_commit(self) -> float:
        if self.branch_commits <= 0:
            raise ValueError("branch_commits must be positive")
        return self.pr_workflow_runs / self.branch_commits

    @property
    def commit_to_file_ratio(self) -> float:
        if self.files_changed <= 0:
            raise ValueError("files_changed must be positive")
        return self.branch_commits / self.files_changed


@dataclass(frozen=True)
class BatchedMaterializationPlan:
    pending_files: int
    expected_branch_updates: int = 1
    expected_pr_ci_runs: int = 1

    def __post_init__(self) -> None:
        if self.pending_files < 1:
            raise ValueError("pending_files must be positive")
        if self.expected_branch_updates != 1:
            raise ValueError("RPE-013 contract batches into exactly one branch update")
        if self.expected_pr_ci_runs != 1:
            raise ValueError("RPE-013 contract expects one PR CI run per batch")


def compare_materialization(n_files: int) -> dict[str, int | float]:
    if n_files < 1:
        raise ValueError("n_files must be positive")
    sequential_updates = n_files
    batched_updates = 1
    avoided_updates = sequential_updates - batched_updates
    return {
        "pending_files": n_files,
        "sequential_branch_updates": sequential_updates,
        "batched_branch_updates": batched_updates,
        "avoided_branch_updates": avoided_updates,
        "branch_update_reduction_fraction": avoided_updates / sequential_updates,
    }
