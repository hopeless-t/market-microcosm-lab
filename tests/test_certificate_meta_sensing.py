from market_microcosm.certificate_meta_sensing import (
    certificate_meta_sensing_report_payload,
    exact_certificate_calibration_portfolio,
)


def test_minimum_targeted_calibration():
    x = exact_certificate_calibration_portfolio()
    s = x["selected"]
    assert s["calibration_ids"] == ["gtm-incidence-study"]
    assert s["calibration_cost"] == 2
    assert round(
        s["policy"]["worst_case_expected_cost"], 3
    ) == 11.2
    assert s["meets_target"] is True


def test_e076_promotion_contract():
    x = certificate_meta_sensing_report_payload()
    assert all(x["promotion_gate"].values())
    assert x["promoted_meta_sensing_rule"] == (
        "acquire-minimum-calibration-evidence-to-meet-certificate-target-v1"
    )
