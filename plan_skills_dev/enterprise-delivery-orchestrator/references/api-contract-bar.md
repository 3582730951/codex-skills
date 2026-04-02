# API Contract And Function Boundary Bar

Use this file whenever the task exposes or changes an API, module boundary, or public function.

## Contract Rules

- Public interfaces are part of the product. Treat them as design, not leftovers from coding.
- Every changed boundary must appear in the `API Contract Table` or `Function Boundary Table`.
- "Internal for now" is not an excuse when multiple modules depend on the interface.

## API Quality Bar

Require, at minimum:

- stable naming that matches the task domain
- explicit input and output schema
- explicit failure semantics
- auth / trust-boundary handling when applicable
- side-effect and idempotency rules
- compatibility expectations for callers
- observability hooks for debugging and rollout

Reject APIs that:

- leak storage or transport details without need
- return shapeless blobs when a typed contract is available
- hide error semantics behind vague booleans or generic status strings
- mix validation, business logic, and transport logic in one boundary

## Function Boundary Rules

Public or cross-module functions must have:

- one clear responsibility
- explicit inputs and outputs
- explainable side effects
- local validation responsibility
- test coverage aligned with the responsibility

Reject functions that:

- combine parsing, validation, I/O, orchestration, and policy in one body
- mutate shared state without explicit concurrency or ownership rules
- expose more parameters or options than their responsibility justifies
- use AI-generic naming such as `processData`, `handleThing`, or `runTask`

## System And Low-Level Boundaries

For FFI, JNI, ABI, or runtime boundaries, require:

- exact ownership rules
- exact memory / lifetime rules
- exact threading expectations
- exact error propagation model
- cleanup responsibility on all paths

Load [system-architecture-bar.md](system-architecture-bar.md) when these surfaces appear.

## Basis

- Stripe API versioning  
  https://docs.stripe.com/api/versioning
- Stripe idempotent requests  
  https://docs.stripe.com/api/idempotent_requests
