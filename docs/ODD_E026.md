# ODD addendum — E026 sampled-observation assumption audit

## Purpose

Use the admitted SARTRAS sampling anchor to test what a published sample count can and cannot justify.

The source reports 35,130 applications in FY2022, approximately 1,200 sampled institutions, approximately 46,600 usage reports, and approximately 118,600 works in those reports. SARTRAS also describes the reporting system as a sample method designed to balance survey accuracy against burden and states that each institution normally reports for one designated month.

The public material establishes that sampling exists. E026 deliberately does **not** assume that the selection is uniform random sampling.

## Stage A — optimistic reference world

As a mathematical checksum, E026 first creates a hypothetical simple-random-sampling-without-replacement world.

For population size (N), sample size (n), and (m) institutions carrying an event of interest:

```text
P(detect at least one)
  = 1 - C(N-m, n) / C(N, n)
```

The implementation evaluates the equivalent sequential product to avoid huge combinatorial intermediates.

With (N = 35,130) and (n = 1,200):

- 87 carrier institutions are sufficient to cross 95% detection in the SRS reference;
- 133 are sufficient to cross 99%;
- a one-per-thousand phenomenon is detected only about 70%, not 95%, even in this optimistic reference.

The 95% SRS knee is therefore around 0.25% population prevalence.

## Stage B — adversarial assumption audit

The meta-loop then attacks its own SRS assumption.

If the selection mechanism is unconstrained, a sample of 1,200 can be drawn entirely from non-carrier institutions whenever at least 1,200 non-carriers exist.

For the same 87-carrier population that gives greater than 95% detection under SRS, an unconstrained selection mechanism can still produce zero observed carriers.

Therefore:

```text
sample size
!= inclusion probabilities
!= representativeness certificate
```

The numerical SRS curve is retained as a reference world but loses authority as an empirical uncertainty calibration.

## Promoted rule

E026 promotes:

`sampling-design-metadata-required-before-prevalence-inference-v1`

Before sample-derived prevalence or observation-noise calibration may become authoritative, the empirical plane must identify enough of the selection design to justify the estimator, including where applicable:

- sampling frame;
- strata;
- inclusion probabilities or weighting rule;
- nonresponse handling;
- time-window assignment.

## Consequence for the market model

Future SARTRAS-like worlds must distinguish:

- latent population state;
- selected institutions;
- reported observations;
- weighting / estimator;
- downstream allocation decision.

The Governor may receive sampled observations. The Oracle may retain full population state for simulation checks. The two must not be silently merged.

## Limitation

E026 does not state or imply that SARTRAS used simple random sampling, biased sampling, or any particular inclusion design. The adversarial world demonstrates non-identifiability from sample count alone.
