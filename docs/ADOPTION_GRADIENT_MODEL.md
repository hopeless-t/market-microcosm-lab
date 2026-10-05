# Adoption Gradient Model

Status: research hypothesis / synthetic-model candidate

## Motivation

A technology can have high semantic or technical value and still fail to spread if adoption requires users to cross too many simultaneous ecosystem boundaries. Programming-language history provides a useful hypothesis: ideas often survive even when the original language/product does not, because semantic traits are absorbed by systems with lower migration friction.

This is a natural Market Microcosm question because adoption is an ecosystem viability problem, not only a product-quality score.

## Candidate adoption model

A deliberately simple starting relation:

```text
AdoptionPressure ~
  SemanticValue
  * Interoperability
  * Tooling
  * EcosystemAccess
  * MigrationGradient
  / (LearningCost + MigrationCost + OperationalRisk)
```

This is not an empirical law. It is a synthetic mechanism to stress and falsify.

## Actors

Candidate world:

```text
Users / developers
Existing ecosystem
New technology
Tooling providers
Library / integration providers
Employers / production operators
```

Each actor can respond differently to technical value, switching cost, compatibility, perceived production risk, and network effects.

## Key variable: MigrationGradient

`MigrationGradient` represents whether adoption can happen in useful partial steps.

Examples:

```text
LOW gradient:
  replace language + build system + libraries + deployment + mental model at once

HIGH gradient:
  add one typed file / one adapter / one component / one project boundary at a time
```

Hypothesis:

> For equal intrinsic technical value, a smooth migration gradient can dominate a technically superior but discontinuous replacement path.

## Semantic gene transfer

Model ideas separately from products.

```text
Product population share
!=
Semantic trait population share
```

A product can decline while one of its traits spreads into competitors.

Candidate traits:

- ownership/resource discipline;
- algebraic data types/pattern matching;
- effect separation;
- stronger type-level constraints;
- state/update/view architecture;
- gradual typing;
- interoperable native compilation;
- structured diagnostics.

This permits a measurable state such as:

```text
original technology share -> low
trait diffusion across ecosystem -> high
```

which should not be classified as simple failure.

## Synthetic experiments

### E-A1: Equal value, different migration gradient

Hold intrinsic utility fixed. Vary migration cost and partial-adoption paths. Measure adoption, abandonment, ecosystem survival, and time-to-useful-value.

### E-A2: Superior technology with weak ecosystem access

Give one technology higher semantic value but poor tooling/library interoperability. Compare against a weaker technology embedded in a strong existing ecosystem.

### E-A3: Semantic gene survives product collapse

Allow traits from a declining technology to be adopted by competitors. Measure product extinction separately from trait survival.

### E-A4: Tooling rescue

Introduce improved diagnostics, package tooling, adapters, or migration automation after adoption stalls. Test whether ecosystem viability changes without changing core semantic value.

### E-A5: Canonical IR bridge

Introduce a provider-neutral semantic bridge that lowers migration cost between existing systems and a new technology. Test whether interoperability can shift the adoption knee without requiring full replacement.

## Observables

- active adopter population;
- retained adopter population;
- time-to-first-useful-value;
- migration completion rate;
- rollback/abandonment;
- ecosystem/library coverage;
- operator risk events;
- tooling cost;
- trait diffusion;
- product survival;
- total ecosystem viability.

## Important distinctions

```text
Technical Superiority != Adoption
Product Failure != Idea Failure
Interop Exists != Migration Is Cheap
High Adoption != Healthy Ecosystem
Trait Diffusion != Original Product Success
Synthetic Result != Historical Causal Proof
```

## Connection to Canonical IR

Canonical IR should be evaluated not only for representational elegance, but for whether it creates a smooth migration gradient:

```text
existing object
  -> lift into canonical semantics
  -> partial cross-system reuse
  -> lower back to existing target
```

If adoption requires replacing all languages, APIs, tools, and workflows at once, the design has failed the migration-gradient test even if the IR is internally elegant.

## Falsification direction

The model should admit worlds where migration gradient does *not* dominate: for example, a sufficiently large semantic-value advantage, strong coordination, regulation, a platform mandate, or catastrophic legacy cost may make abrupt replacement rational.

Working principle:

> Model adoption as ecosystem dynamics: good ideas need a survivable path into the world.
