# DCRE-021 — Value threshold for operational demand telemetry

## Trigger

DCRE-020 repairs rigid use-or-lose activation by deploying capacity only when realized demand needs it.

That arm assumes the demand state is observed correctly before activation.

DCRE-021 prices observation quality against activation waste and service loss.

## Frozen uncertainty

Reuse the DCRE-020 two-state world:

```text
LOW demand  = 100 with probability .5
HIGH demand = 160 with probability .5
baseline capacity = 100
optional capacity = 60
activation resource = .5 per capacity unit
unmet-demand penalty = 2 per task
```

Telemetry is symmetric: it reports the correct HIGH/LOW state with accuracy `q`.

## ALWAYS_ON

Activate all optional capacity regardless of demand:

```text
expected activation resource = 30
expected unmet demand = 0
expected loss = 30
```

This is safe for service but spends resources even in LOW demand.

## TELEMETRY_GATED

Activate the 60 optional units only when telemetry reports HIGH.

In the frozen symmetric world:

```text
expected loss = 75 - 60q
```

Break-even against ALWAYS_ON is therefore:

```text
75 - 60q = 30
q = .75
```

Examples:

```text
q=.60 -> activation 15, expected unmet 12, loss 39
q=.80 -> activation 15, expected unmet  6, loss 27
```

Below the accuracy knee, saving activation resource is not worth the service risk under the frozen penalty. Above it, telemetry becomes decision-relevant.

## Result

```text
demand-contingent control
!= valuable control
unless observation quality crosses a decision threshold
```

Operational telemetry is another scarce information good. Its value depends on the cost of false activation and false non-activation, not merely on nominal accuracy.

DCRE-021 does not claim `.75` is a real threshold. It is exact only for this synthetic loss surface.

## Reuse instead of reinvention

The obvious next attack is correlated telemetry failure. That mechanism is already represented by the qualified E022/E023 lineage (`WitnessTopology`, failure domains, and hidden `DependencyShock`). DCRE does not create a second sensor-independence framework.

Telemetry identities can be projected onto those existing failure-domain abstractions when needed.

## Claim ceiling

```text
authority_effect = NONE
claim_ceiling = SYNTHETIC_TELEMETRY_VALUE_KNEE
```

## Next new physical falsifier

DCRE-022 moves to **spatial resource allocation**: two regions have complementary energy/water headroom, so a globally attractive placement can still violate a local resource ceiling. This keeps foreground work on physical market ecology while reusing E022/E023 for observation-dependency questions.
