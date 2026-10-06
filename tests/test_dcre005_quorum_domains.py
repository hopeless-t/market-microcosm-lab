import pytest

from market_microcosm.dcre005_quorum_domains import (
    frozen_quorum_report,
    frozen_topologies,
    quorum_accuracy,
)


def test_three_nominal_witnesses_can_be_one_effective_domain() -> None:
    same, _, independent = frozen_topologies()
    assert same.witness_count == independent.witness_count == 3
    assert same.domain_count == 1
    assert independent.domain_count == 3


def test_three_independent_domains_improve_majority_accuracy() -> None:
    same, pair, independent = frozen_topologies()
    assert quorum_accuracy(same) == pytest.approx(0.8)
    assert quorum_accuracy(pair) == pytest.approx(0.8)
    assert quorum_accuracy(independent) == pytest.approx(0.896)


def test_frozen_report_separates_witness_count_from_domain_count() -> None:
    report = frozen_quorum_report()
    assert report["same-domain-3"]["nominal_witnesses"] == 3
    assert report["same-domain-3"]["independent_domains"] == 1
    assert report["correlated-pair-2-1"]["independent_domains"] == 2
    assert report["independent-1-1-1"]["independent_domains"] == 3
    assert report["independent-1-1-1"]["majority_accuracy"] > report["same-domain-3"]["majority_accuracy"]


def test_invalid_accuracy_fails_closed() -> None:
    topology = frozen_topologies()[0]
    with pytest.raises(ValueError):
        quorum_accuracy(topology, domain_accuracy=1.1)
