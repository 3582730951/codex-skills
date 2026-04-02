# Rust Adapter

Use this file when changed surfaces are written in Rust.

## Core Rules

- Design the safe API first.
- Keep ownership, borrowing, and mutability obvious in the interface.
- Prefer domain types over loose maps or stringly-typed boundaries.
- Use `Result` and error enums intentionally.
- Keep public traits and generics as small as the real extension surface requires.

## Unsafe Rules

Every `unsafe` block or item must have a nearby `SAFETY:` explanation that states:

- why unsafe is necessary
- required preconditions
- why those preconditions hold here

## FFI And Runtime Rules

- isolate FFI boundaries
- convert raw inputs into safe domain types early
- document thread-safety and pinning expectations
- make cleanup and shutdown behavior explicit

## Reject

- `unsafe` with no proof comment
- traits or generics added only for future speculation
- public APIs exposing raw low-level details with no need

## Basis

- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/
- Rust Style Guide: https://doc.rust-lang.org/style-guide/
- Rust for Linux coding guidelines: https://docs.kernel.org/rust/coding-guidelines.html
