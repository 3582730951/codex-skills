# Feasibility Envelope

Use this file when the user expects the skill to take a requirement and output a "complete product".

## Truth First

This skill can orchestrate delivery of a strong, usable, reviewable product slice. It cannot honestly guarantee that any arbitrary prompt will become a fully mature production-grade company product in one pass.

The correct promise is:

- if the requirement is bounded, the stack is known or can be chosen quickly, and the external dependencies are manageable, the skill can drive a multi-agent implementation toward a coherent product deliverable
- if the requirement is too broad, the skill must first reduce it to a credible release slice

## Complete Product Definition

Treat "complete product" as a release slice with:

- a clearly bounded problem and user
- core user journeys implemented end to end
- product/UI direction, not just raw screens
- stable contracts between major modules
- tests for core paths
- explicit non-goals
- release readiness status
- residual risks stated honestly

Do not treat "complete product" as:

- every future feature imagined by the user
- enterprise-scale reliability for all unknown traffic patterns
- full operations maturity without infrastructure, credentials, environments, and external integration access

## Delivery Classes

### Class A: Direct Delivery

Examples:

- a focused internal tool
- a bounded CRUD app with real product polish
- a contained API service
- a single-system runtime feature

Action:

- proceed through the full skill flow

### Class B: Parallel Delivery

Examples:

- a product with clear separable frontend, backend, and testing tracks
- a system tool with distinct architecture, implementation, and verification tracks

Action:

- split into parallel tracks
- define file ownership and merge order before coding
- use real delegated workers when available

### Class C: Must De-Scope First

Examples:

- "build a full SaaS like X" with no narrower release target
- multi-platform products with payments, auth, admin, analytics, marketing site, mobile apps, and infra in one request
- system projects with unclear OS, ABI, hardware, or performance constraints

Action:

- stop broad implementation
- produce a release-1 scope with explicit omissions
- ask for confirmation if the scope cut changes product intent materially

## Multi-Agent Parallel Rule

Multi-agent parallel delivery is only credible when:

- tracks are separable
- contracts can be written before coding
- one file has one owner at a time
- reviewers remain independent

If these are not true, parallelism increases churn instead of speed.

## Red Flags

De-scope instead of pretending when:

- the user request contains multiple products, not one
- the repository and stack are both undefined
- external services or credentials are required but unavailable
- acceptance criteria are aspirational rather than testable
- the request would require undiscoverable business decisions
