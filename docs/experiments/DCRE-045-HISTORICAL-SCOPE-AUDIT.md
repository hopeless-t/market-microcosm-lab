# DCRE-045 — Historical scope alignment is not causal identification

## Trigger

DCRE-044 introduced a scope-alignment gate before any empirical number may constrain a synthetic coefficient.

A natural next question is whether the LBNL 2024 U.S. Data Center Energy Usage Report already contains a historical pair suitable for calibrating the DCRE demand/rebound parameter `eta`.

It contains two closely aligned historical objects:

1. U.S. data-center **server installed base** from 2014 onward;
2. U.S. data-center **server electricity use** from 2014 onward.

At first glance this looks like the missing empirical pair. DCRE-045 audits whether it is actually admissible for causal calibration.

## Primary source

Lawrence Berkeley National Laboratory, *2024 United States Data Center Energy Usage Report*, LBNL-2001637.

Source page:

`https://eta-publications.lbl.gov/publications/2024-lbnl-data-center-energy-usage-report`

Report PDF:

`https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report.pdf`

Relevant report locations:

- Methodology overview: installed base is generated from equipment shipment data; annual energy is produced from installed base plus wattage/operation assumptions.
- pp. 30–31 / Figure 3.9: server installed base.
- p. 49 / Figure 5.1: server annual electricity use.

The text reports a 2014 server installed base of 14 million and a 2020 installed base of 21 million. It also reports server electricity rising from about 30 TWh in 2014 to nearly 100 TWh in 2023.

## What aligns

```text
geography       = U.S. data centers
component scope = servers
historical era  = 2014–2023 overlap
```

This is much better aligned than mixing accelerator shipment flow, fleet-wide facility electricity, corporate PUE/WUE, or unrelated forecast horizons.

## Why `eta` still remains UNKNOWN

### 1. The two series are not independent observations

The report is a bottom-up model.

The installed base is itself constructed from shipment data plus assumed equipment lifetime. Server electricity is then calculated from installed base together with server-type power, utilization/operational-time, idle-power, and related assumptions.

Therefore:

```text
installed-base model output
-> electricity model output
```

is not an independent observational pair from which a causal response parameter can be identified.

### 2. Server count is not service demand or compute output

A server is a heterogeneous stock unit. Between 2014 and 2023 the mix changes materially, including GPU-accelerated systems, while average power and utilization also change.

Therefore:

```text
server stock growth
!= compute-service demand growth
!= useful-output growth
```

A ratio of electricity growth to server-count growth would mix hardware composition, utilization, power density, facility efficiency, and demand.

### 3. Public prose does not expose a complete exact paired annual table

Figures provide historical trajectories, but DCRE does not authorize chart digitization as an automatic path to a precise structural coefficient. Approximate visual extraction would add false precision on top of already model-derived quantities.

## Contract

DCRE-045 therefore records:

```text
scope_aligned                = TRUE
historical_overlap           = TRUE
provenance_independent       = FALSE
demand_semantics_aligned     = FALSE
complete_public_paired_table = FALSE
causal_calibration_admissible= FALSE
candidate_eta                = UNKNOWN
```

The important result is that **scope alignment is necessary but not sufficient**.

## Promotion gate for future empirical calibration

A future `eta` candidate requires, at minimum:

1. matched geography and system boundary;
2. matched time interval and temporal grain;
3. an observed or independently estimated demand/output quantity rather than equipment stock alone;
4. an electricity/resource outcome not mechanically derived from that same demand proxy by the same model;
5. enough public numeric resolution to reproduce the estimate without chart-reading guesswork;
6. explicit treatment of hardware mix, utilization, and efficiency confounders.

Until then:

```text
eta = UNKNOWN
```

is the promoted state.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = EMPIRICAL_IDENTIFIABILITY_AUDIT_ONLY
```

DCRE-045 does not estimate rebound, Jevons effects, demand elasticity, or real-world causal coefficients.

## Next falsifier

DCRE-046 should search for a genuinely independent demand/output series at compatible scope: workload volume, compute delivered, accelerator-hours, cloud-service output, or another reproducible activity measure paired with electricity. If no such public series exists, the missing-observation boundary should be promoted rather than replaced with a proxy by convenience.
