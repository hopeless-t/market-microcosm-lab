# ODD addendum — E064 prospective evidence cutoff

## Purpose

Attack E063's use of Q4 event semantics.

The Q4 annotations are useful explanations of the realized transition.

They are not automatically legitimate features for a warning that is supposed to be issued at the Q3 disclosure date.

E064 makes evidence availability time explicit.

## Decision cutoff

```text
2025-08-14
```

This is the FY2025 Q3 public disclosure date used as the prospective decision boundary.

## Available at the cutoff

- Q3 ARR / churn / contract count / ARPA;
- Q3 management commentary;
- Q3 statement that the new Knowledge Suite release was expected to improve churn.

## Future-only relative to the cutoff

Available on the FY2025 Q4 disclosure date:

- Q4 outcome KPIs;
- Q4 statement that Knowledge Suite+ launch timing slipped and ARR decreased;
- Q4 statement that service-withdrawal preparation and launch delay temporarily reduced ARPA.

## Leakage rule

A retrospective analysis may use the Q4 event annotations to explain what happened.

A prospective Q3 warning evaluator may not use them as input features because they did not yet exist in the public evidence set.

Therefore:

```text
retrospective explanation authority
!=
prospective prediction authority
```

## Promotion rule

`prospective-warning-evidence-must-exist-before-decision-cutoff-v1`

## Limitation

Public disclosure time is the authority boundary for this experiment. Internal operators may have had earlier private information, but that would define a different dataset and access scope.
