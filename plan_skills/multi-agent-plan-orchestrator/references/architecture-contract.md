# Architecture Contract

Use this file when the architect needs to produce a binding design that engineers and reviewers can execute against without guesswork.

## Contract Rule

For any `standard` or `heavy` task, do not start implementation until the architect has produced an `Architecture Contract`.

The contract is not a loose sketch. It is the binding reference for:

- boundaries
- invariants
- interfaces
- coding rules specific to the task
- validation strategy
- migration or rollback shape

If a section is unknown, mark it explicitly as unknown and assign an owner to resolve it. Do not hide uncertainty behind generic wording.

## Required Sections

Write the contract with these sections:

```text
Objective:
Scope:
Non-Goals:
Source Artifacts:
System Boundaries:
File And Module Ownership:
Interfaces And Data Contracts:
Invariants:
Failure Modes And Error Handling:
Regression Perimeter:
Unchanged Guarantees:
Probable Failure Scenarios:
Task-Specific Coding Rules:
Implementation Tracks:
Validation Strategy:
Migration Or Rollback:
Security Notes:
Open Questions:
```

## Task-Specific Coding Rules

Do not settle for generic style rules.

Require rules that materially shape the implementation, such as:

- where validation happens
- how errors are surfaced
- what may or may not be hardcoded
- logging and observability boundaries
- transaction or concurrency rules
- nullability and default handling
- API compatibility constraints
- performance budgets
- feature-flag expectations

If different engineers could read the contract and still produce incompatible implementations, the coding rules are not detailed enough.

## Regression Perimeter

For bug fixes and behavior changes, require the contract to map:

- the directly changed path
- neighboring paths that rely on the same helper, state, or contract
- upstream callers and downstream effects
- observability or rollback signals that would show collateral damage

Make the architect write down what must remain unchanged as well as what will change.

## Implementation Tracks

For each engineering track, specify:

- owned files or modules
- allowed touch points outside the owned boundary
- expected artifacts
- dependencies on other tracks
- explicit tests or checks that must pass before merge

## Reviewer Checklist

The architecture reviewer should reject the contract if:

- file ownership is missing or ambiguous
- interfaces are described without concrete contracts
- invariants are absent
- regression perimeter is missing for a bug fix or behavior change
- unchanged guarantees are not written down
- probable failure scenarios stop at the reproduced bug
- validation strategy is too vague to test
- migration, rollback, or compatibility impact is ignored when relevant
- coding rules are generic enough to permit inconsistent implementations

## Minimal Example Skeleton

```text
Objective: Add X without changing Y.
Scope: Touch modules A and B.
Non-Goals: No schema redesign.
Source Artifacts: issue-123, current API contract, failing test T.
System Boundaries: Service A may call B through adapter C only.
File And Module Ownership: Engineer A owns adapter C; Engineer B owns tests in module T.
Interfaces And Data Contracts: Request field q is required, trimmed, and max 256 chars.
Invariants: Existing endpoint response schema must remain backward-compatible.
Failure Modes And Error Handling: Validation errors return 400; downstream timeout maps to retryable error path.
Regression Perimeter: adapter C, retry helper R, timeout metrics, and integration path I must be checked.
Unchanged Guarantees: response schema, retry budget, and log redaction rules stay unchanged.
Probable Failure Scenarios: timeout fix could hide retries, double-log failures, or break existing metric labels.
Task-Specific Coding Rules: No fallback to hardcoded defaults; validate at boundary; log only request IDs.
Implementation Tracks: Track 1 adapter change; Track 2 regression tests.
Validation Strategy: unit tests U1-U3, integration I1, manual timeout simulation.
Migration Or Rollback: guarded by feature flag F; rollback disables new branch only.
Security Notes: sanitize q before logging.
Open Questions: whether timeout budget changes; owner Architect.
```
