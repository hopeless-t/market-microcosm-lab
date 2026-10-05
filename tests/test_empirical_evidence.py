from market_microcosm.empirical_evidence import (
    TARGET_OBSERVABLES,
    empirical_evidence_report_payload,
    empirical_source_registry,
    exact_public_source_portfolio,
    netflix_q2_2024_region_anchor,
    sartras_2022_reconciliation,
)


def test_sartras_2022_accounting_reconciles_to_rounding() -> None:
    row = sartras_2022_reconciliation()

    assert row["receipt_total"] == 4_662_378
    assert row["allocation_total"] == 4_662_379
    assert row["rounding_delta"] == 1
    assert row["absolute_rounding_delta"] <= 1


def test_netflix_regional_arm_is_not_a_single_global_value() -> None:
    row = netflix_q2_2024_region_anchor()

    assert row["regions"]["UCAN"]["arm_usd"] == 17.17
    assert row["regions"]["APAC"]["arm_usd"] == 7.17
    assert row["arm_max_min_ratio"] > 2.0


def test_public_portfolio_excludes_restricted_sources() -> None:
    registry = {
        row.source_id: row
        for row in empirical_source_registry()
    }
    portfolio = exact_public_source_portfolio()
    selected = set(portfolio["selected_source_ids"])

    assert not portfolio["missing_observables"]
    assert set(TARGET_OBSERVABLES) <= set(
        portfolio["covered_observables"]
    )
    assert "gamepass-partner-center-schema" not in selected
    assert "spotify-million-playlist" not in selected
    assert all(registry[source_id].public_values for source_id in selected)


def test_schema_visibility_is_not_observation_visibility() -> None:
    gamepass = next(
        row
        for row in empirical_source_registry()
        if row.source_id == "gamepass-partner-center-schema"
    )

    assert gamepass.authority_class == "official_schema"
    assert gamepass.access_class == "restricted_partner"
    assert gamepass.public_values is False


def test_e024_promotion_contract() -> None:
    payload = empirical_evidence_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_evidence_rule"] == "empirical-evidence-plane-v1"
