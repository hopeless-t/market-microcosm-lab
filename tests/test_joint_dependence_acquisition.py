from market_microcosm.joint_dependence_acquisition import (
    joint_dependence_report_payload,
    joint_optimal_policy,
    marginal_bad_probability,
)
from market_microcosm.sequential_evidence_acquisition import BAD_PROBABILITY


def test_joint_world_preserves_e069_marginals():
    assert marginal_bad_probability() == BAD_PROBABILITY


def test_joint_dependence_reorders_safe_path():
    x = joint_optimal_policy()
    assert x["safe_path"] == [
        "gtm-pack",
        "finance-pack",
        "signed-strategy-gap-attestation",
    ]
    assert round(x["expected_cost"], 2) == 8.45


def test_e072_promotion_contract():
    x = joint_dependence_report_payload()
    assert round(x["regret"], 2) == 0.75
    assert all(x["promotion_gate"].values())
    assert x["promoted_joint_rule"] == (
        "sequential-acquisition-requires-joint-failure-model-not-marginals-only-v1"
    )
