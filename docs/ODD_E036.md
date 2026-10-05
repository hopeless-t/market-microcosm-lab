# ODD addendum — E036 discovery-tuned early warning with untouched holdout

## Purpose

Attack E035's strongest limitation.

E035 exactly classified a seven-case hand-built reference suite. That is a compilation check, but a warning rule can appear perfect simply because the cases were designed around the same mechanisms.

E036 generates broad deterministic scenario populations and separates threshold discovery from holdout evaluation.

## Scenario generator

Each generated state samples:

- initial cash;
- booked revenue;
- cash cost;
- collection lag;
- fully-loaded delivery margin;
- market headroom;
- downstream success ratio;
- continuation value;
- strategic-exit value;
- revenue growth;
- an elevated-churn flag.

The six-month intervention oracle is true when at least one structural failure holds:

- simulated cash becomes negative before or after delayed collections;
- fully-loaded margin is below 5%;
- market headroom is below 15%;
- downstream success ratio is below 10%;
- strategic exit value exceeds continuation value.

Revenue growth and the churn flag do **not** define the oracle.

## Isolation

Discovery:

```text
seed = 32035
n = 500
```

Untouched holdout:

```text
seed = 42035
n = 500
```

The holdout is never used for threshold selection.

## Threshold search

The candidate grid varies:

- cash coverage ratio: 0.75, 1.0, 1.25, 1.5;
- fully-loaded margin: 0%, 5%, 10%;
- market headroom: 10%, 15%, 20%;
- downstream success: 8%, 10%, 15%;
- strategic-exit gap: -10, 0, +10.

That produces 324 candidate warning configurations.

Selection maximizes discovery F1, then recall, then minimizes false positives with deterministic tie-breaking.

## Result

The selected threshold vector is:

```text
cash coverage ratio = 1.0
fully-loaded margin = 0.05
market headroom = 0.15
downstream success = 0.10
strategic-exit gap = 0
```

On the untouched generated holdout, the multi-signal rule retains greater than 98% precision, recall, and F1.

Revenue-only holdout recall remains below 25%.

Churn-only holdout recall remains below 30%.

## Interpretation

This is the first step beyond the hand-built E035 cases.

It demonstrates within-family generalization and correct seed-bank isolation. It does **not** demonstrate real-company predictive validity because discovery and holdout share the same structural generator.

## Promotion rule

`discovery-tuned-multi-signal-warning-with-holdout-v1`

## Next falsification

E037 should deliberately mutate the structural generator — interaction terms, nonlinear cost escalation, correlated failures, delayed observations, and definition drift — and measure how rapidly the E036 warning loses authority.
