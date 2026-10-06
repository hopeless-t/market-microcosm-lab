# RPE-004 — Wake-signal reliability adversary

## Question

RPE-003 showed that a rare but urgent dormant meaning can be kept cheap and still recovered if a prewarm signal arrives before the decision deadline.

RPE-004 attacks that assumption:

> What happens when the wake signal is missing, delayed, noisy, or otherwise untrustworthy?

## Scenario set

Five deterministic signal worlds are evaluated against the same 12-epoch residency fixture:

1. **healthy** — both true prewarm signals arrive one epoch early with high confidence;
2. **missing-first** — the first true signal is absent and the channel reports degraded health;
3. **delayed-first** — the first true signal arrives too late while channel health is degraded;
4. **false-positive** — two low-confidence false signals are injected between the true signals;
5. **combined** — the first true signal is missing while low-confidence false positives are also present.

The channel-health flag is an explicit synthetic observation. It is not inferred from the future demand event.

## Policies

### Naive any-signal prewarm

Any observed signal moves the rare meaning to WARM for the following epoch.

Expected failure:
- missing and delayed signals lose rare urgent value;
- false positives waste residency cost.

### Confidence-filtered prewarm

Only signals at or above the declared confidence threshold trigger WARM residency.

Expected improvement:
- low-confidence false-positive cost disappears.

Expected remaining failure:
- filtering cannot recover a signal that never arrived or arrived too late.

### Always-WARM rare meaning

Keeps the rare critical meaning WARM at every epoch.

This is the conservative readiness baseline: full value should survive every signal scenario, but holding cost is paid continuously.

### Certified hybrid

Uses high-confidence prewarm in healthy periods and falls back to conservative WARM residency while the signal channel is explicitly degraded.

This separates two questions:

```text
is the signal positive?
```

from:

```text
is the signal channel currently trustworthy enough to rely on absence?
```

A missing signal has meaning only while the observation channel itself is healthy.

## Expected synthetic result

Across the five scenarios:

- naive any-signal: 1149 / 1185 decision-value units at aggregate cost 604;
- confidence-filtered: same 1149 value at lower cost 596;
- always-WARM: all 1185 value at cost 685;
- certified hybrid: all 1185 value at cost 593.

Thus filtering alone handles false positives but not false negatives. In this fixture, explicit channel-health fallback recovers the missing/delayed cases while remaining cheaper than both naive signaling and permanent WARM residency.

These are fixture-relative results only.

## Candidate rule

```text
SIGNAL_DRIVEN_PREWARM
REQUIRES
CHANNEL_HEALTH_CERTIFICATION
AND
FAIL_CLOSED_RESIDENCY_FALLBACK
```

This mirrors the wider Market Microcosm lesson from E016/E017: an optimization may retain authority only while the evidence supporting its assumptions remains valid.

## Next falsifiers

RPE-005 should move beyond one rare meaning and attack finite warm-up capacity:

- multiple simultaneous rare signals;
- different values and deadlines;
- prewarm budget smaller than demand;
- greedy value/cost scheduling counterexamples;
- uncertain signal confidence and correlated false positives.

A later experiment should also attack semantic staleness: a meaning may wake on time and still be wrong because its canonical content is outdated.

## Claim ceiling

`DETERMINISTIC_SYNTHETIC_SIGNAL_HEALTH_FIXTURE_ONLY_NO_REAL_ALERT_RELIABILITY_CLAIM`
