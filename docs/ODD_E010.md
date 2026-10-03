# ODD protocol — E010 ecological market

## Purpose

Study how pooled subscription revenue, actor solvency, catalog composition, user utility, entry, exit, and allocation rules interact over long horizons.

## Entities and state

- two user preference segments;
- a platform with a cash reserve and operating cost;
- developers with segment, reserve cash, production cost, publisher relation, and active state;
- publishers with reserve cash, operating cost, and active state;
- content with segment, quality, age, developer ownership, and availability.

One step represents an abstract month.

## Scheduling

1. Current catalog determines segment utility and engagement.
2. Users pay subscription revenue.
3. The mechanism splits revenue between platform and creator pool.
4. Creator pool is divided among usage, survival floor, and ecosystem fund.
5. Publisher fees and developer payouts are applied.
6. Operating/production costs leave the closed market as explicit external sinks.
7. Insolvent actors exit.
8. A declared external startup-capital source may fund a dormant entrant.
9. Catalog availability updates.
10. User populations update through utility-sensitive churn/acquisition and a bounded exogenous market shock.

## Design concepts

### Viability
Platform, developer population, publisher population, user population, and service quality must remain above declared floors.

### Adaptation
Allocation mechanisms alter the flow of capital and therefore future catalog survival.

### Sensing
E010 currently gives the mechanism aggregate contemporaneous usage. Later versions will introduce delayed/noisy observation.

### Stochasticity
Only declared bounded demand shocks and entry draws use randomness. Seeds are split across discovery, promotion, meta evaluation, and baseline reporting.

### Conservation
Internal transfers conserve cash. Subscription revenue and entrant capital are explicit external sources; operating/production costs are explicit external sinks.

## Limitations

- user preferences are only two-dimensional;
- prices are fixed during E010;
- content creation quality is exogenous;
- publishers do not renegotiate contracts;
- recommendation/exposure is implicit in appeal rather than strategic;
- no causal attribution or Shapley allocation is used yet.

These simplifications are deliberate so that failure mechanisms remain inspectable.
