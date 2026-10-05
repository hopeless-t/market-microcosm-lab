from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations


@dataclass(frozen=True)
class EmpiricalSource:
    source_id: str
    name: str
    provider: str
    access_class: str
    public_values: bool
    authority_class: str
    observed_through: str
    granularity: str
    observables: tuple[str, ...]
    limitations: tuple[str, ...]
    url: str

    @property
    def evidence_cost(self) -> int:
        return {
            "public_official": 1,
            "public_academic": 2,
            "public_archive": 3,
            "request_only": 4,
            "restricted_partner": 5,
            "exploratory_nonofficial": 6,
        }[self.access_class]


TARGET_OBSERVABLES = (
    "allocation_accounting",
    "sampling_design",
    "demand_engagement",
    "regional_subscription_economics",
    "preference_structure",
    "catalog_diversity",
)


def empirical_source_registry() -> tuple[EmpiricalSource, ...]:
    return (
        EmpiricalSource(
            source_id="sartras-2022-management-overview",
            name="SARTRAS 2022 management overview",
            provider="SARTRAS",
            access_class="public_official",
            public_values=True,
            authority_class="official",
            observed_through="2022 fiscal year; published October 2024",
            granularity="annual accounting plus sampled usage reporting",
            observables=("allocation_accounting", "sampling_design"),
            limitations=(
                "Usage reports are sampled rather than a census.",
                "Published aggregate accounting is not a causal estimate.",
            ),
            url=(
                "https://sartras.or.jp/wp-content/uploads/"
                "kanrijigyougaikyo_2022.pdf"
            ),
        ),
        EmpiricalSource(
            source_id="netflix-h2-2025-engagement",
            name="Netflix What We Watched H2 2025",
            provider="Netflix",
            access_class="public_official",
            public_values=True,
            authority_class="official",
            observed_through="2025-07 through 2025-12",
            granularity="title-level engagement report",
            observables=("demand_engagement", "catalog_diversity"),
            limitations=(
                "Viewing is observational, not randomized exposure.",
                "Title-level engagement alone does not identify retention effects.",
            ),
            url=(
                "https://about.netflix.com/en/news/"
                "what-we-watched-the-second-half-of-2025"
            ),
        ),
        EmpiricalSource(
            source_id="netflix-q2-2024-regional",
            name="Netflix Q2 2024 shareholder letter",
            provider="Netflix",
            access_class="public_official",
            public_values=True,
            authority_class="official",
            observed_through="Q2 2024",
            granularity="regional streaming financial metrics",
            observables=("regional_subscription_economics",),
            limitations=(
                "ARM is average revenue per membership, not a posted plan price.",
                "Foreign exchange and plan/country mix affect reported ARM.",
            ),
            url=(
                "https://ir.netflix.net/files/doc_financials/2024/q2/"
                "FINAL-Q2-24-Shareholder-Letter.pdf"
            ),
        ),
        EmpiricalSource(
            source_id="movielens-32m",
            name="MovieLens 32M",
            provider="GroupLens Research",
            access_class="public_academic",
            public_values=True,
            authority_class="academic",
            observed_through="ratings collected through October 2023",
            granularity="user-item ratings and tags",
            observables=("preference_structure",),
            limitations=(
                "MovieLens users are self-selected and not Netflix users.",
                "Ratings are preference proxies, not subscription retention.",
            ),
            url="https://grouplens.org/datasets/movielens/32m/",
        ),
        EmpiricalSource(
            source_id="netflix-prize",
            name="Netflix Prize dataset",
            provider="Netflix / public archives",
            access_class="public_archive",
            public_values=True,
            authority_class="historical_official_origin",
            observed_through="historical prize period",
            granularity="user-title ratings with dates",
            observables=("preference_structure",),
            limitations=(
                "The dataset is historical and predates modern Netflix streaming.",
                "Archive availability and original redistribution terms require review.",
            ),
            url="https://www.kaggle.com/datasets/netflix-inc/netflix-prize-data",
        ),
        EmpiricalSource(
            source_id="gamepass-2022-members-lower-bound",
            name="Microsoft Game Pass 25M+ subscriber milestone",
            provider="Microsoft",
            access_class="public_official",
            public_values=True,
            authority_class="official",
            observed_through="2022-01-18",
            granularity="public membership headline",
            observables=("membership_scale",),
            limitations=(
                "The published value is a lower bound: more than 25 million.",
                "The later Game Pass Core conversion changes comparability risk.",
            ),
            url=(
                "https://news.microsoft.com/source/2022/01/18/"
                "microsoft-to-acquire-activision-blizzard-to-bring-the-joy-"
                "and-community-of-gaming-to-everyone-across-every-device/"
            ),
        ),
        EmpiricalSource(
            source_id="gamepass-core-2023-definition-event",
            name="Xbox Game Pass Core launch / Xbox Live Gold conversion",
            provider="Microsoft / Xbox",
            access_class="public_official",
            public_values=True,
            authority_class="official",
            observed_through="2023-09-14",
            granularity="membership-definition event",
            observables=("metric_definition",),
            limitations=(
                "This is a scope/change event rather than a membership count.",
            ),
            url=(
                "https://news.xbox.com/en-us/2023/07/17/"
                "xbox-game-pass-core/"
            ),
        ),
        EmpiricalSource(
            source_id="gamepass-2024-members-rounded",
            name="Xbox 34M Game Pass member headline",
            provider="Microsoft / Xbox",
            access_class="public_official",
            public_values=True,
            authority_class="official",
            observed_through="2024-02-15",
            granularity="public membership headline",
            observables=("membership_scale",),
            limitations=(
                "The public statement is a rounded headline value.",
                "Metric scope must be reconciled with the 2023 Core conversion.",
            ),
            url=(
                "https://news.xbox.com/en-us/podcast/"
                "phil-spencer-sarah-bond-and-matt-booty-share-updates-"
                "on-the-xbox-business/"
            ),
        ),
        EmpiricalSource(
            source_id="gamepass-partner-center-schema",
            name="Microsoft Partner Center Game Pass datasets",
            provider="Microsoft",
            access_class="restricted_partner",
            public_values=False,
            authority_class="official_schema",
            observed_through="partner-specific reporting periods",
            granularity="title-month-platform usage and purchase aggregates",
            observables=("demand_engagement", "regional_subscription_economics"),
            limitations=(
                "The schema is documented publicly but report values require authorization.",
                "Do not treat field definitions as public observations.",
            ),
            url=(
                "https://learn.microsoft.com/partner-center/insights/"
                "downloads-hub-datasets"
            ),
        ),
        EmpiricalSource(
            source_id="spotify-million-playlist",
            name="Spotify Million Playlist Dataset",
            provider="Spotify Research",
            access_class="request_only",
            public_values=False,
            authority_class="official_origin",
            observed_through="historical playlist sample",
            granularity="playlist-track graph",
            observables=("preference_structure", "catalog_diversity"),
            limitations=(
                "The dataset is not currently an immediate public download.",
                "The sample is not guaranteed to represent all Spotify users.",
            ),
            url=(
                "https://research.atspotify.com/2020/09/"
                "the-million-playlist-dataset-remastered"
            ),
        ),
    )


def sartras_2022_reconciliation() -> dict:
    unit = "JPY_thousand_tax_exclusive"
    receipts = {
        "primary_secondary": 2_263_598,
        "higher_education": 2_397_753,
        "article_4": 1_027,
    }
    allocation = {
        "distribution_fund": 3_403_744,
        "common_purpose_fund": 932_270,
        "administration_fee": 326_365,
    }

    receipt_total = sum(receipts.values())
    allocation_total = sum(allocation.values())
    rounding_delta = allocation_total - receipt_total

    return {
        "period": "FY2022",
        "unit": unit,
        "receipts": receipts,
        "receipt_total": receipt_total,
        "allocation": allocation,
        "allocation_total": allocation_total,
        "rounding_delta": rounding_delta,
        "absolute_rounding_delta": abs(rounding_delta),
        "allocation_shares": {
            key: value / allocation_total
            for key, value in allocation.items()
        },
        "sampling": {
            "all_applications": 35_130,
            "sampled_institutions_approx": 1_200,
            "usage_reports_approx": 46_600,
            "works_in_reports_approx": 118_600,
            "sampled_institution_fraction_approx": 1_200 / 35_130,
        },
        "source_id": "sartras-2022-management-overview",
    }


def netflix_q2_2024_region_anchor() -> dict:
    regions = {
        "UCAN": {
            "revenue_usd_millions": 4_296,
            "paid_memberships_millions": 84.11,
            "arm_usd": 17.17,
        },
        "EMEA": {
            "revenue_usd_millions": 3_008,
            "paid_memberships_millions": 93.96,
            "arm_usd": 10.80,
        },
        "LATAM": {
            "revenue_usd_millions": 1_204,
            "paid_memberships_millions": 49.25,
            "arm_usd": 8.28,
        },
        "APAC": {
            "revenue_usd_millions": 1_052,
            "paid_memberships_millions": 50.32,
            "arm_usd": 7.17,
        },
    }
    arms = [row["arm_usd"] for row in regions.values()]
    memberships = [
        row["paid_memberships_millions"]
        for row in regions.values()
    ]
    weighted_arm = sum(
        row["arm_usd"] * row["paid_memberships_millions"]
        for row in regions.values()
    ) / sum(memberships)

    return {
        "period": "Q2-2024",
        "regions": regions,
        "arm_max_min_ratio": max(arms) / min(arms),
        "membership_weighted_arm_usd": weighted_arm,
        "source_id": "netflix-q2-2024-regional",
        "interpretation_guard": (
            "ARM is average revenue per membership and must not be "
            "relabelled as posted subscription price."
        ),
    }


def netflix_h2_2025_engagement_anchor() -> dict:
    return {
        "period": "2025-07/2025-12",
        "hours_watched": 96_000_000_000,
        "source_id": "netflix-h2-2025-engagement",
        "interpretation_guard": (
            "Do not divide this period total by a membership headline from "
            "another period without an explicit alignment model."
        ),
    }


def _covered_observables(
    sources: tuple[EmpiricalSource, ...],
) -> set[str]:
    covered: set[str] = set()
    for source in sources:
        covered.update(source.observables)
    return covered


def exact_public_source_portfolio(
    target_observables: tuple[str, ...] = TARGET_OBSERVABLES,
) -> dict:
    registry = empirical_source_registry()
    eligible = tuple(
        source
        for source in registry
        if source.public_values
        and source.access_class.startswith("public_")
        and source.authority_class
        in {"official", "academic", "historical_official_origin"}
    )
    target = set(target_observables)
    feasible: list[tuple[tuple, tuple[EmpiricalSource, ...]]] = []

    for size in range(1, len(eligible) + 1):
        for subset in combinations(eligible, size):
            covered = _covered_observables(subset)
            if target <= covered:
                score = (
                    size,
                    sum(source.evidence_cost for source in subset),
                    tuple(source.source_id for source in subset),
                )
                feasible.append((score, subset))
        if feasible:
            break

    if not feasible:
        raise ValueError("no public source portfolio covers target observables")

    _, selected = min(feasible, key=lambda row: row[0])
    covered = _covered_observables(selected)

    return {
        "target_observables": sorted(target),
        "selected_source_ids": [
            source.source_id for source in selected
        ],
        "selected_count": len(selected),
        "evidence_cost": sum(
            source.evidence_cost for source in selected
        ),
        "covered_observables": sorted(covered & target),
        "missing_observables": sorted(target - covered),
    }


def empirical_evidence_report_payload() -> dict:
    registry = empirical_source_registry()
    portfolio = exact_public_source_portfolio()
    sartras = sartras_2022_reconciliation()
    netflix_regions = netflix_q2_2024_region_anchor()
    netflix_engagement = netflix_h2_2025_engagement_anchor()

    restricted_ids = {
        source.source_id
        for source in registry
        if not source.public_values
    }
    selected_ids = set(portfolio["selected_source_ids"])

    gates = {
        "sartras_accounting_closes_within_published_rounding": (
            sartras["absolute_rounding_delta"] <= 1
        ),
        "public_portfolio_covers_target_observables": (
            not portfolio["missing_observables"]
        ),
        "public_portfolio_contains_no_restricted_values": (
            selected_ids.isdisjoint(restricted_ids)
        ),
        "gamepass_schema_not_promoted_as_public_observation": (
            "gamepass-partner-center-schema" not in selected_ids
        ),
        "spotify_request_only_not_promoted_as_public_observation": (
            "spotify-million-playlist" not in selected_ids
        ),
        "netflix_regional_arm_requires_heterogeneity": (
            netflix_regions["arm_max_min_ratio"] > 2.0
        ),
        "period_alignment_guard_present": (
            "another period"
            in netflix_engagement["interpretation_guard"]
        ),
    }

    return {
        "experiment": "E024",
        "question": (
            "Can public empirical observations constrain the synthetic "
            "market without allowing restricted, stale, or schema-only "
            "evidence to silently gain calibration authority?"
        ),
        "source_registry": [asdict(source) for source in registry],
        "target_observables": list(TARGET_OBSERVABLES),
        "public_portfolio": portfolio,
        "anchors": {
            "sartras_2022": sartras,
            "netflix_q2_2024_regions": netflix_regions,
            "netflix_h2_2025_engagement": netflix_engagement,
        },
        "promotion_gate": gates,
        "promoted_evidence_rule": (
            "empirical-evidence-plane-v1"
            if all(gates.values())
            else None
        ),
        "next_model_constraints": {
            "global_fixed_price": (
                "reject for empirical calibration; add regional economics"
            ),
            "gamepass_usage_values": (
                "adapter only until authorized observations exist"
            ),
            "cross_period_ratio": (
                "forbidden unless periods and populations are aligned"
            ),
            "synthetic_causal_claims": (
                "remain separate from empirical calibration"
            ),
        },
        "limitations": (
            "E024 validates evidence admission and a small set of published "
            "anchors. It does not claim that SARTRAS, Netflix, Game Pass, "
            "MovieLens, or Spotify share one causal market mechanism."
        ),
    }
