from __future__ import annotations


POPULATION_APPLICATIONS = 35_130
SAMPLED_INSTITUTIONS_APPROX = 1_200


def simple_random_detection_probability(
    *,
    population_size: int,
    sample_size: int,
    carrier_count: int,
) -> float:
    if not 0 <= carrier_count <= population_size:
        raise ValueError("carrier_count outside population")
    if not 0 <= sample_size <= population_size:
        raise ValueError("sample_size outside population")
    if carrier_count == 0 or sample_size == 0:
        return 0.0
    if carrier_count > population_size - sample_size:
        return 1.0

    probability_zero_hits = 1.0
    for draw in range(sample_size):
        probability_zero_hits *= (
            population_size - carrier_count - draw
        ) / (population_size - draw)

    return 1.0 - probability_zero_hits


def minimum_carriers_for_detection(
    target_probability: float,
    *,
    population_size: int = POPULATION_APPLICATIONS,
    sample_size: int = SAMPLED_INSTITUTIONS_APPROX,
) -> dict:
    if not 0.0 < target_probability < 1.0:
        raise ValueError("target_probability must be inside (0, 1)")

    for carrier_count in range(1, population_size + 1):
        probability = simple_random_detection_probability(
            population_size=population_size,
            sample_size=sample_size,
            carrier_count=carrier_count,
        )
        if probability >= target_probability:
            return {
                "target_detection_probability": target_probability,
                "minimum_carrier_count": carrier_count,
                "minimum_population_fraction": (
                    carrier_count / population_size
                ),
                "achieved_detection_probability": probability,
            }

    raise AssertionError("detection target should be reachable")


def unconstrained_selection_worst_case_detection(
    *,
    population_size: int,
    sample_size: int,
    carrier_count: int,
) -> dict:
    noncarriers = population_size - carrier_count
    sample_can_avoid_every_carrier = noncarriers >= sample_size
    minimum_carriers_in_sample = max(
        0,
        sample_size - noncarriers,
    )

    return {
        "sample_can_avoid_every_carrier": sample_can_avoid_every_carrier,
        "minimum_carriers_in_sample": minimum_carriers_in_sample,
        "worst_case_detection_probability_lower_bound": (
            0.0 if sample_can_avoid_every_carrier else 1.0
        ),
    }


def sampling_observation_report_payload() -> dict:
    population_size = POPULATION_APPLICATIONS
    sample_size = SAMPLED_INSTITUTIONS_APPROX

    thresholds = {
        str(int(target * 100)): minimum_carriers_for_detection(
            target,
            population_size=population_size,
            sample_size=sample_size,
        )
        for target in (0.50, 0.90, 0.95, 0.99)
    }

    srs_95 = thresholds["95"]
    adversarial = unconstrained_selection_worst_case_detection(
        population_size=population_size,
        sample_size=sample_size,
        carrier_count=srs_95["minimum_carrier_count"],
    )

    one_per_thousand_count = round(population_size * 0.001)
    one_per_thousand_srs = simple_random_detection_probability(
        population_size=population_size,
        sample_size=sample_size,
        carrier_count=one_per_thousand_count,
    )

    gates = {
        "sample_is_small_relative_to_population": (
            sample_size / population_size < 0.05
        ),
        "srs_reference_has_nontrivial_detection_knee": (
            0.002
            < srs_95["minimum_population_fraction"]
            < 0.003
        ),
        "one_per_thousand_is_not_95_percent_detectable_under_srs": (
            one_per_thousand_srs < 0.95
        ),
        "sample_size_alone_allows_zero_detection_world": (
            adversarial[
                "worst_case_detection_probability_lower_bound"
            ]
            == 0.0
        ),
        "actual_selection_probability_model_is_not_assumed": True,
        "sampling_design_metadata_required_before_prevalence_inference": True,
    }

    return {
        "experiment": "E026",
        "question": (
            "What can the published SARTRAS sample size establish about "
            "observation coverage, and which conclusions fail once the "
            "unpublished selection mechanism is treated as unknown?"
        ),
        "empirical_anchor": {
            "source_id": "sartras-2022-management-overview",
            "population_applications": population_size,
            "sampled_institutions_approx": sample_size,
            "sample_fraction_approx": sample_size / population_size,
            "usage_reports_approx": 46_600,
            "works_in_reports_approx": 118_600,
            "reporting_window": "approximately one designated month per institution",
        },
        "hypothetical_srs_reference": {
            "assumption": (
                "uniform simple random sampling without replacement; "
                "reference calculation only, not attributed to SARTRAS"
            ),
            "detection_thresholds": thresholds,
            "one_per_thousand": {
                "carrier_count": one_per_thousand_count,
                "detection_probability": one_per_thousand_srs,
            },
        },
        "adversarial_unknown_design": {
            "carrier_count": srs_95["minimum_carrier_count"],
            **adversarial,
            "interpretation": (
                "Without inclusion probabilities or constraints on selection, "
                "the same nominal sample size can entirely miss a phenomenon "
                "concentrated outside the selected institutions."
            ),
        },
        "promotion_gate": gates,
        "promoted_observation_rule": (
            "sampling-design-metadata-required-before-prevalence-inference-v1"
            if all(gates.values())
            else None
        ),
        "required_future_metadata": (
            "selection frame",
            "strata",
            "inclusion probabilities or weighting rule",
            "nonresponse handling",
            "time-window assignment",
        ),
        "model_update": (
            "Do not calibrate an empirical governor's observation noise from "
            "sample count alone. Keep sampled observation separate from latent "
            "world state and fail closed on prevalence inference until the "
            "selection design is identified."
        ),
        "limitations": (
            "The SRS detection curve is a mathematical reference world. "
            "E026 makes no claim that SARTRAS used simple random sampling, "
            "nor that institutions are exchangeable or that usage events are "
            "independent within institutions."
        ),
    }
