from market_microcosm.dcre055_external_site_energy_audit import (
    RecordSemantics,
    dcre055_external_site_energy_audit,
)


def test_external_authoritative_records_add_context_but_not_customer_energy() -> None:
    report = dcre055_external_site_energy_audit()
    assert report["utility_aggregate_energy_observed"] is True
    assert report["power_or_contract_capacity_observed"] is True
    assert report["customer_site_energy_record_count"] == 0
    assert report["google_the_dalles_annual_mwh"] is None


def test_capacity_and_aggregate_load_are_not_silently_retyped_as_site_energy() -> None:
    report = dcre055_external_site_energy_audit()
    assert report["power_capacity_is_energy_consumption"] is False
    assert report["utility_aggregate_is_customer_load"] is False
    assert report["site_wue_identified"] is False
    assert all(
        record.semantics
        in {
            RecordSemantics.UTILITY_AGGREGATE_ENERGY,
            RecordSemantics.PEAK_OR_CONTRACT_CAPACITY,
        }
        for record in report["records"]
    )


def test_external_expansion_does_not_upgrade_authority() -> None:
    report = dcre055_external_site_energy_audit()
    assert report["authority_effect"] == "NONE"
