# ODD addendum — E076 active sensing for the certificate

E075 certifies a tight worst-case collection cost of **12.0** under marginal intervals and arbitrary dependence.

E076 asks a meta-level sensing question:

```text
What is the cheapest calibration evidence that can tighten
the robust certificate to <= 11.3?
```

Candidate synthetic calibration actions can tighten lower failure bounds for finance, GTM, strategy, or all axes.

Every calibration subset is enumerated. After each update, all six evidence bundle orders are recompiled under interval/dependence ambiguity.

The exact minimum target-reaching calibration is:

```text
gtm-incidence-study
calibration cost = 2
```

It raises the admitted lower bounds for market-headroom and downstream-funnel failure enough to reduce the tight robust acquisition bound:

```text
12.0 -> 11.2
```

The selected evidence order remains:

```text
GTM -> strategy -> finance
```

Finance-only or strategy-only calibration does not reach the 11.3 target.

The important object is not full prior recovery. It is **minimum calibration sufficient for the declared certificate target**.

Promotion: `acquire-minimum-calibration-evidence-to-meet-certificate-target-v1`.
