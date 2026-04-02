# Java Adapter

Use this file when changed surfaces are written in Java.

## Core Rules

- Public APIs state nullability, error semantics, and thread-safety expectations.
- Keep package boundaries meaningful and stable.
- Use interfaces and abstractions where they simplify substitution or testing, not by habit.
- Control object lifecycle, resource closing, and serialization boundaries explicitly.
- Keep services cohesive instead of building giant coordinator classes.

## Quality Checks

- package structure reflects architectural boundaries
- exceptions communicate the actual contract
- resources are closed deterministically
- concurrency assumptions are explicit
- reflection or serialization use is justified and bounded

## Reject

- utility or manager classes with broad unrelated responsibility
- silent null contracts
- hidden thread-safety assumptions
- dependency injection layers that add ceremony without value

## Basis

- Google Java Style Guide: https://google.github.io/styleguide/javaguide.html
- Oracle Secure Coding Guidelines for Java SE: https://www.oracle.com/technetwork/java/seccodeguide-139067.html
