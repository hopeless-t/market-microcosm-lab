# ODD addendum — E094 SaaS exit runoff state machine

## Purpose

E029 introduces strategic exit as a control action.

E094 uses Jooto's public shutdown plan to attack the shortcut:

`EXIT_DECIDED => business instantly becomes zero`

## Public state transition

**2026-08-06 — RUNOFF_AND_MIGRATION begins**

- new registrations stop;
- new paid contracts stop;
- upgrades and new implementation/BPR work stop;
- existing customers remain served;
- service quality and security must be maintained;
- data export/migration and prepaid-fee settlement remain obligations;
- one-time transition costs may occur.

**2027-07-31 — general service ends**

The inclusive runoff period is **360 days**.

**2027-08-01 — FINAL_SHUTDOWN reference state**

## Consequence

Exit has at least two operational states:

`RUNOFF_AND_MIGRATION -> FINAL_SHUTDOWN`

Revenue, operating cost, customer obligations, and employee/resource transition do not disappear on the board-decision date.

Promotion:

`strategic-exit-is-runoff-state-machine-not-instant-zeroing-v1`
