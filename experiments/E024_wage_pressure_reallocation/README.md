# E024 — Wage pressure, bargaining power, and worker reallocation

E024 returns the lab to its ecological-market core and asks a deceptively simple question:

> When wage pressure causes firms to exit, does the system actually reallocate workers toward higher-productivity / higher-wage activity, or can transition friction turn creative destruction into plain destruction?

This is a **synthetic experiment proposal**, not an empirical estimate or a policy recommendation.

## External observation that motivates the experiment

Tokyo Shoko Research reported that in FY2026 H1 (April–September), 240 Japanese bankruptcies were classified as related to labor shortages, with 130 attributed to rising personnel costs. Firms with capital below JPY 10 million accounted for 66.2%, and services plus construction accounted for 60.8%.

Source:

- Tokyo Shoko Research, 2026-10-05: https://www.tsr-net.co.jp/data/detail/1203295_1527.html

The SME Agency's September 2025 price-negotiation survey reported a 50.0% pass-through rate for labor costs, below the corresponding raw-material pass-through rate.

Source:

- Small and Medium Enterprise Agency: https://www.chusho.meti.go.jp/keiei/torihiki/kaiseihou_setsumeikai/gaiyo.pdf

A Hatena Anonymous Diary post used the bankruptcy report to argue that firms unable to support adequate wages should exit. The post is useful here as a **hypothesis generator**, not as evidence about firm quality, owner extraction, or welfare effects.

Prompt source:

- https://anond.hatelabo.jp/20261005133437

## Core distinction

E024 explicitly separates:

```text
firm exit != productivity selection
higher wage floor != successful worker reallocation
higher aggregate productivity != higher worker welfare
price pressure != firm inefficiency
worker availability != worker mobility
```

A system can destroy low-productivity firms and improve allocation. It can also destroy viable but low-bargaining-power firms, strand workers who lack transition runway, increase concentration, or accelerate automation without preserving worker welfare.

## Synthetic actors

### Firm state

For firm `i`:

```text
F_i = (
  productivity,
  cash_buffer,
  wage_offer,
  labor_demand,
  output_price,
  price_pass_through,
  bargaining_power,
  fixed_cost,
  automation_option,
  market_share
)
```

A minimal profit identity is:

```text
profit_i = revenue_i - wage_bill_i - fixed_cost_i - transition_cost_i
```

`price_pass_through` and `bargaining_power` are kept distinct from productivity so the experiment can test whether the wrong firms are selected out.

### Worker state

For worker `j`:

```text
W_j = (
  wage,
  liquid_savings,
  minimum_consumption,
  transition_cost,
  skill_vector,
  mobility,
  matching_probability,
  unemployment_duration,
  reservation_wage
)
```

Workers are not teleported between firms. Reallocation consumes time and resources.

A useful transition-runway condition is:

```text
liquid_savings + safety_net_support
    >= transition_cost + minimum_consumption * unemployment_duration
```

If the condition fails, a nominally available better job may be unreachable.

## Interventions and stresses

E024 should vary at least these axes independently before combining them:

1. **wage pressure** — wage floor or market wage increase;
2. **labor scarcity** — reduced worker availability / higher vacancy pressure;
3. **price-pass-through capacity** — how much added labor cost can reach output prices;
4. **buyer bargaining asymmetry** — downstream firms may be unable to renegotiate price;
5. **worker transition liquidity** — savings / bridge support / unemployment support;
6. **matching friction** — time and probability required to find a new job;
7. **automation substitutability** — whether firms can replace tasks with capital / software;
8. **demand elasticity** — whether customers accept resulting price increases.

Single-axis sweeps must precede composite stress so interaction-only failure regions can be identified rather than misattributed.

## Regimes to compare

### A — Productive reallocation

```text
wage pressure
-> weak low-productivity firms exit
-> workers move quickly
-> higher-productivity firms absorb labor
-> wages and productivity rise
```

### B — Transition-friction failure

```text
wage pressure
-> firm exit
-> workers lack runway / matching capacity
-> unemployment duration rises
-> worker welfare falls before reallocation completes
```

### C — Bargaining-power selection

```text
wage pressure
-> low-pass-through downstream firms exit
-> upstream / dominant buyers retain margin
-> concentration rises
-> exit is correlated more with bargaining weakness than productivity
```

### D — Automation substitution

```text
wage pressure
-> automation becomes economical
-> firm viability improves
-> labor demand falls
-> aggregate productivity may rise while worker outcomes diverge
```

## Primary outcomes

Do not optimize on bankruptcy count alone.

Track at minimum:

- firm survival by productivity decile;
- firm survival by bargaining-power / pass-through decile;
- worker employment rate;
- median and lower-decile worker income;
- time to re-employment;
- fraction of displaced workers successfully reallocated;
- fraction falling below a minimum-consumption floor;
- aggregate productivity;
- output and consumer-price change;
- market concentration;
- automation intensity;
- total safety-net / transition-bridge cost;
- firm diversity and entry rate.

## Candidate hypotheses

### H1 — Selection quality

If worker mobility is high and pass-through is approximately symmetric, wage pressure should preferentially remove low-productivity firms.

### H2 — Transition runway knee

Below a worker-liquidity threshold, the same wage shock should produce a discontinuous increase in failed reallocations even when destination jobs exist.

### H3 — Bargaining-power confound

With asymmetric pass-through, firm exit should become materially correlated with weak bargaining power even after controlling synthetic productivity.

### H4 — Concentration feedback

Selective downstream exit should increase buyer / platform concentration, which can further reduce pass-through and create a reinforcing loop.

### H5 — Automation bifurcation

As automation substitutability rises, firm survival can improve while worker income / employment diverges from aggregate productivity.

### H6 — Safety-net as allocation infrastructure

Bridge support can improve eventual reallocation not merely by transferring income, but by preventing workers from dropping out before a higher-value match becomes reachable.

## Promotion criteria

An E024 implementation should not be promoted merely because one regime looks intuitive. It should require:

1. exact accounting of wages, firm cash, worker cash, taxes / support, and explicit external sources / sinks;
2. no instantaneous worker reassignment;
3. separate measurement of productivity and bargaining power;
4. single-axis baselines before composite shocks;
5. failure-state biopsy for firm exit and worker dropout;
6. at least one counterexample where bankruptcy count points in the wrong direction for welfare;
7. replayable deterministic seeds plus held-out stress evaluation;
8. sensitivity analysis over transition liquidity and pass-through;
9. explicit non-claim that synthetic results estimate current Japanese policy effects.

## First implementation wedge

Keep the initial world small enough to enumerate selected slices exactly:

```text
3 productivity classes
x 3 bargaining-power classes
x 3 worker-liquidity classes
x 4 wage-pressure levels
x 3 pass-through regimes
```

Use exact enumeration for the smallest world as an oracle, then scale into Monte Carlo only after the transition and accounting invariants are verified.

## Why this belongs in Market Microcosm Lab

The existing lab asks whether an ecosystem remains viable under pressure. E024 extends that logic across the firm-worker boundary: actor exit is not the end of the story. The important object is the **reallocation path after exit**, including who can survive the path, where value migrates, and whether the resulting ecosystem remains worth participating in.

The research target is therefore not:

```text
minimize bankruptcies
```

or:

```text
maximize bankruptcies of weak firms
```

but rather:

```text
preserve a viable ecosystem while allowing resources to move toward higher-value uses
without hiding transition costs, bargaining asymmetry, or worker dropout.
```
