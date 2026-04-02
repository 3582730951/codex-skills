# C++ Adapter

Use this file when changed surfaces are written in C++.

## Core Rules

- Prefer RAII and value semantics by default.
- Make ownership and lifetime visible in types and interfaces.
- Use exceptions, status objects, or error codes consistently within the subsystem.
- Keep templates and metaprogramming proportional to real reuse.
- Minimize exposed mutable state.

## Quality Checks

- public APIs state ownership expectations
- resource cleanup is automatic or obviously enforced
- abstractions reduce complexity instead of moving it around
- tests can exercise failure paths without heroics

## Reject

- raw `new` / `delete` as the normal path
- unclear ownership at interface boundaries
- broad utility layers with no domain reason
- exception safety left to guesswork

## Basis

- C++ Core Guidelines: https://github.com/isocpp/CppCoreGuidelines
- SEI CERT C++ Coding Standard: https://wiki.sei.cmu.edu/confluence/display/cplusplus
