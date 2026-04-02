# TypeScript Adapter

Use this file when changed surfaces are written in TypeScript.

## Core Rules

- Keep public interfaces fully typed.
- Treat `any` as an exception, not a convenience.
- Validate untrusted input at the I/O boundary.
- Prefer discriminated unions and domain types over loose string flags.
- Keep server/client, API/UI, and domain/transport boundaries explicit.

## Frontend And Full-Stack Checks

- props and DTOs must reflect real product semantics
- async states need loading, success, and failure handling
- avoid boolean-prop sprawl when a state model is clearer
- route and data boundaries must be explainable
- generated types should not replace contract thinking

## Reject

- casual `any`, `as unknown as`, or broad type assertions in core paths
- components that mix data fetching, transformation, layout, and policy without a boundary
- convenience objects with optional fields for every scenario

## Basis

- TypeScript handbook and strict typing conventions are implied, but repository rules still take priority
