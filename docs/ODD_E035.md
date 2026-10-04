# ODD addendum — E035 negative-evidence early-warning tournament

## Purpose

Compile the Japanese failure mechanisms discovered in E028–E034 into a first exact early-warning benchmark.

The target is not a production bankruptcy predictor.

The target is to test whether familiar scalar proxies remain trustworthy when failure modes include liquidity lag, human-delivery burden, market ceiling, funnel attenuation, strategic exit, and intentional pruning.

## Reference scenarios

The finite suite contains:

- healthy scalable business;
- cash-conversion-lag trap;
- hidden human-delivery-cost trap;
- market-ceiling trap;
- funnel-quality trap;
- strategic-exit trap;
- healthy intentional-pruning case with elevated churn.

Each scenario carries an explicit oracle label for whether intervention is required.

## Candidate warning rules

### Revenue-only

Warn only when current revenue growth is non-positive.

This deliberately represents an overly optimistic growth heuristic.

### Churn-only

Warn whenever churn is elevated.

This tests the failure exposed by E030: intentional pruning can raise churn without indicating ecosystem deterioration.

### Multi-signal

Warn when any declared structural risk crosses its reference threshold:

- insufficient cash to bridge collection lag;
- fully loaded delivery margin below 20%;
- market headroom below 40%;
- downstream funnel success below 30%;
- strategic exit value greater than continuation value.

## Exact result

On the reference suite:

- revenue-only misses most failure archetypes;
- churn-only misses non-churn failure modes and false-alarms on healthy pruning;
- multi-signal exactly matches the declared oracle.

This exact match is not evidence that the thresholds generalize. It means the negative-evidence mechanisms have been successfully compiled into a testable warning vector.

## Promotion rule

`negative-evidence-multi-signal-early-warning-v1`

## Next research step

The warning vector must next leave the hand-constructed reference world.

Future work should:

1. generate broad Monte Carlo scenario families around each mechanism;
2. search for interaction-only early-warning failures;
3. calibrate thresholds on discovery scenarios;
4. use untouched holdouts;
5. seek real longitudinal company data to measure actual lead time and false-alert rate.

## Limitation

E035 is a structural benchmark, not a clinical or financial prediction service and not a claim about any named company's future.
