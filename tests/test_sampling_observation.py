from market_microcosm.sampling_observation import (
    POPULATION_APPLICATIONS,
    SAMPLED_INSTITUTIONS_APPROX,
    minimum_carriers_for_detection,
    sampling_observation_report_payload,
    simple_random_detection_probability,
    unconstrained_selection_worst_case_detection,
)


def test_srs_detection_thresholds_are_exactly_located() -> None:
    p95 = minimum_carriers_for_detection(0.95)
    p99 = minimum_carriers_for_detection(0.99)

    assert p95["minimum_carrier_count"] == 87
    assert 0.95 <= p95["achieved_detection_probability"] < 0.96
    assert p99["minimum_carrier_count"] == 133
    assert 0.99 <= p99["achieved_detection_probability"] < 1.0


def test_one_per_thousand_is_not_a_95_percent_detection_claim() -> None:
    carriers = round(POPULATION_APPLICATIONS * 0.001)
    probability = simple_random_detection_probability(
        population_size=POPULATION_APPLICATIONS,
        sample_size=SAMPLED_INSTITUTIONS_APPROX,
        carrier_count=carriers,
    )

    assert 0.70 < probability < 0.71


def test_sample_size_alone_has_zero_worst_case_detection_bound() -> None:
    row = unconstrained_selection_worst_case_detection(
        population_size=POPULATION_APPLICATIONS,
        sample_size=SAMPLED_INSTITUTIONS_APPROX,
        carrier_count=87,
    )

    assert row["sample_can_avoid_every_carrier"] is True
    assert row["minimum_carriers_in_sample"] == 0
    assert row["worst_case_detection_probability_lower_bound"] == 0.0


def test_e026_promotion_contract() -> None:
    payload = sampling_observation_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_observation_rule"] == (
        "sampling-design-metadata-required-before-prevalence-inference-v1"
    )
