# Plan Completeness Bar

Use this file before implementation. The purpose is to stop shallow plans from being treated as execution-ready.

## What A Complete Plan Must Cover

- explicit release slice
- in-scope and out-of-scope boundaries
- target user or operator
- success criteria that can be tested
- major journeys or flows
- module boundaries
- API and function boundaries
- validation strategy
- ownership and sequencing
- residual risks and explicit omissions

## Required Dimensions

Score each dimension from `0` to `5`:

- scope clarity
- contract completeness
- execution readiness
- validation readiness
- de-scope honesty

Any dimension below `4` means the plan is not ready for implementation.

## Red Flags

Reject the plan if it:

- describes a product without a release slice
- omits non-goals
- has vague "build the backend/frontend" steps with no contracts
- starts coding before ownership, validation, or merge order is defined
- lists aspirations instead of testable acceptance
- hides uncertainty instead of cutting scope

## Required Evidence

Before coding starts, the PM should be able to point to:

- `Task Charter`
- `Product/Experience Brief`
- `Architecture Contract`
- `Execution Contract`
- `Capability Routing Table`
- `Plan Coverage Matrix`

Use `scripts/score_plan_quality.py` and `scripts/check_capability_routing.py` for a mechanical first pass.
