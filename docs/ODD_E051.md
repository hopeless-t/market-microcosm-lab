# ODD addendum — E051 active lineage discovery

## Purpose

E050 requires upstream lineage-root diversity, but it assumes the dependency graph is already known.

E051 attacks that assumption.

The experiment asks whether a hidden common root can be discovered from bounded intervention fingerprints rather than inferred from source names.

## Reference topology

Three apparently independent sources actually share one root:

```text
source-a / domain-a -> master-warehouse
source-b / domain-b -> master-warehouse
source-c / domain-c -> master-warehouse
source-d / domain-d -> independent-root-d
source-e / domain-e -> independent-root-e
```

## Bounded probes

The reference probe catalog contains candidate dependency interventions.

A probe targeted at `master-warehouse` affects source-a, source-b, and source-c simultaneously across three witness domains.

Local or unrelated probes do not create the same cross-domain fingerprint.

## Discovery criterion

A probe is evidence of a hidden common root when it perturbs at least three source observations spanning at least three declared witness domains.

The discovered dependency becomes an authority-changing event: any prior claim that the three affected sources represented independent evidence must be re-audited.

## Promotion rule

`hidden-lineage-roots-require-active-intervention-discovery-v1`

## Limitation

The reference assumes safe, perfectly observable probes. Real deployments need non-destructive canaries, intervention permission, noise models, and rollback.
