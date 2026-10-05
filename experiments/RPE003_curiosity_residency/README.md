# RPE-003 — Curiosity residency and wake-up economics

## Question

RPE-001 preserves dormant canonical meaning instead of forcing every idea into downstream work. RPE-003 asks whether that option value is actually usable:

> Can knowledge remain cheap while dormant and still become available before a decision deadline?

The experiment treats research attention as a residency system with four tiers:

| Tier | Holding cost / epoch | Wake latency | Wake cost |
| --- | ---: | ---: | ---: |
| HOT | 4.0 | 0 | 0.0 |
| WARM | 2.0 | 1 | 1.0 |
| COLD | 0.5 | 2 | 3.0 |
| DORMANT | 0.0 | 4 | 6.0 |

These numbers are synthetic bookkeeping units, not measured token, API, RAM, or Human-attention costs.

## Fixture

Twelve epochs contain six canonical meanings:

- a continuously demanded canonical kernel with a zero-latency deadline;
- a frequent finite-RAM line that tolerates WARM wake latency;
- PCG and labor-transition lines that tolerate COLD wake latency;
- a rare but urgent dormant-social-capital line with only two demand events;
- an archive-only line that is never demanded.

The rare urgent line emits an explicit prewarm signal one epoch before each demand.

Total possible decision value is 237 synthetic units.

## Policies

### Always HOT

Everything remains resident. This is the maximum-readiness baseline and should capture all value, but it pays holding cost even for unused knowledge.

### All DORMANT

Nothing is held resident. This is the minimum-holding-cost baseline and should fail urgent deadlines because wake latency is too long.

### Static tiering

Frequently used meanings are assigned permanent HOT/WARM/COLD tiers by broad demand class. Rare knowledge remains DORMANT.

This should handle ordinary traffic cheaply but miss the rare urgent line.

### Recency only

Residency depends only on how recently the meaning was demanded. It has no prior signal for first use and therefore exposes cold-start and long-gap failures.

### Signal-aware prewarm

Uses the same static baseline but temporarily raises a meaning to WARM when an explicit decision-hazard signal was observed in the previous epoch.

The signal does not create downstream authority. It only changes residency.

## Core distinction

```text
canonical meaning preserved
!=
meaning ready before the deadline
```

Dormancy preserves option value only if the system also has a bounded reactivation path.

## Expected synthetic result

- always-HOT: 100% value, highest holding cost;
- all-DORMANT: urgent value collapses;
- static tiering: ordinary value survives but rare urgent demand is missed;
- recency-only: cold-start / long-gap loss remains;
- signal-aware prewarm: all 237 value units are captured at substantially lower cost than always-HOT.

The intended comparison is multi-objective. `value_per_resource_cost` is reported but is not a promotion authority by itself.

## Candidate rule

```text
PRESERVE_DORMANT_OPTION_VALUE
AND
PREWARM_ONLY_ON_DECISION_HAZARD_SIGNALS
```

This is the Curiosity Intake analogue of demand-paged residency: retain meaning cheaply, keep a small HOT substrate, and move dormant knowledge toward residency only when a decision boundary approaches.

## Falsifiers

RPE-004 should attack the strongest new assumption: the prewarm signal.

Useful adversaries include:

- missing signals;
- false-positive signals;
- signal delay;
- burst demand with insufficient warm-up capacity;
- stale canonical meaning that wakes successfully but is no longer valid.

## Claim ceiling

`DETERMINISTIC_SYNTHETIC_WAKE_SIGNAL_FIXTURE_ONLY_NO_REAL_ATTENTION_SCHEDULER_CLAIM`
