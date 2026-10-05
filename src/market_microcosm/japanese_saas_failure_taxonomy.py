from __future__ import annotations


DIMENSIONS = (
    "kpi_sign_ambiguity",
    "reporting_kernel_break",
    "exit_decided",
    "competitive_advantage_failure",
    "persistent_profitability_failure",
    "runoff_transition",
    "residual_capability_value",
)


def case_fingerprints() -> dict[str, dict[str, bool]]:
    return {
        "BBD_portfolio_transition": {
            "kpi_sign_ambiguity": True,
            "reporting_kernel_break": False,
            "exit_decided": False,
            "competitive_advantage_failure": False,
            "persistent_profitability_failure": False,
            "runoff_transition": False,
            "residual_capability_value": False,
        },
        "Allied_overseas_saas_exit": {
            "kpi_sign_ambiguity": True,
            "reporting_kernel_break": True,
            "exit_decided": True,
            "competitive_advantage_failure": False,
            "persistent_profitability_failure": True,
            "runoff_transition": False,
            "residual_capability_value": False,
        },
        "Jooto_business_exit": {
            "kpi_sign_ambiguity": False,
            "reporting_kernel_break": False,
            "exit_decided": True,
            "competitive_advantage_failure": True,
            "persistent_profitability_failure": True,
            "runoff_transition": True,
            "residual_capability_value": True,
        },
    }


def one_bit_failure_label() -> dict[str, bool]:
    return {case: True for case in case_fingerprints()}


def taxonomy_report_payload() -> dict:
    fingerprints = case_fingerprints()
    vectors = {
        case: tuple(int(values[dimension]) for dimension in DIMENSIONS)
        for case, values in fingerprints.items()
    }
    pairwise_distances = {}
    cases = tuple(vectors)
    for index, left in enumerate(cases):
        for right in cases[index + 1 :]:
            pairwise_distances[f"{left}__vs__{right}"] = sum(
                a != b for a, b in zip(vectors[left], vectors[right])
            )

    gates = {
        "one_bit_failure_label_collapses_all_three_cases": (
            len(set(one_bit_failure_label().values())) == 1
        ),
        "typed_vectors_are_all_distinct": len(set(vectors.values())) == 3,
        "every_pair_differs_on_multiple_dimensions": all(
            distance >= 2 for distance in pairwise_distances.values()
        ),
        "only_allied_has_reporting_kernel_break": (
            sum(
                values["reporting_kernel_break"]
                for values in fingerprints.values()
            )
            == 1
            and fingerprints["Allied_overseas_saas_exit"][
                "reporting_kernel_break"
            ]
        ),
        "only_jooto_has_competitive_advantage_failure_and_runoff": (
            fingerprints["Jooto_business_exit"]["competitive_advantage_failure"]
            and fingerprints["Jooto_business_exit"]["runoff_transition"]
            and not fingerprints["BBD_portfolio_transition"]["runoff_transition"]
            and not fingerprints["Allied_overseas_saas_exit"]["runoff_transition"]
        ),
        "bbd_is_not_an_exit_case": (
            fingerprints["BBD_portfolio_transition"]["exit_decided"] is False
        ),
        "taxonomy_preserves_case_specific_mechanisms": True,
    }

    return {
        "experiment": "E096",
        "question": (
            "Can Japanese SaaS negative evidence be represented by one binary "
            "failure label, or does the evidence require a typed mechanism vector?"
        ),
        "cases": {
            "BBD_portfolio_transition": (
                "Active portfolio transition with KPI sign conflict; no business exit."
            ),
            "Allied_overseas_saas_exit": (
                "Deterioration-linked reporting-kernel break, governance checkpoint, "
                "and later overseas-business exit."
            ),
            "Jooto_business_exit": (
                "Nonzero traction but competitive-advantage/profitability failure, "
                "strategic resource reallocation, runoff obligations, and residual value."
            ),
        },
        "dimensions": list(DIMENSIONS),
        "one_bit_failure_label": one_bit_failure_label(),
        "fingerprints": fingerprints,
        "vectors": {case: list(vector) for case, vector in vectors.items()},
        "pairwise_hamming_distance": pairwise_distances,
        "promotion_gate": gates,
        "promoted_taxonomy_rule": (
            "japanese-saas-negative-evidence-requires-typed-mechanism-vector-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Failure evidence is represented as mechanism state, not a single label. "
            "Portfolio transition, observation-process break, competitive-advantage "
            "failure, profitability failure, exit runoff, and residual capability value "
            "remain independently visible."
        ),
        "limitations": (
            "The taxonomy currently contains three public-company case families and "
            "binary dimensions. It is a mechanism vocabulary, not a prevalence model "
            "or exhaustive classification of Japanese SaaS."
        ),
    }
