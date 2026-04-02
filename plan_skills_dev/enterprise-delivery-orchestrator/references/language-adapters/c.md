# C Adapter

Use this file when changed surfaces are written in C.

## Core Rules

- Make ownership and cleanup explainable.
- Keep header surfaces minimal and stable.
- Validate external inputs at the boundary.
- Use one clear error convention per subsystem.
- Prefer simple control flow over clever macros or implicit coupling.

## System C Rules

For kernel, runtime, embedded, or driver code:

- document lock expectations
- document lifetime for buffers, handles, and shared state
- centralize cleanup or make cleanup paths obviously equivalent
- treat ABI, packing, and memory layout as contracts
- avoid hidden blocking or allocation in sensitive contexts

## Reject

- implicit ownership transfer
- resources cleaned up on the happy path only
- giant headers exposing internals
- macros that obscure control flow without strong justification

## Basis

- Linux kernel coding style: https://kernel.org/doc/html/next/process/coding-style.html
- SEI CERT C Coding Standard: https://wiki.sei.cmu.edu/confluence/display/c
