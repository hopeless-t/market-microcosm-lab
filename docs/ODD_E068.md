# ODD addendum — E068 decision-sufficient evidence acquisition

E067 solves the minimum authorized portfolio for **full five-axis direct coverage**.

E068 attacks the assumption that every decision needs that full state.

The warning is OR-shaped:

```text
WARN if any structural axis is bad
SAFE only if all five axes are directly observed safe
```

Exact subset search is run against finite reference worlds.

For a world where only downstream funnel success is bad, `crm-funnel-export` alone certifies WARN at cost **2**.

Across all single-bad-axis worlds, the exact warning-certificate cost ranges from **2 to 5**, always below E067's full-contract cost 14.

For the all-safe world, no shortcut exists: every axis must be directly observed, and the exact minimum is the E067 portfolio at cost **14**.

Therefore evidence requirements are asymmetric:

```text
positive warning certificate: one sufficient failing witness may be enough
safe certificate: complete direct coverage is required
```

This experiment is an information lower bound, not a deployable oracle policy. The search knows the reference truth only for evaluation. A real controller must decide which observation to request **before** knowing which axis is bad.

Promotion: `warning-evidence-acquisition-is-decision-sufficient-not-full-state-v1`.
