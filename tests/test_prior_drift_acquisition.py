from market_microcosm.prior_drift_acquisition import (
    optimal_policy_for_prior,
    prior_drift_report_payload,
    PRIORS,
)


def test_finance_shift_reorders_policy():
    x = optimal_policy_for_prior(PRIORS["finance-shift"])
    assert x["initial_action"] == "finance-pack"
    assert round(x["expected_cost"], 7) == 8.8731875


def test_strategy_shift_reorders_policy():
    x = optimal_policy_for_prior(PRIORS["strategy-shift"])
    assert x["initial_action"] == "signed-strategy-gap-attestation"
    assert round(x["expected_cost"], 5) == 9.25625


def test_e070_promotion_contract():
    x = prior_drift_report_payload()
    assert x["e069_policy_authority_under_shift"] == "REVOKED"
    assert x["scenarios"]["finance-shift"]["regret"] > 3.7
    assert x["scenarios"]["strategy-shift"]["regret"] > 1.5
    assert all(x["promotion_gate"].values())
