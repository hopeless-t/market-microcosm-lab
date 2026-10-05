from market_microcosm.calibration_frontier import (
    calibration_frontier_report_payload,
    compile_calibration_for_target,
    pareto_frontier,
)


def test_exact_calibration_frontier():
    x = pareto_frontier()
    assert [
        (
            row["calibration_cost"],
            round(row["policy"]["worst_case_expected_cost"], 2),
        )
        for row in x
    ] == [(0, 12.0), (1, 11.85), (2, 11.2)]


def test_target_compiler():
    assert compile_calibration_for_target(11.9)["selected"][
        "calibration_ids"
    ] == ["strategy-incidence-study"]
    assert compile_calibration_for_target(11.3)["selected"][
        "calibration_ids"
    ] == ["gtm-incidence-study"]
    assert compile_calibration_for_target(11.1)["status"] == "UNSAT"


def test_e077_promotion_contract():
    x = calibration_frontier_report_payload()
    assert all(x["promotion_gate"].values())
    assert x["promoted_frontier_rule"] == (
        "certificate-calibration-uses-pareto-frontier-and-fail-closed-target-compiler-v1"
    )
