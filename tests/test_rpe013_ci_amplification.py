import pytest

from market_microcosm.rpe013_ci_amplification import (
    BatchedMaterializationPlan,
    CIAmplificationObservation,
    compare_materialization,
)


def test_observed_rpe_branch_amplification_snapshot() -> None:
    observation = CIAmplificationObservation(
        branch_commits=47,
        pr_workflow_runs=44,
        files_changed=47,
    )
    assert observation.runs_per_commit == pytest.approx(44 / 47)
    assert observation.commit_to_file_ratio == 1.0


def test_batching_four_files_uses_one_branch_update() -> None:
    plan = BatchedMaterializationPlan(pending_files=4)
    report = compare_materialization(plan.pending_files)
    assert report["sequential_branch_updates"] == 4
    assert report["batched_branch_updates"] == 1
    assert report["avoided_branch_updates"] == 3
    assert report["branch_update_reduction_fraction"] == pytest.approx(0.75)


def test_batch_contract_is_fail_closed() -> None:
    with pytest.raises(ValueError):
        BatchedMaterializationPlan(pending_files=3, expected_branch_updates=2)
