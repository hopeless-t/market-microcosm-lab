# ODD protocol — E000 finite market microcosm

## Overview

### Purpose
E000 is a deliberately tiny market ecosystem used to verify the laboratory machinery before realism is added. It asks whether allocation policies can keep a platform and two developer populations solvent under bounded shocks.

### Entities, state variables, and scales
Entities are one platform and two developer classes. The finite state is integer reserve capital for each actor in [0, 4]. One step is an abstract accounting period.

### Process overview and scheduling
At each step the observer exposes allowed reserve information, the governor chooses a payout action, an exogenous disturbance is applied, and the world transition is computed. Viability is evaluated after the transition.

## Design concepts

- Basic principle: robust viability, not one-period profit.
- Adaptation: governors alter payouts in response to observed reserve imbalance.
- Objectives: stay viable first; improve reserve/welfare margin second.
- Prediction: the oracle computes actions from complete state and the exact viability kernel.
- Sensing: deployable policies receive only ToyObservation; coarse mode intentionally compresses state.
- Stochasticity: experiment scenarios sample declared disturbances from seeded PRNGs.
- Observation: world truth, policy observation, and verifier evidence are separate records.

## Details

### Initialization
Promotion scenarios begin from states in the exact robust viability kernel.

### Input data
E000 uses no external empirical data. All parameters are explicit constants in ToyWorld.

### Submodels
The transition includes subscription revenue, platform burn, developer burn, payout allocation, bounded reserve capacity, and developer-specific shocks.

## Limitations
E000 is a correctness target, not an empirical model of Game Pass, Netflix, or SARTRAS. Its value is that the complete state/action graph can be enumerated and checked exactly.
