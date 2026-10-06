# DCRE-057 — Contracted minimum and delivery availability do not identify realized load

## Trigger

DCRE-056 formalized the exact theorem:

```text
annual energy <= peak capacity * 8760 hours
```

but refused to apply a utility-territory load value to one Google site.

A second route might be to infer utilization from contract terms.

Northern Wasco County PUD publicly describes large-load service agreements with:

- minimum power purchase commitments based on customer forecasts;
- take-or-pay provisions;
- continuous 8,760-hour-per-year power delivery requirements.

DCRE-057 asks whether those contract surfaces identify realized load factor or annual energy.

## Primary source

Northern Wasco County PUD — Data Center Services:

- https://www.nwascopud.org/about-us/data-center-services/

The utility states that large-load agreements include minimum purchase commitments, take-or-pay protections, coordinated connection timing, and continuous power delivery requirements.

## Semantic distinction

A take-or-pay commitment constrains commercial obligations.

A 24/7/365 delivery requirement constrains service availability.

Neither directly measures electricity actually consumed.

Therefore:

```text
contracted minimum != realized load
```

and:

```text
delivery availability != energy used
```

Even if a utility is prepared to deliver firm power every hour of the year, the customer can still have time-varying utilization below its connection or contract envelope.

## Missing observations

The inspected public surface does not expose:

```text
customer-specific minimum commitment MW
customer-specific interval-meter series
customer-specific annual load factor
customer-specific annual MWh
```

Therefore no realized-energy reconstruction is authorized.

## Machine-readable result

```text
minimum_purchase_commitment_exists = TRUE
minimum_purchase_commitment_value  = UNKNOWN
take_or_pay_exists                 = TRUE
delivery_hours_available           = 8760
customer_interval_series           = UNOBSERVED
realized_load_factor               = UNKNOWN
Google_The_Dalles_annual_MWh       = UNKNOWN
authority_effect                   = NONE
```

## Result

DCRE-055 showed that aggregate system energy and capacity records do not identify customer annual energy.

DCRE-056 showed that a valid power-to-energy theorem cannot be populated with a capacity value from the wrong population.

DCRE-057 now closes a third shortcut: contractual obligations and service availability cannot be silently retyped as realized utilization.

The empirical state is therefore:

```text
site water              = observed
site PUE                = observed
utility aggregate load  = observed
capacity context        = observed
contract structure      = observed
realized site load      = unobserved
```

## Claim ceiling

```text
claim_ceiling = CONTRACT_VS_REALIZED_LOAD_OBSERVABILITY_AUDIT_ONLY
```

No load factor, annual MWh, WUE, or energy-water substitution coefficient is inferred.

## Next falsifier

DCRE-058 should stop chasing the same hidden customer meter unless a genuinely new data surface appears. Instead, it should ask what **system-level** empirical questions can be answered with the quantities that are public: utility load growth, data-center-attributed growth narratives, water use, PUE, and resource-planning rules. The next empirical objective should be to identify a robust system-level claim that does not require customer-specific MWh.
