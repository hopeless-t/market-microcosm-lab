from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class UserSegment:
    name: str
    population: float


@dataclass(frozen=True)
class Developer:
    developer_id: str
    segment: str
    cash: float
    monthly_cost: float
    publisher_id: str
    active: bool = True
    entrant: bool = False


@dataclass(frozen=True)
class Publisher:
    publisher_id: str
    cash: float
    monthly_cost: float
    active: bool = True


@dataclass(frozen=True)
class Content:
    content_id: str
    developer_id: str
    segment: str
    quality: float
    age: int = 0
    active: bool = True


@dataclass(frozen=True)
class Mechanism:
    name: str
    platform_take: float
    survival_floor_share: float
    ecosystem_fund_share: float
    publisher_fee: float = 0.08

    def __post_init__(self) -> None:
        values = (
            self.platform_take,
            self.survival_floor_share,
            self.ecosystem_fund_share,
            self.publisher_fee,
        )
        if any(x < 0 or x > 1 for x in values):
            raise ValueError("mechanism shares must be in [0, 1]")
        if self.survival_floor_share + self.ecosystem_fund_share > 1:
            raise ValueError("floor + ecosystem fund cannot exceed creator pool")


@dataclass(frozen=True)
class MarketState:
    month: int
    users: tuple[UserSegment, ...]
    developers: tuple[Developer, ...]
    publishers: tuple[Publisher, ...]
    contents: tuple[Content, ...]
    platform_cash: float
    cumulative_entries: int = 0
    cumulative_exits: int = 0

    @property
    def total_users(self) -> float:
        return sum(x.population for x in self.users)

    @property
    def active_developers(self) -> tuple[Developer, ...]:
        return tuple(x for x in self.developers if x.active)

    @property
    def active_publishers(self) -> tuple[Publisher, ...]:
        return tuple(x for x in self.publishers if x.active)

    @property
    def total_internal_cash(self) -> float:
        return (
            self.platform_cash
            + sum(x.cash for x in self.developers)
            + sum(x.cash for x in self.publishers)
        )


@dataclass(frozen=True)
class MarketMetrics:
    user_utility: float
    diversity: float
    active_developers: int
    active_publishers: int
    total_users: float
    platform_cash: float
    health: float


@dataclass(frozen=True)
class StepAudit:
    before_cash: float
    after_cash: float
    external_revenue: float
    external_costs: float
    entry_capital: float
    conservation_error: float
    creator_pool: float
    creator_paid: float


@dataclass(frozen=True)
class StepResult:
    state: MarketState
    metrics: MarketMetrics
    audit: StepAudit


@dataclass(frozen=True)
class MarketWorld:
    subscription_price: float = 10.0
    platform_monthly_cost: float = 1800.0
    utility_target: float = 0.65
    base_churn_rate: float = 0.020
    churn_sensitivity: float = 0.15
    base_acquisition_rate: float = 0.022
    entry_startup_capital: float = 1800.0
    entry_probability_cap: float = 0.20
    minimum_users: float = 500.0
    minimum_active_developers: int = 2
    minimum_active_publishers: int = 1
    minimum_service_quality: float = 0.40

    def initial_state(self) -> MarketState:
        return MarketState(
            month=0,
            users=(
                UserSegment("mainstream", 900.0),
                UserSegment("niche", 100.0),
            ),
            developers=(
                Developer("dev-main-a", "mainstream", 4200.0, 1300.0, "pub-main"),
                Developer("dev-main-b", "mainstream", 3600.0, 1200.0, "pub-main"),
                Developer("dev-niche-a", "niche", 1800.0, 1000.0, "pub-niche"),
                Developer(
                    "dev-niche-b",
                    "niche",
                    0.0,
                    950.0,
                    "pub-niche",
                    active=False,
                    entrant=True,
                ),
            ),
            publishers=(
                Publisher("pub-main", 2600.0, 350.0),
                Publisher("pub-niche", 1500.0, 80.0),
            ),
            contents=(
                Content("content-main-a", "dev-main-a", "mainstream", 0.88),
                Content("content-main-b", "dev-main-b", "mainstream", 0.78),
                Content("content-niche-a", "dev-niche-a", "niche", 0.82),
                Content(
                    "content-niche-b",
                    "dev-niche-b",
                    "niche",
                    0.76,
                    active=False,
                ),
            ),
            platform_cash=6000.0,
        )

    def _publisher_map(self, state: MarketState) -> dict[str, Publisher]:
        return {p.publisher_id: p for p in state.publishers}

    def _developer_map(self, state: MarketState) -> dict[str, Developer]:
        return {d.developer_id: d for d in state.developers}

    def available_contents(self, state: MarketState) -> tuple[Content, ...]:
        developers = self._developer_map(state)
        publishers = self._publisher_map(state)
        available: list[Content] = []
        for c in state.contents:
            developer = developers[c.developer_id]
            publisher = publishers[developer.publisher_id]
            if c.active and developer.active and publisher.active:
                available.append(c)
        return tuple(available)

    @staticmethod
    def _appeal(user_segment: str, content: Content) -> float:
        match = 1.0 if user_segment == content.segment else 0.12
        freshness = max(0.65, 1.0 - 0.005 * content.age)
        return content.quality * match * freshness

    def segment_utility(self, state: MarketState, segment_name: str) -> float:
        appeals = sorted(
            (self._appeal(segment_name, c) for c in self.available_contents(state)),
            reverse=True,
        )
        if not appeals:
            return 0.0
        first = appeals[0]
        second = appeals[1] if len(appeals) > 1 else 0.0
        matching = sum(
            1 for c in self.available_contents(state) if c.segment == segment_name
        )
        breadth = min(0.10, 0.05 * math.sqrt(matching))
        return min(1.0, 0.70 * first + 0.20 * second + breadth)

    def engagement(self, state: MarketState) -> dict[str, float]:
        contents = self.available_contents(state)
        result = {c.content_id: 0.0 for c in contents}
        for segment in state.users:
            weights = [max(1e-9, self._appeal(segment.name, c)) for c in contents]
            denom = sum(weights)
            if denom <= 0:
                continue
            for content, weight in zip(contents, weights):
                result[content.content_id] += segment.population * weight / denom
        return result

    def metrics(self, state: MarketState) -> MarketMetrics:
        total_users = state.total_users
        if total_users > 0:
            utility = sum(
                s.population * self.segment_utility(state, s.name)
                for s in state.users
            ) / total_users
        else:
            utility = 0.0

        contents = self.available_contents(state)
        counts: dict[str, int] = {}
        for c in contents:
            counts[c.segment] = counts.get(c.segment, 0) + 1
        if len(counts) <= 1:
            diversity = 0.0
        else:
            total = sum(counts.values())
            entropy = -sum(
                (n / total) * math.log(n / total)
                for n in counts.values()
                if n > 0
            )
            diversity = entropy / math.log(len(counts))

        active_devs = len(state.active_developers)
        active_pubs = len(state.active_publishers)
        dev_health = active_devs / max(1, len(state.developers))
        publisher_health = active_pubs / max(1, len(state.publishers))
        platform_health = (
            max(0.0, state.platform_cash)
            / (max(0.0, state.platform_cash) + 5000.0)
            if state.platform_cash > 0
            else 0.0
        )
        components = (
            max(1e-9, utility),
            max(1e-9, diversity),
            max(1e-9, dev_health),
            max(1e-9, publisher_health),
            max(1e-9, platform_health),
        )
        health = math.prod(components) ** (1.0 / len(components))

        return MarketMetrics(
            user_utility=utility,
            diversity=diversity,
            active_developers=active_devs,
            active_publishers=active_pubs,
            total_users=total_users,
            platform_cash=state.platform_cash,
            health=health,
        )

    def viable(self, state: MarketState) -> bool:
        metrics = self.metrics(state)
        return (
            state.platform_cash >= 0
            and metrics.active_developers >= self.minimum_active_developers
            and metrics.active_publishers >= self.minimum_active_publishers
            and metrics.total_users >= self.minimum_users
            and metrics.user_utility >= self.minimum_service_quality
        )

    def _developer_allocations(
        self,
        state: MarketState,
        mechanism: Mechanism,
        creator_pool: float,
        engagement: dict[str, float],
    ) -> dict[str, float]:
        active = list(state.active_developers)
        if not active:
            return {}

        allocations = {d.developer_id: 0.0 for d in active}
        floor_pool = creator_pool * mechanism.survival_floor_share
        ecosystem_pool = creator_pool * mechanism.ecosystem_fund_share
        usage_pool = creator_pool - floor_pool - ecosystem_pool

        for d in active:
            allocations[d.developer_id] += floor_pool / len(active)

        content_by_id = {c.content_id: c for c in self.available_contents(state)}
        usage_by_dev = {d.developer_id: 0.0 for d in active}
        for content_id, amount in engagement.items():
            content = content_by_id[content_id]
            usage_by_dev[content.developer_id] += amount
        usage_total = sum(usage_by_dev.values())
        if usage_total > 0:
            for developer_id, amount in usage_by_dev.items():
                allocations[developer_id] += usage_pool * amount / usage_total
        else:
            for d in active:
                allocations[d.developer_id] += usage_pool / len(active)

        segment_counts: dict[str, int] = {}
        for c in self.available_contents(state):
            segment_counts[c.segment] = segment_counts.get(c.segment, 0) + 1
        if ecosystem_pool > 0:
            supported_segment = min(
                (d.segment for d in active),
                key=lambda s: (segment_counts.get(s, 0), s),
            )
            supported = [d for d in active if d.segment == supported_segment]
            for d in supported:
                allocations[d.developer_id] += ecosystem_pool / len(supported)

        return allocations

    def _update_users(
        self,
        state: MarketState,
        rng: random.Random,
    ) -> tuple[UserSegment, ...]:
        updated: list[UserSegment] = []
        for segment in state.users:
            utility = self.segment_utility(state, segment.name)
            churn = self.base_churn_rate + max(
                0.0, self.utility_target - utility
            ) * self.churn_sensitivity
            acquisition = self.base_acquisition_rate * utility / self.utility_target
            market_shock = rng.uniform(-0.004, 0.004)
            growth_rate = acquisition - churn + market_shock
            population = max(0.0, segment.population * (1.0 + growth_rate))
            updated.append(UserSegment(segment.name, population))
        return tuple(updated)

    def step(
        self,
        state: MarketState,
        mechanism: Mechanism,
        rng: random.Random,
    ) -> StepResult:
        before_cash = state.total_internal_cash
        external_revenue = state.total_users * self.subscription_price
        engagement = self.engagement(state)

        creator_pool = external_revenue * (1.0 - mechanism.platform_take)
        allocations = self._developer_allocations(
            state, mechanism, creator_pool, engagement
        )
        creator_paid = sum(allocations.values())

        publisher_map = self._publisher_map(state)
        publisher_income = {p.publisher_id: 0.0 for p in state.publishers}
        developer_income = {d.developer_id: 0.0 for d in state.developers}

        for developer in state.active_developers:
            gross = allocations.get(developer.developer_id, 0.0)
            publisher = publisher_map[developer.publisher_id]
            fee = gross * mechanism.publisher_fee if publisher.active else 0.0
            publisher_income[developer.publisher_id] += fee
            developer_income[developer.developer_id] += gross - fee

        external_costs = self.platform_monthly_cost
        external_costs += sum(d.monthly_cost for d in state.active_developers)
        external_costs += sum(p.monthly_cost for p in state.active_publishers)

        updated_publishers: list[Publisher] = []
        for publisher in state.publishers:
            if publisher.active:
                cash = (
                    publisher.cash
                    + publisher_income[publisher.publisher_id]
                    - publisher.monthly_cost
                )
                updated_publishers.append(
                    Publisher(
                        publisher.publisher_id,
                        cash,
                        publisher.monthly_cost,
                        active=cash >= 0,
                    )
                )
            else:
                updated_publishers.append(publisher)

        updated_developers: list[Developer] = []
        exits = 0
        for developer in state.developers:
            if developer.active:
                cash = (
                    developer.cash
                    + developer_income[developer.developer_id]
                    - developer.monthly_cost
                )
                active = cash >= 0
                exits += int(not active)
                updated_developers.append(
                    Developer(
                        developer.developer_id,
                        developer.segment,
                        cash,
                        developer.monthly_cost,
                        developer.publisher_id,
                        active=active,
                        entrant=developer.entrant,
                    )
                )
            else:
                updated_developers.append(developer)

        updated_publisher_map = {
            p.publisher_id: p for p in updated_publishers
        }
        entry_capital = 0.0
        entries = 0
        active_after = [d for d in updated_developers if d.active]
        average_creator_income = (
            creator_paid / len(active_after) if active_after else 0.0
        )
        dormant = [
            d
            for d in updated_developers
            if (not d.active)
            and d.entrant
            and updated_publisher_map[d.publisher_id].active
            and d.cash == 0.0
        ]
        if dormant and active_after:
            average_cost = sum(d.monthly_cost for d in active_after) / len(active_after)
            attractiveness = max(0.0, average_creator_income / max(1.0, average_cost) - 1.0)
            probability = min(
                self.entry_probability_cap,
                0.03 + 0.08 * attractiveness,
            )
            if rng.random() < probability:
                entrant = dormant[0]
                entry_capital = self.entry_startup_capital
                entries = 1
                updated_developers = [
                    Developer(
                        d.developer_id,
                        d.segment,
                        entry_capital if d.developer_id == entrant.developer_id else d.cash,
                        d.monthly_cost,
                        d.publisher_id,
                        active=True if d.developer_id == entrant.developer_id else d.active,
                        entrant=d.entrant,
                    )
                    for d in updated_developers
                ]

        developer_active = {d.developer_id: d.active for d in updated_developers}
        updated_contents: list[Content] = []
        for content in state.contents:
            activate_entry_content = (
                entries == 1
                and content.developer_id == dormant[0].developer_id
                if dormant
                else False
            )
            active = (
                (content.active or activate_entry_content)
                and developer_active[content.developer_id]
            )
            updated_contents.append(
                Content(
                    content.content_id,
                    content.developer_id,
                    content.segment,
                    content.quality,
                    age=content.age + 1 if active else content.age,
                    active=active,
                )
            )

        platform_cash = (
            state.platform_cash
            + external_revenue
            - creator_paid
            - self.platform_monthly_cost
        )

        pre_user_state = MarketState(
            month=state.month + 1,
            users=state.users,
            developers=tuple(updated_developers),
            publishers=tuple(updated_publishers),
            contents=tuple(updated_contents),
            platform_cash=platform_cash,
            cumulative_entries=state.cumulative_entries + entries,
            cumulative_exits=state.cumulative_exits + exits,
        )
        updated_users = self._update_users(pre_user_state, rng)
        next_state = MarketState(
            month=pre_user_state.month,
            users=updated_users,
            developers=pre_user_state.developers,
            publishers=pre_user_state.publishers,
            contents=pre_user_state.contents,
            platform_cash=pre_user_state.platform_cash,
            cumulative_entries=pre_user_state.cumulative_entries,
            cumulative_exits=pre_user_state.cumulative_exits,
        )

        after_cash = next_state.total_internal_cash
        expected_after = (
            before_cash + external_revenue + entry_capital - external_costs
        )
        conservation_error = after_cash - expected_after
        if abs(conservation_error) > 1e-6:
            raise AssertionError(
                f"market ledger violated conservation: {conservation_error=}"
            )

        audit = StepAudit(
            before_cash=before_cash,
            after_cash=after_cash,
            external_revenue=external_revenue,
            external_costs=external_costs,
            entry_capital=entry_capital,
            conservation_error=conservation_error,
            creator_pool=creator_pool,
            creator_paid=creator_paid,
        )
        return StepResult(
            state=next_state,
            metrics=self.metrics(next_state),
            audit=audit,
        )


def default_mechanisms() -> tuple[Mechanism, ...]:
    return (
        Mechanism("usage-only", 0.30, 0.00, 0.00),
        Mechanism("light-floor", 0.30, 0.10, 0.05),
        Mechanism("balanced", 0.30, 0.15, 0.10),
        Mechanism("diversity-heavy", 0.30, 0.10, 0.20),
        Mechanism("creator-heavy", 0.24, 0.15, 0.10),
        Mechanism("platform-heavy", 0.38, 0.10, 0.05),
    )
