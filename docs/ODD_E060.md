# ODD addendum — E060 heterogeneous dependency-audit allocation

## Purpose

E059 compiles one minimum global audit depth.

E060 attacks the assumption that every dependency branch needs the same depth.

Different branches can have different residual blast bounds and different evidence costs.

## Reference branches

The downstream authority budget remains:

```text
maximum residual blast <= 2 certified channels
```

Each branch exposes several audit options.

The exact optimizer selects:

| Branch | Selected option | Cost | Residual blast |
| --- | --- | ---: | ---: |
| network | targeted | 2 | 2 |
| identity | targeted | 1 | 2 |
| power | deep | 3 | 2 |
| vendor | none | 0 | 2 |
| operator | targeted | 2 | 2 |

Total cost:

```text
8
```

A uniform "deep audit everything" policy costs:

```text
4 + 3 + 3 + 2 + 4 = 16
```

with no stronger downstream authority in this reference.

## Consequence

Recursive dependency depth becomes branch-specific.

The optimization problem is:

```text
minimize total audit cost
subject to
every dependency branch discharging its blast-radius proof obligation
```

This is the dependency-audit analogue of E045 predicate-scoped sensing.

## Promotion rule

`recursive-lineage-audit-depth-is-allocated-per-proof-obligation-v1`

## Limitation

The reference treats branch audits as independent. Real audit actions can cover multiple branches or share fixed costs, motivating a coupled bundle optimizer.
