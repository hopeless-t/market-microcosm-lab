# ODD addendum — E059 dependency-depth stopping rule

## Purpose

E057 shows that failure-domain discovery is recursive.

Without a stopping rule, "verify the roots beneath the roots" can become an unbounded audit.

E059 makes the stopping condition downstream-authority scoped.

## Declared downstream contract

The E055/E056 observation code tolerates at most two correlated certified-channel failures for the current authority claim.

Recursive dependency auditing therefore needs to reduce the maximum unverified blast radius to at most two channels.

## Reference audit depths

| Depth | Cumulative cost | Maximum unverified correlated providers | Maximum channels |
| ---: | ---: | ---: | ---: |
| 0 | 0 | 5 | 10 |
| 1 | 2 | 2 | 4 |
| 2 | 5 | 1 | 2 |
| 3 | 9 | 1 | 2 |

Depth 0 only knows the repaired provider placement.

Depth 1 verifies network/identity segmentation but still allows one unknown dependency to span two providers.

Depth 2 verifies enough physical/vendor/power lineage that all remaining unverified descendants are provider-local.

Depth 3 adds endpoint detail but does not improve the cross-provider blast bound.

## Exact stopping rule

Choose the minimum-cost depth satisfying:

```text
maximum unverified correlated blast
<= downstream tolerated blast
```

The exact selected depth is:

```text
depth = 2
cost = 5
maximum residual blast = 2 channels
```

## Consequence

Dependency discovery does not stop because "we looked deep enough."

It stops because the remaining uncertainty can no longer violate the declared downstream authority contract.

## Promotion rule

`recursive-lineage-audit-stops-at-minimum-depth-meeting-blast-budget-v1`

## Limitation

The depth-specific upper bounds are admitted structural evidence. A newly discovered common mode can falsify them and revoke the stopping certificate.
